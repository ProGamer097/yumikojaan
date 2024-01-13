"""MIT License

Copyright (c) 2023-24 Noob-Mukesh

          GITHUB: NOOB-MUKESH
          TELEGRAM: @MR_SUKKUN

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""

from pyrogram import filters
from pyrogram.types import  Message
from pyrogram.enums import ChatAction
from pyrogram.types import InputMediaPhoto
from .. import pbot as  Mukesh,BOT_USERNAME
import requests

#import requests
#import random
#import MukeshRobot.strings.animal_facts_string as InputMediaPhoto
#from MukeshRobot import dispatcher
#from telegram import Update
#from MukeshRobot.modules.disable import DisableAbleCommandHandler
#from telegram.ext import CallbackContext

#@Mukesh.on_message(filters.command("imagine"))
#async def imagine_(b, message: Message):
    #if message.reply_to_message:
        #text = message.reply_to_message.text
    #else:
        #text =message.text.split(None, 1)[1]
    #m =await message.reply_text( "`❍ ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...,\n\n❍ ɢᴇɴᴇʀᴀᴛɪɴɢ ᴘʀᴏᴍᴘᴛ .. ...`")
    #results= requests.get(f"https://mukesh-api.vercel.app/imagine/{text}").json()["results"]

    #caption = f"""
#✦ sᴜᴄᴇssғᴜʟʟʏ ɢᴇɴᴇʀᴀᴛᴇᴅ ✦

#❍ **ɢᴇɴᴇʀᴀᴛᴇᴅ ʙʏ ➛** [๛ᴀ ᴠ ɪ s ʜ ᴀ ༗](https://t.me/Avishaxbot)
#❍ **ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ ➛** {message.from_user.mention}
#"""
    #await m.delete()
    #photos=[]
    #for i in range(5):
        #photos.append(InputMediaPhoto(results[i]))
    #photos.append(InputMediaPhoto(results[5], caption=caption))
    #await b.send_media_group(message.chat.id, media=photos)




async def animalfact_(b, message: Message):
  if message.effective_message.reply_text(random.choice(animal_facts.ANIMAL_FACTS))

def cats_(b, message: Message):
    msg = message.effective_message
    else:
        url = f'https://aws.random.cat/meow'
        result = requests.get(url).json()
        img = result['file']
        msg.reply_photo(photo=img)
    except:        
        url = f'https://aws.random.cat/meow'
        result = requests.get(url).json()
        img = result['file']
        msg.reply_photo(photo=img)

ANIMALFACT_HANDLER = DisableAbleCommandHandler("animalfacts", animalfact, run_async=True)
dispatcher.add_handler(ANIMALFACT_HANDLER)
CAT_HANDLER = DisableAbleCommandHandler(("cats", "cat"), cats, run_async=True)
dispatcher.add_handler(CAT_HANDLER)

__mod_name__ = "Animals"
__help__ = """
   ➢ `/animalfacts` - To Get random animal facts.
   ➢ `/cats` - To Get Random Photo of Cats.
   ➢ `/goose`*:* Sends Random Goose pic.
   ➢ `/woof`*:* Sends Random Woof pic.
   ➢ `/lizard`*:* Sends Random Lizard GIFs.
"""