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

        av_indeces_already_received = []
        for item in client.av.getReceivedItems():
            index_received, item_id = item
            av_indeces_already_received.append(index_received)

        reward_index = self.index
        for item in self.items:

            # Have we already received the index of this reward?
            not_applied_yet = reward_index not in av_indeces_already_received

            # If we need to apply it go ahead and keep track on the toon that we applied this specific reward
            if not_applied_yet:
                itemName = client.get_item_info(item.item)
                fromName = client.get_slot_info(item.player).name
                ap_reward: APReward = get_ap_reward_from_id(item.item)
                ap_reward.apply(client.av)
                client.av.addReceivedItem(reward_index, item.item)
                client.av.d_showReward(item.item, fromName, item.player == client.slot)
                self.debug(f"Received item {itemName} from {fromName}")

            # Incrememnt the reward index and go to the next one
            reward_index += 1
