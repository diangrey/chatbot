import random
from Abg.chat_status import adminsOnly

from pymongo import MongoClient
from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from pyrogram.types import InlineKeyboardMarkup, Message

from config import MONGO_URL
from Radhe import Radhe
from Radhe.modules.helpers import CHATBOT_ON, is_admins


@Radhe.on_cmd("chatbot", group_only=True)
@adminsOnly("can_delete_messages")
async def chaton_(_, m: Message):
    await m.reply_text(
        f"ᴄʜᴀᴛ: {m.chat.title}\n**ᴄʜᴏᴏsᴇ ᴀɴ ᴏᴩᴛɪᴏɴ ᴛᴏ ᴇɴᴀʙʟᴇ/ᴅɪsᴀʙʟᴇ ᴄʜᴀᴛʙᴏᴛ.**",
        reply_markup=InlineKeyboardMarkup(CHATBOT_ON),
    )


@Radhe.on_message(
    (filters.text | filters.sticker | filters.group) & ~filters.private & ~filters.bot,
    group=4,
)
async def chatbot_text(client: Client, message: Message):
    try:
        if message.text.startswith(("!", "/", "?", "@", "#")):
            return
    except Exception:
        pass

    chatdb = MongoClient(MONGO_URL)
    chatai = chatdb["Word"]["WordDb"]

    RADHEdb = MongoClient(MONGO_URL)
    RADHE = RADHEdb["RADHEDb"]["RADHE"]
    is_RADHE = RADHE.find_one({"chat_id": message.chat.id})

    if not message.reply_to_message and not is_RADHE:
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)
        data = list(chatai.find({"word": message.text}))
        if data:
            pick = random.choice(data)
            if pick["check"] == "sticker":
                await message.reply_sticker(pick["text"])
            else:
                await message.reply_text(pick["text"])

    if message.reply_to_message and message.reply_to_message.from_user.id == client.id and not is_RADHE:
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)
        data = list(chatai.find({"word": message.text}))
        if data:
            pick = random.choice(data)
            if pick["check"] == "sticker":
                await message.reply_sticker(pick["text"])
            else:
                await message.reply_text(pick["text"])

    if message.reply_to_message and message.reply_to_message.from_user.id != client.id:
        if message.sticker:
            if not chatai.find_one(
                {
                    "word": message.reply_to_message.text,
                    "id": message.sticker.file_unique_id,
                }
            ):
                chatai.insert_one(
                    {
                        "word": message.reply_to_message.text,
                        "text": message.sticker.file_id,
                        "check": "sticker",
                        "id": message.sticker.file_unique_id,
                    }
                )
        if message.text:
            if not chatai.find_one(
                {"word": message.reply_to_message.text, "text": message.text}
            ):
                chatai.insert_one(
                    {
                        "word": message.reply_to_message.text,
                        "text": message.text,
                        "check": "none",
                    }
                )


@Radhe.on_message(
    (filters.sticker | filters.group | filters.text) & ~filters.private & ~filters.bot,
    group=4,
)
async def chatbot_sticker(client: Client, message: Message):
    try:
        if message.text.startswith(("!", "/", "?", "@", "#")):
            return
    except Exception:
        pass

    chatdb = MongoClient(MONGO_URL)
    chatai = chatdb["Word"]["WordDb"]

    RADHEdb = MongoClient(MONGO_URL)
    RADHE = RADHEdb["RADHEDb"]["RADHE"]
    is_RADHE = RADHE.find_one({"chat_id": message.chat.id})

    if not message.reply_to_message and not is_RADHE:
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)
        data = list(chatai.find({"word": message.sticker.file_unique_id}))
        if data:
            pick = random.choice(data)
            if pick["check"] == "text":
                await message.reply_text(pick["text"])
            else:
                await message.reply_sticker(pick["text"])


@Radhe.on_message(
    (filters.text | filters.sticker | filters.group) & ~filters.private & ~filters.bot,
    group=4,
)
async def chatbot_pvt(client: Client, message: Message):
    try:
        if message.text.startswith(("!", "/", "?", "@", "#")):
            return
    except Exception:
        pass

    chatdb = MongoClient(MONGO_URL)
    chatai = chatdb["Word"]["WordDb"]

    await client.send_chat_action(message.chat.id, ChatAction.TYPING)
    data = list(chatai.find({"word": message.text}))
    if data:
        pick = random.choice(data)
        if pick["check"] == "sticker":
            await message.reply_sticker(pick["text"])
        else:
            await message.reply_text(pick["text"])


@Radhe.on_message(
    (filters.sticker | filters.group) & ~filters.private & ~filters.bot,
    group=4,
)
async def chatbot_sticker_pvt(client: Client, message: Message):
    chatdb = MongoClient(MONGO_URL)
    chatai = chatdb["Word"]["WordDb"]

    await client.send_chat_action(message.chat.id, ChatAction.TYPING)
    data = list(chatai.find({"word": message.sticker.file_unique_id}))
    if data:
        pick = random.choice(data)
        if pick["check"] == "text":
            await message.reply_text(pick["text"])
        else:
            await message.reply_sticker(pick["text"])
