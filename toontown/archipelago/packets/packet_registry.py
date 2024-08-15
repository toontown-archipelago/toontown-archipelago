from toontown.archipelago.packets.clientbound.bounced_packet import BouncedPacket
from toontown.archipelago.packets.clientbound.connected_packet import ConnectedPacket
from toontown.archipelago.packets.clientbound.connection_refused_packet import ConnectionRefusedPacket
from toontown.archipelago.packets.clientbound.data_package_packet import DataPackagePacket
from toontown.archipelago.packets.clientbound.invalid_packet import InvalidPacket
from toontown.archipelago.packets.clientbound.location_info_packet import LocationInfoPacket
from toontown.archipelago.packets.clientbound.print_json_packet import PrintJSONPacket
from toontown.archipelago.packets.clientbound.received_items_packet import ReceivedItemsPacket
from toontown.archipelago.packets.clientbound.retrieved_packet import RetrievedPacket
from toontown.archipelago.packets.clientbound.room_info_packet import RoomInfoPacket
from toontown.archipelago.packets.clientbound.room_update_packet import RoomUpdatePacket
from toontown.archipelago.packets.clientbound.set_reply_packet import SetReplyPacket
from toontown.archipelago.packets.serverbound.bounce_packet import BouncePacket
from toontown.archipelago.packets.serverbound.connect_packet import ConnectPacket
from toontown.archipelago.packets.serverbound.connect_update_packet import ConnectUpdatePacket
from toontown.archipelago.packets.serverbound.get_data_package_packet import GetDataPackagePacket
from toontown.archipelago.packets.serverbound.get_packet import GetPacket
from toontown.archipelago.packets.serverbound.location_checks_packet import LocationChecksPacket
from toontown.archipelago.packets.serverbound.location_scouts_packet import LocationScoutsPacket
from toontown.archipelago.packets.serverbound.say_packet import SayPacket
from toontown.archipelago.packets.serverbound.set_notify_packet import SetNotifyPacket
from toontown.archipelago.packets.serverbound.set_packet import SetPacket
from toontown.archipelago.packets.serverbound.status_update_packet import StatusUpdatePacket
from toontown.archipelago.packets.serverbound.sync_packet import SyncPacket

PACKET_CMD_TO_CLASS = {

    # Server -> Client packets
    'RoomInfo': RoomInfoPacket,
    'ConnectionRefused': ConnectionRefusedPacket,
    'Connected': ConnectedPacket,
    'ReceivedItems': ReceivedItemsPacket,
    'LocationInfo': LocationInfoPacket,
    'RoomUpdate': RoomUpdatePacket,
    'PrintJSON': PrintJSONPacket,
    'DataPackage': DataPackagePacket,
    'Bounced': BouncedPacket,
    'InvalidPacket': InvalidPacket,
    'Retrieved': RetrievedPacket,
    'SetReply': SetReplyPacket,

    # Client -> Server packets
    'Connect': ConnectPacket,
    'ConnectUpdate': ConnectUpdatePacket,
    'Sync': SyncPacket,
    'LocationChecks': LocationChecksPacket,
    'LocationScouts': LocationScoutsPacket,
    'StatusUpdate': StatusUpdatePacket,
    'Say': SayPacket,
    'GetDataPackage': GetDataPackagePacket,
    'Bounce': BouncePacket,
    'Get': GetPacket,
    'Set': SetPacket,
    'SetNotify': SetNotifyPacket,
}
