from typing import List

from toontown.archipelago.definitions.rewards import APReward, get_ap_reward_from_id
from toontown.archipelago.util.net_utils import NetworkItem
from toontown.archipelago.packets.clientbound.clientbound_packet_base import ClientBoundPacketBase


# Sent to clients when they receive an item.
class ReceivedItemsPacket(ClientBoundPacketBase):

    def __init__(self, json_data):
        super().__init__(json_data)

        # The next empty slot in the list of items for the receiving client.
        self.index: int = json_data['index']

        # The items which the client is receiving.
        self.items: List[NetworkItem] = json_data['items']

    def handle(self, client):

        reward_index = self.index
        for item in self.items:

            # Have we already received the index of this reward?
            not_applied_yet = reward_index not in client.av.getReceivedItems()

            # If we need to apply it go ahead and keep track on the toon that we applied this specific reward
            if not_applied_yet:
                ap_reward: APReward = get_ap_reward_from_id(item.item)
                ap_reward.apply(client.av)
                client.av.addReceivedItem(item.item)
                self.debug(f"Received item {client.get_item_info(item.item)} from {client.get_slot_info(item.player).name}")

            # Incrememnt the reward index and go to the next one
            reward_index += 1
