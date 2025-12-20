import os
import aiohttp
import tempfile

from pyrogram.types import Message
from Radhe import Radhe

API = "https://last-warning.serv00.net/md.php?url={}"

@Radhe.on_cmd("download")
async def download(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            "❌ Usage:\n`Radhe download <instagram | pinterest | youtube link>`"
        )

    url = message.text.split(None, 1)[1].strip()
    wait = await message.reply_text("⏳ đøωηℓσαđιηg ყσυя яєqυєѕт βαву… ρℓєαѕє ωαιт")

    try:
        # ---- Fetch API response ----
        async with aiohttp.ClientSession() as session:
            async with session.get(API.format(url), timeout=30) as r:
                data = await r.json()

        if data.get("statusCode") != 200:
            return await wait.edit("❌ API error.\n contact @candy_caugh")

        medias = data.get("medias", [])
        if not medias:
            return await wait.edit("❌ Media not found.")

        media = medias[0]   # best / first
        media_url = media["url"]
        media_type = media.get("type")
        title = data.get("title", "")

        # ---- Temp file ----
        suffix = ".mp4" if media_type == "video" else ".jpg"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp_path = tmp.name

        # ---- Download actual media ----
        async with aiohttp.ClientSession() as session:
            async with session.get(media_url) as r:
                with open(tmp_path, "wb") as f:
                    async for chunk in r.content.iter_chunked(10240):
                        f.write(chunk)

        await wait.delete()

        # ---- Send to Telegram ----
        if media_type == "video":
            await message.reply_video(video=tmp_path, caption=title)
        else:
            await message.reply_photo(photo=tmp_path, caption=title)

        os.remove(tmp_path)

    except Exception as e:
        await wait.edit(f"❌ Error:\n`{e}`")
