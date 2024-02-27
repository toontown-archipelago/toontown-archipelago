import asyncio
from asyncio import CancelledError

from toontown.archipelago.apclient.archipelago_client import ArchipelagoClient

SLOT_NAME = 'devvydontTT'
PASSWORD = 'aaaaaaaaaaaaa'


async def run_client():

    client = ArchipelagoClient(SLOT_NAME, password=PASSWORD)

    # Now we can do things like await client.send_message() whenever needed




    try:
        await asyncio.gather(client.server_task)
    except CancelledError:
        print("Background tasks canceled")

if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(run_client())
    except KeyboardInterrupt:
        print("Aborting...")

    input("Press ENTER to exit")
