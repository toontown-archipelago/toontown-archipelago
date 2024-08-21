import ssl
import time
import traceback

import urllib.parse

from _socket import gaierror
from direct.showbase.DirectObject import DirectObject
from direct.stdpy import threading
from typing import List, Dict, Union

import certifi
from websockets import ConnectionClosed, InvalidURI, InvalidMessage
from websockets.sync.client import connect, ClientConnection

from toontown.archipelago.apclient.ap_client_enums import APClientEnums
from toontown.archipelago.util import net_utils, global_text_properties
from toontown.archipelago.util.data_package import DataPackage
from toontown.archipelago.util.global_text_properties import MinimalJsonMessagePart, get_raw_formatted_string
from toontown.archipelago.util.location_scouts_cache import LocationScoutsCache
from toontown.archipelago.util.net_utils import encode, decode, NetworkSlot, item_flag_to_color, NetworkPlayer
from toontown.archipelago.packets import packet_registry
from toontown.archipelago.packets.archipelago_packet_base import ArchipelagoPacketBase
from toontown.archipelago.packets.clientbound.clientbound_packet_base import ClientBoundPacketBase
from toontown.archipelago.packets.serverbound.connect_packet import ConnectPacket
from toontown.archipelago.packets.serverbound.serverbound_packet_base import ServerBoundPacketBase
from toontown.archipelago.util.utils import cache_argsless

# TODO find dynamic way to do this
DEFAULT_ARCHIPELAGO_SERVER_ADDRESS = "localhost"
DEFAULT_PORT = 38281


@cache_argsless
def get_ssl_context():
    return ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=certifi.where())


