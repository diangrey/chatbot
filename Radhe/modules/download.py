import os
import tempfile
import aiohttp
import aiofiles

from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from Radhe import Radhe

API = "https://last-warning.serv00.net/md.php?url="

# =====================================
# /download (YT / IG / Pinterest)
# =====================================
@Radhe.on_message(filters.command("download"))
async def download(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("❌ **Provide a link**")

    url = message.text.split(None, 1)[1]
    msg = await message.reply_text("⏳ đøωηℓσαđιηg ყσυя яєqυєѕт βαву… ρℓєαѕє ωαιт")

    async with aiohttp.ClientSession() as session:
        async with session.get(API + url) as r:
            data = await r.json()

    if data.get("statusCode") != 200 or not data.get("medias"):
        return await msg.edit("❌ **No media found**")

    # ---------- YouTube ----------
    if "youtube.com" in url or "youtu.be" in url:
        buttons = [
            [
                InlineKeyboardButton("🎬 360p", callback_data=f"dl|yt|360|{url}"),
                InlineKeyboardButton("🎬 720p", callback_data=f"dl|yt|720|{url}")
            ],
            [
                InlineKeyboardButton("🎬 1080p", callback_data=f"dl|yt|1080|{url}")
            ],
            [
                InlineKeyboardButton("🎧 MP3", callback_data=f"dl|yt|mp3|{url}")
            ]
        ]
        return await msg.edit(
            "ωнαт ᴅσ уσυ ωαηт ʈσ ∂σ?",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    # ---------- Instagram / Pinterest ----------
    buttons = [
        [
            InlineKeyboardButton("⬇️ Download", callback_data=f"dl|sm|best|{url}")
        ]
    ]

    await msg.edit(
        "⬇️ **Media found**",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# =====================================
# CALLBACK HANDLER
# =====================================
@Radhe.on_callback_query(filters.regex("^dl\\|"))
async def callback(_, query: CallbackQuery):
    await query.answer()
    _, platform, quality, url = query.data.split("|", 3)

    status = await query.message.edit_text("⏳ đøωηℓσαđιηg ყσυя яєqυєѕт βαву… ρℓєαѕє ωαιт")

    async with aiohttp.ClientSession() as session:
        async with session.get(API + url) as r:
            data = await r.json()

        medias = data.get("medias", [])
        if not medias:
            return await status.edit("❌ **Media not available**")

        selected = None

        # ---------- YouTube ----------
        if platform == "yt":
            if quality == "mp3":
                for m in medias:
                    if m.get("type") == "audio":
                        selected = m
                        break
            else:
                for m in medias:
                    q_label = m.get("quality", "") or m.get("qualityLabel", "")
                    if m.get("type") == "video" and quality in q_label:
                        selected = m
                        break

        # ---------- Instagram / Pinterest ----------
        else:
            selected = medias[0]

        # Fallback
        if not selected:
            selected = medias[0]

        file_url = selected["url"]
        ext = selected.get("extension", "mp4")

        # ---------- Download file asynchronously ----------
        tmp_path = None
        try:
            # Create temp file
            tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}")
            tmp_path = tmp_file.name
            tmp_file.close()  # close sync file

            # Async download to temp file
            async with session.get(file_url) as resp:
                async with aiofiles.open(tmp_path, 'wb') as f:
                    async for chunk in resp.content.iter_chunked(65536):
                        await f.write(chunk)

            # ---------- Send to Telegram ----------
            if ext == "mp3":
                await query.message.reply_audio(
                    audio=tmp_path,
                    caption="🎧 **ʜєяє ιѕ үσυя αυ∂ισ**"
                )
            elif ext.lower() in ["jpg", "jpeg", "png"]:
                await query.message.reply_photo(
                    photo=tmp_path,
                    caption="🖼 **ʜєяє ιѕ үσυя ιмαgє**"
                )
            else:
                await query.message.reply_video(
                    video=tmp_path,
                    caption="🎬 **ʜєяє ιѕ үσυя νι∂єσ**"
                )

        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.remove(tmp_path)
            await status.delete()
