from typing import List

from toontown.archipelago.definitions.rewards import APReward, get_ap_reward_from_id
from toontown.archipelago.net_utils import NetworkItem
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
        for item in self.items:
            ap_reward: APReward = get_ap_reward_from_id(item.item)
            ap_reward.apply(client.av)
            print(f"[AP Client] Received item {client.get_item_info(item.item)} from {client.get_slot_info(item.player).name}")
