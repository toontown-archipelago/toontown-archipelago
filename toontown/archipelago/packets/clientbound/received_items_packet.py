from typing import List, Tuple

from toontown.archipelago.definitions.rewards import APReward, get_ap_reward_from_id, EarnedAPReward
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
        items_received: List[Tuple[int, int]] = client.av.getReceivedItems().copy()
        for item in items_received:
            index_received, item_id = item
            av_indeces_already_received.append(index_received)

        new_items: List[Tuple[int, int]] = []

        reward_index = self.index
        for item in self.items:

            # Have we already received the index of this reward?
            not_applied_yet = reward_index not in av_indeces_already_received

            # If we need to apply it go ahead and keep track on the toon that we applied this specific reward
            if not_applied_yet:
                itemName = client.get_item_info(item.item)
                fromName = client.get_slot_info(item.player).name
                ap_reward_definition: APReward = get_ap_reward_from_id(item.item)
                reward: EarnedAPReward = EarnedAPReward(client.av, ap_reward_definition, reward_index, item.item, fromName, item.player == client.slot)
                client.av.queueAPReward(reward)
                new_items.append((reward_index, item.item))
                self.debug(f"Queued {itemName} from {fromName}")

            # Incrememnt the reward index and go to the next one
            reward_index += 1

        # Now perform an update on the items that this av has received
        items_received.extend(new_items)
        client.av.b_setReceivedItems(items_received)