# Class to handle sending and receiving packets through a socket estabilished via the archipelago server
class ArchipelagoClient(DirectObject):

    notify = directNotify.newCategory("ArchipelagoClient")

    def __init__(self, av, slot_name: str = '', password: str = ''):

        self.state = APClientEnums.DISCONNECTED

        # Address to connect to (IP of archipelago server)
        # Given from the client to be attempt address
        self.address: str = f"{DEFAULT_ARCHIPELAGO_SERVER_ADDRESS}:{DEFAULT_PORT}"

        # Parsed from the address
        self.port = DEFAULT_PORT
        self.slot_name = slot_name  # slot assigned for seed generation
        self.password: str = password  # password if required
        # Socket interface of the archipelago server
        self.socket: ClientConnection = None

        # Store some identification
        self.av = av  # DistributedToonAI that owns this client
        self.slot: int = -1  # Our slot ID given when we connect
        self.team: int = 999
        self.uuid: str = av.getUUID() # not sure how important this is atm but just generating something in update_id method

        # Actually defines correct values for variables above
        self.update_identification(slot_name, password)

        # Store information for retrieval later that we received from packets
        self.slot_id_to_slot_name: Dict[int, NetworkSlot] = {}
        self.data_packages: Dict[str, DataPackage] = {}
        self.global_data_package: DataPackage = DataPackage()
        self.location_scouts_cache: LocationScoutsCache = LocationScoutsCache()

    def has_slot_info(self, slot_id: int) -> bool:
        return slot_id in self.slot_id_to_slot_name

    # Given a slot number (as string or int, doesn't matter but must be a number) return the NetworkSlot as cached
    def get_slot_info(self, slot: Union[str, int]) -> NetworkSlot:
        return self.slot_id_to_slot_name[int(slot)]

    # Returns the local slot ID (int) that this client belongs to
    def get_local_slot(self) -> int:
        return self.slot

    # Retrieve the name of a player in this AP session
    def get_player_name(self, slot_id: int) -> str:

        if not self.has_slot_info(slot_id):
            return f"??? (player {slot_id})"

        return self.get_slot_info(slot_id).name

    # Given the ID of an item, find a display name for the item using our data package
    def get_item_name(self, item_id: Union[str, int]) -> str:
        return self.global_data_package.get_item_from_id(item_id)

    # Given the ID of location, find a display name for the location using our data package
    def get_location_name(self, location_id: Union[str, int]) -> str:
        return self.global_data_package.get_location_from_id(location_id)

    def __get_packet_handle_event_name(self):
        return self.av.uniqueName(f'incoming-ap-packet')

    # Starts up the socket thread
    def start(self):

        # If we are not disconnected we aren't allowed to do this
        if self.state != APClientEnums.DISCONNECTED:
            raise Exception("You are already connected!")

        # Run the socket thread and let it do whatever
        self.accept(self.__get_packet_handle_event_name(), self.handle_message_from_server)
        thread = threading.Thread(target=self.__socket_thread, daemon=True)
        thread.start()

    # Attempt to use the socket to send a ConnectPacket
    def connect(self):

        # If we aren't connected yet, estabilish a connection
        if self.state == APClientEnums.DISCONNECTED:
            return self.start()

        if self.state == APClientEnums.CONNECTING:
            raise Exception(f"You are already attempting to connect! Please wait a second!")

        # If we are already connected, don't do anything
        if self.state == APClientEnums.PLAYING:
            raise Exception(f"You are already connected with slot: {self.slot_name}")

        # We are connected to the server but aren't assigned to a slot yet
        # Make a ConnectPacket and send it
        self.send_connect_packet()

    # Stops the socket thread and disconnects the connection
    def stop(self):
        # If there is a socket connection, break it
        if self.socket:
            self.socket.close()
            self.socket = None
            self.state = APClientEnums.DISCONNECTED
        self.ignore(self.__get_packet_handle_event_name())

    # Parses a url given (basically the archipelago server address)
    # Updates username, password, and port
    def parse_url(self, url: str):

        # Update the raw address given
        self.address = url

        # Try to extract the username password and port from this address
        address = f"ws://{self.address}" if "://" not in self.address \
            else self.address.replace("archipelago://", "ws://")

        server_url = urllib.parse.urlparse(address)

        new_username = ''
        new_password = ''
        if server_url.username:
            new_username = server_url.username
        if server_url.password:
            new_password = server_url.password

        use_default_port = False
        if not server_url.port:
            use_default_port = True

        self.update_identification(new_username, new_password)

        self.port = server_url.port or 38281

        port_component = ''
        if use_default_port:
            port_component = f':{self.port}'

        return f"{address}{port_component}"

    # Called via a new thread, responsible for instantiating a socket connection to the archipelago server
    # and receiving and handling incoming packets. Every 5 seconds we will perform a "kill" check to see
    # whether we should continue executing this thread
    # We should only kill this loop when either the toon logs out, or either endpoint loses internet connection
    # A toon should then be able to reconnect using !connect once more if the latter happens
    def __socket_thread(self):

        # Kill if we aren't disconnected
        if self.state != APClientEnums.DISCONNECTED:
            self.av.d_sendArchipelagoMessage("Attempted to start server client but one is already active!")
            return

        self.state = APClientEnums.CONNECTING
        self.av.d_sendArchipelagoMessage("[AP Client Thread] Starting server loop")

        # Parse the URL to the archipelago server, use whatever URL we defined previously
        try:
            address = self.parse_url(self.address)
        except ValueError as e:
            self.av.d_sendArchipelagoMessage(f"Error parsing url! {e}", color='red')
            return

        self.av.d_sendArchipelagoMessage(f"[AP Client Thread] Attempting connection with archipelago server at {address}...")

        # Attempt to connect to the server, if we get refused then !connect must be run to try again
        try:
            with connect(address, ssl_context=get_ssl_context() if address.startswith("wss://") else None) as socket:

                self.av.d_sendArchipelagoMessage(f"[AP Client Thread] Estabilished socket connection with archipelago server at {address}")
                self.socket = socket
                self.state = APClientEnums.CONNECTED

                # Attempt to forever read packets. Once the socket connection is closed, this loop and thread will term
                while True:
                    try:
                        # Read the raw data receieved, format is a string repr of a list of json objects
                        msg = socket.recv()
                        # Decode will flatten the msg into a list of raw json packets
                        for raw_packet in decode(msg):
                            messenger.send(self.__get_packet_handle_event_name(), sentArgs=[raw_packet], taskChain='default')

                    # We timeout when we have a timeout=x parameter set in recv(), usually we ignore
                    except TimeoutError:
                        pass  # Do nothing
                    # ConnectionClosed happens either when the server shuts down or when the toon logs out
                    except ConnectionClosed:
                        self.av.d_sendArchipelagoMessage("[AP Client Thread] Socket connection to archipelago server closed")
                        break

        # This will happen when we were given a bad archipelago server IP or when it just is not running
        except ConnectionRefusedError:
            self.av.d_sendArchipelagoMessage(f"[AP Client Thread] Socket connection to archipelago server {address} failed, either wrong address or server is not running")
        except gaierror:
            self.av.d_sendArchipelagoMessage(get_raw_formatted_string([MinimalJsonMessagePart(f"Server address {address} failed to parse! Please check the address given and try again.", color='red')]))
        except InvalidURI:
            self.av.d_sendArchipelagoMessage(get_raw_formatted_string([MinimalJsonMessagePart(f"Server address {address} is not a valid server.", color='red')]))
        except InvalidMessage or ConnectionError:
            self.av.d_sendArchipelagoMessage(get_raw_formatted_string([MinimalJsonMessagePart(f"Failed to connect to {address}.", color='red')]))

        except Exception as e:
            # Attempt encryption pass
            if address.startswith("ws://"):
                # try wss
                self.address = f"ws{address[1:]}"
                self.state = APClientEnums.DISCONNECTED
                self.__socket_thread()
                return

            self.av.d_sendArchipelagoMessage(get_raw_formatted_string([MinimalJsonMessagePart(f"Archipelago connection killed to prevent a district reset.", color='red')]))
            self.av.d_sendArchipelagoMessage(get_raw_formatted_string([MinimalJsonMessagePart(f"[SEVERE ERROR] Unhandled exception: {e}", color='red')]))
            self.av.d_sendArchipelagoMessage(get_raw_formatted_string([MinimalJsonMessagePart(f"Check district(ai) logs for full traceback.", color='red')]))
            self.av.d_sendArchipelagoMessage('You may use !connect to reconnect!')
            traceback.print_exc()

        if self.socket:
            self.socket.close()
            self.socket = None

        self.state = APClientEnums.DISCONNECTED
        # Ran out of data to send
        self.av.d_sendArchipelagoMessage("[AP Client Thread] Ran out of data to retrieve from server! Please use !connect to reconnect")
        self.av.d_sendArchipelagoMessage("[AP Client Thread] Terminating thread...")
        self.ignore(self.__get_packet_handle_event_name())

    def update_identification(self, slot_name: str = '', password: str = ''):

        if len(slot_name) > 0:
            self.slot_name = slot_name
            self.av.b_setName(slot_name)

        if len(password) > 0:
            self.password = password

        self.uuid = self.av.getUUID()  # todo make sure this is correct

    # Constructs a ConnectPacket to authenticate with the server
    def send_connect_packet(self):
        # When we are given this packet, we should connect this player to the server
        connect_packet = ConnectPacket()
        connect_packet.game = net_utils.ARCHIPELAGO_GAME_NAME
        connect_packet.name = self.slot_name
        connect_packet.password = self.password
        connect_packet.uuid = self.uuid
        connect_packet.version = net_utils.ARCHIPELAGO_CLIENT_VERSION
        connect_packet.items_handling = ConnectPacket.ITEMS_HANDLING_ALL_FLAGS
        connect_packet.tags = []
        connect_packet.slot_data = True
        self.send_packet(connect_packet)

    def handle_message_from_server(self, message):

        # self.notify.info(f"{message}")
        # Retrieve the type of packet receieved from the server
        packet_class = packet_registry.PACKET_CMD_TO_CLASS[message['cmd']]
        # Make sure we received a client packet
        assert packet_class.packet_type == ArchipelagoPacketBase.PacketType.CLIENT_BOUND
        # Instantiate the packet
        packet: ClientBoundPacketBase = packet_class(message)
        # Make sure it is valid
        assert packet.valid()

        # DEBUG
        self.__debug_dump_raw_packet_contents(packet.raw_data)

        # Handle the packet
        packet.handle(self)

    def __debug_dump_raw_packet_contents(self, json_data):
        import json
        from pathlib import Path
        Path(f'output/{json_data["cmd"]}').mkdir(parents=True, exist_ok=True)
        with open(f'output/{json_data["cmd"]}/{json_data["cmd"]}-{int(time.time())}.json', 'w') as f:
            json.dump(json_data, f, indent=4)

    def send_packet(self, packet: ServerBoundPacketBase):
        # Packets need to be in a list anyway so just call the other method and construct a list with the packet
        self.send_packets([packet])

    def send_packets(self, packets: List[ServerBoundPacketBase]):

        if self.state == APClientEnums.DISCONNECTED:
            self.av.d_sendArchipelagoMessage("You cannot send packets unless you are connected to archipelago!")
            return

        # Construct a list of built packets and send them using the json encoder
        raw_packets = []
        for packet in packets:
            raw_packets.append(packet.build())
            packet.debug(f"Sending packet to server: {packet}")

        try:
            self.socket.send(encode(raw_packets))
        except Exception as e:
            self.av.d_sendArchipelagoMessage(f"Failed to communicate with the server ({e})")
            traceback.print_exc()

    def get_item_info(self, item_id):
        return self.global_data_package.id_to_item_name.get(int(item_id), f'Unknown Item[{item_id}]')

    def get_location_info(self, location_id):
        return self.global_data_package.id_to_location_name.get(int(location_id), f'Unknown Location[{location_id}]')

    def set_connect_url(self, server_url: str):
        self.address = server_url

    # Caches an item ID at some location. We do all the conversion in this method necessary to store it how we please
    # our_location_id: The location that we own, that stores some item
    # owning_player_id: The ID of the player that owns the item stored at the location
    # item_id: The ID of the item
    def cache_location_and_item(self, our_location_id: int, owning_player_id: int, item_id: int, item_flag: int = 0):

        # Stolen from the JSON parser

        someone_elses = owning_player_id != self.slot

        owner_name = self.get_slot_info(owning_player_id).name + "'s " if someone_elses else "Your "
        item_name = self.get_item_info(item_id)

        # Let's make the string pretty
        name_color = 'green' if someone_elses else 'magenta'
        item_color = item_flag_to_color(item_flag)
        item_display_string = global_text_properties.get_raw_formatted_string([
            MinimalJsonMessagePart("AP Reward: ", color='salmon'),
            MinimalJsonMessagePart(owner_name, color=name_color),
            MinimalJsonMessagePart(item_name, color=item_color)
        ])

        self.location_scouts_cache.put(our_location_id, item_display_string)
