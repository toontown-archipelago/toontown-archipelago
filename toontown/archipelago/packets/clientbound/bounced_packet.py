from typing import List, Dict, Any

from toontown.archipelago.packets.serverbound.bounce_packet import BouncePacket
from toontown.archipelago.definitions.death_reason import DeathReason
from toontown.archipelago.packets.clientbound.clientbound_packet_base import ClientBoundPacketBase
from toontown.archipelago.packets.serverbound.connect_packet import ConnectPacket
from toontown.archipelago.util import global_text_properties
from toontown.archipelago.util.global_text_properties import MinimalJsonMessagePart


# Sent to clients after a client requested this message be sent to them, more info in the Bounce package.
class BouncedPacket(ClientBoundPacketBase):

    def __init__(self, json_data):
        super().__init__(json_data)

        # Optional. Game names this message is targeting
        self.games: List[str] = self.read_raw_field("games", ignore_missing=True)

        # Optional. Player slot IDs that this message is targeting
        self.slots: List[int] = self.read_raw_field('slots', ignore_missing=True)

        # Optional. Client Tags this message is targeting
        self.tags: List[str] = self.read_raw_field('tags', ignore_missing=True)

        # The data in the Bounce package copied
        self.data: Dict[Any, Any] = self.read_raw_field('data', ignore_missing=True)

    # Used to check if a received DeathLink Bounced packet was caused by us.
    # Check BouncePacket.add_deathlink_data() (self.data['source']) to see what you're supposed to check
    # to prevent infinite deathlink packets
    def caused_by_toon(self, toon) -> bool:
        # Check the source of the deathlink, if there was a toon ID match then this toon caused the deathlink
        return self.data.get('source') == toon.getUUID()

    # Helper method to handle the packet if this is a deathlink packet
    def handle_deathlink(self, client):

        self.debug("Received deathlink packet")

        # At this point we are assuming that this packet IS a deathlink packet and that our client has it enabled.
        timestamp = self.data['time']
        cause: str = self.data.get("cause")
        source: str = self.data['source']
        toon = client.av

        # All checks passed, kill the toon
        self.debug("Killing toon via deathlink.")
        toon.setDeathReason(DeathReason.DEATHLINK)
        toon.takeDamage(toon.getMaxHp())
        toon.d_broadcastHpString("DEATHLINKED!", (.8, .35, .35))
        toon.d_setAnimState("Died", 1)

        death_component = cause if cause is not None else f"{source} died!"
        msg = global_text_properties.get_raw_formatted_string([
            MinimalJsonMessagePart("[DeathLink] ", color='red'),
            MinimalJsonMessagePart("You went sad because "),
            MinimalJsonMessagePart(f"{death_component}", color='salmon')
        ])
        toon.d_sendArchipelagoMessage(msg)


    def handle(self, client):
        self.debug("Handling packet")

        # Had a weird crash in the caused_by_toon check of self.data being NoneType, while connected alone. Who's sending empty bounce packets?
        if not isinstance(self.data, dict):
            self.debug("BouncePacket Recieved seems to be empty. Ignoring.")
            return

        if self.caused_by_toon(client.av):
            self.debug("Packet seems to have been sent by us. Skip handling this packet")
            return

        # Is this a deathlink packet?
        if isinstance(self.tags, list) and ConnectPacket.TAG_DEATHLINK in self.tags:
            self.handle_deathlink(client)
            return
