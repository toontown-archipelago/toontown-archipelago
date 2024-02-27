import ssl
import time
import traceback

import urllib.parse
from direct.stdpy import threading
from typing import List, Dict, Union

import certifi
from websockets import ConnectionClosed
from websockets.sync.client import connect, ClientConnection

from toontown.archipelago.apclient.ap_client_enums import APClientEnums
from toontown.archipelago.util import net_utils
from toontown.archipelago.util.data_package import DataPackage
from toontown.archipelago.util.net_utils import encode, decode, NetworkSlot
from toontown.archipelago.packets import packet_registry
from toontown.archipelago.packets.archipelago_packet_base import ArchipelagoPacketBase
from toontown.archipelago.packets.clientbound.clientbound_packet_base import ClientBoundPacketBase
from toontown.archipelago.packets.serverbound.connect_packet import ConnectPacket
from toontown.archipelago.packets.serverbound.serverbound_packet_base import ServerBoundPacketBase
from toontown.archipelago.util.utils import cache_argsless

# TODO find dynamic way to do this
ARCHIPELAGO_SERVER_ADDRESS = "localhost"
PORT = 38281


@cache_argsless
def get_ssl_context():
    return ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=certifi.where())


# Class to handle sending and receiving packets through a socket estabilished via the archipelago server
class ArchipelagoClient:

    def __init__(self, av, slot_name: str, password: str = ''):

        self.state = APClientEnums.DISCONNECTED

        # Address to connect to (IP of archipelago server)
        self.address: str = f"{ARCHIPELAGO_SERVER_ADDRESS}:{PORT}"
        # Socket interface of the archipelago server
        self.socket: ClientConnection = None

        # Store some identification
        self.av = av  # DistributedToonAI that owns this client
        self.slot_name: str = slot_name  # slot assigned for seed generation
        self.slot: int = -1  # Our slot ID given when we connect
        self.uuid: str = ''  # not sure how important this is atm but just generating something in udpate_id method
        self.password: str = password  # password if required

        # Actually defines correct values for variables above
        self.update_identification(slot_name, password)

        # Store information for retrieval later that we received from packets
        self.slot_id_to_slot_name: Dict[int, NetworkSlot] = {}
        self.data_packages: Dict[str, DataPackage] = {}
        self.global_data_package: DataPackage = DataPackage()

    # Given a slot number (as string or int, doesn't matter but must be a number) return the NetworkSlot as cached
    def get_slot_info(self, slot: Union[str, int]) -> NetworkSlot:
        return self.slot_id_to_slot_name[int(slot)]

    # Returns the local slot ID (int) that this client belongs to
    def get_local_slot(self) -> int:
        return self.slot

    # Given the ID of an item, find a display name for the item using our data package
    def get_item_name(self, item_id: Union[str, int]) -> str:
        return self.global_data_package.get_item_from_id(item_id)

    # Given the ID of location, find a display name for the location using our data package
    def get_location_name(self, location_id: Union[str, int]) -> str:
        return self.global_data_package.get_location_from_id(location_id)

    # Starts up the socket thread
    def start(self):

        # If we are not disconnected we aren't allowed to do this
        if self.state != APClientEnums.DISCONNECTED:
            raise Exception("You are already connected!")

        # Run the socket thread and let it do whatever
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
        self.av.d_sendArchipelagoMessage("[AP Client] Starting server loop")

        # Parse the URL to the archipelago server
        address = f"ws://{self.address}" if "://" not in self.address \
            else self.address.replace("archipelago://", "ws://")
        server_url = urllib.parse.urlparse(address)
        if server_url.username:
            self.username = server_url.username
        if server_url.password:
            self.password = server_url.password
        port = server_url.port or 38281

        # Attempt to connect to the server, if we get refused then !connect must be run to try again
        try:
            with connect(address, ssl_context=get_ssl_context() if address.startswith("wss://") else None) as socket:

                self.av.d_sendArchipelagoMessage(f"[AP Client] Estabilished socket connection with archipelago server at {address}")
                self.socket = socket
                self.state = APClientEnums.CONNECTED

                # Attempt to forever read packets. Once the socket connection is closed, this loop and thread will term
                while True:
                    try:
                        # Read the raw data receieved, format is a string repr of a list of json objects
                        msg = socket.recv()
                        # Decode will flatten the msg into a list of raw json packets
                        for raw_packet in decode(msg):
                            self.handle_message_from_server(raw_packet)

                    # We timeout when we have a timeout=x parameter set in recv(), usually we ignore
                    except TimeoutError:
                        pass  # Do nothing
                    # ConnectionClosed happens either when the server shuts down or when the toon logs out
                    except ConnectionClosed:
                        self.av.d_sendArchipelagoMessage("[AP Client] Socket connection to archipelago server closed")
                        break

        # This will happen when we were given a bad archipelago server IP or when it just is not running
        except ConnectionRefusedError:
            self.av.d_sendArchipelagoMessage(f"[AP Client] Socket connection to archipelago server {address} failed, either wrong address or server is not running")
        except Exception as e:
            self.av.d_sendArchipelagoMessage(f"[AP Client] Unhandled exception {e}, disconnecting from Archipelago server")

        if self.socket:
            self.socket.close()
            self.socket = None

        self.state = APClientEnums.DISCONNECTED
        # Ran out of data to send
        self.av.d_sendArchipelagoMessage("[AP Client] Ran out of data to retrieve from server! Please use !connect to reconnect")

    def update_identification(self, slot_name: str, password: str = ''):
        self.slot_name = slot_name
        self.av.b_setName(slot_name)
        self.uuid = f"toontown-player-{slot_name}"  # todo make sure this is correct
        self.password = password

    # Constructs a ConnectPacket to authenticate with the server
    def send_connect_packet(self):
        # When we are given this packet, we should connect this player to the server
        connect_packet = ConnectPacket()
        connect_packet.game = net_utils.ARCHIPELAGO_GAME_NAME
        connect_packet.name = self.slot_name
        connect_packet.uuid = self.uuid
        connect_packet.version = net_utils.ARCHIPELAGO_CLIENT_VERSION
        connect_packet.items_handling = ConnectPacket.ITEMS_HANDLING_ALL_FLAGS
        connect_packet.tags = [ConnectPacket.TAG_AP]  # todo add support for deathlink
        connect_packet.slot_data = True
        self.send_packet(connect_packet)

    def handle_message_from_server(self, message):

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
            packet.debug(f"[AP Client] Sending packet to server: {packet}")

        try:
            self.socket.send(encode(raw_packets))
        except Exception as e:
            self.av.d_sendArchipelagoMessage(f"Failed to communicate with the server ({e})")
            traceback.print_exc()

    def get_item_info(self, item_id):
        return self.global_data_package.id_to_item_name.get(int(item_id), f'Unknown Item[{item_id}]')

    def get_location_info(self, location_id):
        return self.global_data_package.id_to_location_name.get(int(location_id), f'Unknown Location[{location_id}]')
