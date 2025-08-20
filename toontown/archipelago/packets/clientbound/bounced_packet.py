import math
from typing import List, Dict, Any

from toontown.archipelago.packets.serverbound.bounce_packet import BouncePacket
from toontown.archipelago.definitions.death_reason import DeathReason
from toontown.archipelago.packets.clientbound.clientbound_packet_base import ClientBoundPacketBase
from toontown.archipelago.packets.serverbound.connect_packet import ConnectPacket
from toontown.archipelago.util import global_text_properties
from toontown.archipelago.util.global_text_properties import MinimalJsonMessagePart
from apworld.toontown.options import DeathLinkOption


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
    def caused_by_toon(self, source, toon) -> bool:
        # Check the source of the deathlink, if there was a toon ID match then this toon caused the deathlink
        return source == toon

    # Helper method to handle the packet if this is a deathlink packet
    def handle_deathlink(self, client):

        self.debug("Received deathlink packet")

        # At this point we are assuming that this packet IS a deathlink packet and that our client has it enabled.
        timestamp = self.data['time']
        cause: str = self.data.get("cause")
        source: str = self.data['source']
        toon = client.av
        toonId = str(abs(int(hash(toon.getUUID()) / 10000000000)))

        # If our source is the same as the UUID eval, stop
        if self.caused_by_toon(source, toonId):
            return

        # All checks passed, kill the toon
        self.debug("Killing toon via deathlink.")
        deathLinkOption = toon.slotData.get('death_link', DeathLinkOption.option_off)
        if deathLinkOption in [DeathLinkOption.option_full, DeathLinkOption.option_one]:
            toon.setDeathReason(DeathReason.DEATHLINK)
            toon.d_broadcastHpString("DEATHLINKED!", (.8, .35, .35))
            if deathLinkOption == DeathLinkOption.option_full:
                toon.takeDamage(toon.getMaxHp())
                toon.d_setAnimState("Died", 1)
                death_component = cause if cause is not None else f"{source} died!"
                msg = global_text_properties.get_raw_formatted_string([
                    MinimalJsonMessagePart("[DeathLink] ", color='red'),
                    MinimalJsonMessagePart("You went sad because "),
                    MinimalJsonMessagePart(f"{death_component}", color='salmon')
                ])
            elif deathLinkOption == DeathLinkOption.option_one:
                toon.takeDamage((toon.getHp() - 1))
                death_component = cause if cause is not None else f"{source} died!"
                msg = global_text_properties.get_raw_formatted_string([
                    MinimalJsonMessagePart("[DeathLink] ", color='red'),
                    MinimalJsonMessagePart("You're nearing sadness because "),
                    MinimalJsonMessagePart(f"{death_component}", color='salmon')
                ])
        elif deathLinkOption == DeathLinkOption.option_drain:
            toon.d_broadcastHpString("DEATHLINKED!", (.8, .35, .35))
            death_component = cause if cause is not None else f"{source} died!"
            msg = global_text_properties.get_raw_formatted_string([
                MinimalJsonMessagePart("[DeathLink] ", color='red'),
                MinimalJsonMessagePart("You feel your happiness draining because "),
                MinimalJsonMessagePart(f"{death_component}", color='salmon')
            ])
            self.hpToDrain = toon.getHp()
            self.drainRate = 0.33
            # We'll take 0.01 seconds off each tick for each 10 laff we are going to drain
            rateToRemove = 0.015 * (self.hpToDrain/10)
            self.drainRate = max(0.01, (0.33 - rateToRemove))
            taskMgr.doMethodLater(self.drainRate, self.handle_link_drain, toonId + '-deathlink-drainTick', extraArgs=[toon, toonId])
        else:
            # This should not happen! But just in case.
            msg = global_text_properties.get_raw_formatted_string([
                MinimalJsonMessagePart("[DeathLink] ", color='red'),
                MinimalJsonMessagePart("You went sad for mysterious reasons."),
            ])
        toon.d_sendArchipelagoMessage(msg)

    def handle_link_drain(self, toon, toonId):
        # This tick is killing the toon, set the death reason to not kill others and break the loop
        if toon.getHp() == 1:
            toon.setDeathReason(DeathReason.DEATHLINK)
        toon.takeDamage(1)
        self.hpToDrain -= 1
        if toon.getHp() > 0 and self.hpToDrain > 0:
            taskMgr.doMethodLater(self.drainRate, self.handle_link_drain, toonId + '-deathlink-drainTick', extraArgs=[toon, toonId])

    def handle_ringlink(self, client):
        self.debug("Received ringlink packet")

        # At this point we are assuming that this packet IS a ringlink packet and that our client has it enabled.
        timestamp = self.data['time']
        amount: int = self.data.get("amount", 0)
        source: str = self.data["source"]
        toon = client.av
        toonId = abs(int(hash(toon.getUUID()) / 10000000000))

        # If our source is the same as the UUID eval, stop
        if self.caused_by_toon(source, toonId):
            return

        # All checks passed, change the currency.
        self.debug("Changing beans via ringlink.")
        if amount >= 0:
            toon.addMoney(amount, isLocalChange=False)
        else:
            toon.takeMoney((amount*-1), isLocalChange=False)

    def handle(self, client):
        self.debug("Handling packet")

        # Had a weird crash in the caused_by_toon check of self.data being NoneType, while connected alone. Who's sending empty bounce packets?
        if not isinstance(self.data, dict):
            self.debug("BouncePacket Recieved seems to be empty. Ignoring.")
            return

        # Is this a deathlink packet?
        if isinstance(self.tags, list) and ConnectPacket.TAG_DEATHLINK in self.tags:
            self.handle_deathlink(client)
            return

        # Is this a ringlink packet?
        if isinstance(self.tags, list) and ConnectPacket.TAG_RINGLINK in self.tags:
            self.handle_ringlink(client)
            return
