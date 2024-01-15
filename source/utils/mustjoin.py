from pyrogram import Client
from pyrogram.errors import FloodWait, ChatAdminRequired, PeerIdInvalid
import asyncio
import logging

logger = logging.getLogger(__name__)

async def is_user_member(client: Client, user_id: int, channel: str) -> bool:
    """
    Checks if the user is a member of the specified channel.
    """
    try:
        member = await client.get_chat_member(channel, user_id)
        return member.status not in ["left", "kicked"]
    except PeerIdInvalid:
        logger.error("Channel or User ID is invalid.")
        return False
    except ChatAdminRequired:
        logger.error("Bot must be an admin in the channel.")
        return False
    except FloodWait as e:
        logger.error(f"Flood wait error: sleeping for {e.x} seconds.")
        await asyncio.sleep(e.x)
        return False
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return False
