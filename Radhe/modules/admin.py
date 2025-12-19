from pyrogram import filters
from pyrogram.types import Message, ChatPermissions
from pyrogram.enums import ChatMemberStatus
from Radhe import Radhe

# =========================
# Allowed user check
# =========================
ALLOWED_USER = 1999645649  # sirf ye user commands use kar sakta hai

def is_allowed_user(user_id: int):
    return user_id == ALLOWED_USER

# =========================
# Helper: get target user
# =========================
def get_target_user(message: Message):
    if message.reply_to_message:
        return message.reply_to_message.from_user.id
    if len(message.command) > 1:
        try:
            return int(message.command[1])
        except ValueError:
            return None
    return None

# =========================
# Prefix filter: Radhe <command>
# =========================
def radhe_command(cmd_name):
    return filters.text & filters.regex(rf"(?i)^Radhe {cmd_name}$")

# =========================
# Ban command
# =========================
@Radhe.on_message(radhe_command("ban") & filters.group)
async def ban_user(_, message: Message):
    if not is_allowed_user(message.from_user.id):
        return await message.reply("😏 **ʏσυ ¢αη'τ υѕє τнιѕ ¢σммαη∂**")
    user_id = get_target_user(message)
    if not user_id:
        return await message.reply("**❌ яєρℓу τσ α υѕєя σя gιvє υѕєяι∂/υѕєяηαмє**")
    try:
        await message.chat.ban_member(user_id)
        await message.reply("🚫 **υѕєя вαηηє∂ ѕυccєѕѕƒυℓℓγ**")
    except Exception as e:
        await message.reply(f"❌ Error:\n`{e}`")

# =========================
# Unban command
# =========================
@Radhe.on_message(radhe_command("unban") & filters.group)
async def unban_user(_, message: Message):
    if not is_allowed_user(message.from_user.id):
        return await message.reply("😏 **ʏσυ ¢αη'τ υѕє τнιѕ ¢σммαη∂**")
    user_id = get_target_user(message)
    if not user_id:
        return await message.reply("**❌ яєρℓу τσ α υѕєя σя gιvє υѕєяι∂/υѕєяηαмє**")
    try:
        await message.chat.unban_member(user_id)
        await message.reply("✅ **υѕєя υηвαηηє∂ ѕυccєѕѕƒυℓℓγ**")
    except Exception as e:
        await message.reply(f"❌ Error:\n`{e}`")

# =========================
# Mute command
# =========================
@Radhe.on_message(radhe_command("mute") & filters.group)
async def mute_user(_, message: Message):
    if not is_allowed_user(message.from_user.id):
        return await message.reply("😏 **ʏσυ ¢αη'τ υѕє τнιѕ ¢σммαη∂**")
    user_id = get_target_user(message)
    if not user_id:
        return await message.reply("❌ **яєρℓу τσ α υѕєя σя gιvє υѕєяι∂/υѕєяηαмє**")
    try:
        await message.chat.restrict_member(user_id, ChatPermissions())
        await message.reply("🔇 **υѕєя мυтє∂ ѕυccєѕѕƒυℓℓγ**")
    except Exception as e:
        await message.reply(f"❌ Error:\n`{e}`")

# =========================
# Unmute command
# =========================
@Radhe.on_message(radhe_command("unmute") & filters.group)
async def unmute_user(_, message: Message):
    if not is_allowed_user(message.from_user.id):
        return await message.reply("😏 **ʏσυ ¢αη'τ υѕє τнιѕ ¢σммαη∂**")
    user_id = get_target_user(message)
    if not user_id:
        return await message.reply("❌ **яєρℓу τσ α υѕєя σя gιvє υѕєяι∂/υѕєяηαмє**")
    try:
        await message.chat.restrict_member(
            user_id,
            ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
        )
        await message.reply("🔊 **υѕєя υηмυтє∂ ѕυccєѕѕƒυℓℓγ**")
    except Exception as e:
        await message.reply(f"🥺 Error:\n`{e}`")

