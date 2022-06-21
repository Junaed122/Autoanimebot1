from main.modules.cv2_utils import get_duration, get_epnum, get_filesize
from main.modules.anilist import get_anime_name
from main.modules.anilist import get_anime_img
from main.modules.thumbnail import generate_thumbnail
from config import CHANNEL_ID
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from main.modules.progress import progress_for_pyrogram
from os.path import isfile
import os
import time
from main import app

async def upload_video(msg: Message,file,id,tit,name,message_id):
    try:
        fuk = isfile(file)
        if fuk:
            r = msg
            c_time = time.time()

            duration = get_duration(file)
            size = get_filesize(file)
            ep_num = get_epnum(name)
            thumbnail,w,h = generate_thumbnail(id,file,tit,ep_num,size,duration)
            
            buttons = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(text="Info", url="https://t.me/Anime_Dex"),
                    InlineKeyboardButton(text="Comments", url=f"https://t.me/AniDec/{message_id}?thread={message_id}")
                ]
            ])

            caption = f"🎥 **{name}**"

            x = await app.send_video(
                CHANNEL_ID,
            file,
            caption=caption,
            duration=duration,
            width=w,
            height=h,
            thumb=thumbnail,
            reply_markup=buttons,
            file_name=os.path.basename(file),
            progress=progress_for_pyrogram,
            progress_args=(
                os.path.basename(file),
                r,
                c_time
            )
            )        
        try:
            await r.delete()
            os.remove(file)
        except:
            pass
    except Exception as e:
        print(e)
    return