# =========================
# Promote command
# =========================
@Radhe.on_message(radhe_command("promote") & filters.group)
async def promote_user(_, message: Message):
    if not is_allowed_user(message.from_user.id):
        return await message.reply("😏 **ʏσυ ¢αη'τ υѕє τнιѕ ¢σммαη∂**")
    user_id = get_target_user(message)
    if not user_id:
        return await message.reply("👀 **яєρℓу τσ α υѕєя σя gιvє υѕєяι∂/υѕєяηαмє**")
    try:
        await message.chat.promote_member(
            user_id,
            can_change_info=True,
            can_delete_messages=True,
            can_invite_users=True,
            can_restrict_members=True,
            can_pin_messages=True,
            can_manage_chat=True
        )
        await message.reply("⭐ **υѕєя ρяσмσтє∂ ѕυccєѕѕƒυℓℓγ**")
    except Exception as e:
        await message.reply(f"❌ `{e}`")

# =========================
# Demote command
# =========================
@Radhe.on_message(radhe_command("demote") & filters.group)
async def demote_user(_, message: Message):
    if not is_allowed_user(message.from_user.id):
        return await message.reply("😏 **ʏσυ ¢αη'τ υѕє τнιѕ ¢σммαη∂**")
    user_id = get_target_user(message)
    if not user_id:
        return await message.reply("👀 **яєρℓу τσ α υѕєя σя gιvє υѕєяι∂/υѕєяηαмє**")
    try:
        await message.chat.promote_member(
            user_id,
            can_change_info=False,
            can_delete_messages=False,
            can_invite_users=False,
            can_restrict_members=False,
            can_pin_messages=False,
            can_manage_chat=False
        )
        await message.reply("👀 **υѕєя ∂ємσтє∂ ѕυccєѕѕƒυℓℓγ**")
    except Exception as e:
        await message.reply(f"❌ `{e}`")

# =========================
# Kick command
# =========================
@Radhe.on_message(radhe_command("kick") & filters.group)
async def kick_user(_, message: Message):
    if not is_allowed_user(message.from_user.id):
        return await message.reply("😏 **ʏσυ ¢αη'τ υѕє τнιѕ ¢σммαη∂**")
    user_id = get_target_user(message)
    if not user_id:
        return await message.reply("👀 **яєρℓу τσ α υѕєя σя gιvє υѕєяι∂/υѕєяηαмє**")
    try:
        await message.chat.unban_member(user_id)  # kick ke liye temporarily ban & unban
        await message.reply("👢 **υѕєя кιcкє∂ ѕυccєѕѕƒυℓℓγ**")
    except Exception as e:
        await message.reply(f"❌ `{e}`")

# =========================
# Pin command
# =========================
@Radhe.on_message(radhe_command("pin") & filters.group)
async def pin_message(_, message: Message):
    if not is_allowed_user(message.from_user.id):
        return await message.reply("😏 **ʏσυ ¢αη'τ υѕє τнιѕ ¢σммαη∂**")
    if not message.reply_to_message:
        return await message.reply("👀 **яєρℓу τσ α мєѕѕαgє τσ ριη ιη gяσυρ**")
    try:
        await message.reply_to_message.pin()
        await message.reply("📌 **мєѕѕαgє ριηηє∂ ѕυccєѕѕƒυℓℓγ**")
    except Exception as e:
        await message.reply(f"❌ `{e}`")

# =========================
# Unpin command
# =========================
@Radhe.on_message(radhe_command("unpin") & filters.group)
async def unpin_message(_, message: Message):
    if not is_allowed_user(message.from_user.id):
        return await message.reply("😏 **ʏσυ ¢αη'τ υѕє τнιѕ ¢σммαη∂**")
    if not message.reply_to_message:
        return await message.reply("👀 **яєρℓу τσ α мєѕѕαgє τσ υηριη fяσм τнє gяσυρ**")
    try:
        await message.reply_to_message.unpin()
        await message.reply("📌 **мєѕѕαgє υηριηηє∂ ѕυccєѕѕƒυℓℓγ**")
    except Exception as e:
        await message.reply(f"❌ `{e}`")
