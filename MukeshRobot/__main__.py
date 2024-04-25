import random
import importlib
import re
import time
import asyncio
from platform import python_version as y
from sys import argv
from pyrogram import __version__ as pyrover
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram import __version__ as telever
from telegram.error import (
    BadRequest,
    ChatMigrated,
    NetworkError,
    TelegramError,
    TimedOut,
    Unauthorized,
)
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
)
from telegram.ext.dispatcher import DispatcherHandlerStop
from telegram.utils.helpers import escape_markdown
from telethon import __version__ as tlhver

import MukeshRobot.modules.no_sql.users_db as sql
from MukeshRobot import (
    BOT_NAME,
    BOT_USERNAME,
    LOGGER,
    OWNER_ID,
    START_IMG,
    SUPPORT_CHAT,
    TOKEN,
    StartTime,
    dispatcher,
    pbot,
    telethn,
    updater,
)
from MukeshRobot.modules import ALL_MODULES
from MukeshRobot.modules.helper_funcs.chat_status import is_user_admin
from MukeshRobot.modules.helper_funcs.misc import paginate_modules


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time
PM_START_TEX = """
â Êœá´‡ÊŸÊŸá´ `{}`, Êœá´á´¡ á´€Ê€á´‡ Êá´á´œ \n any help bro... 
"""

PM_START_TEXT = """ 
*Ð½Ñ”Ñƒ {}, welcome bro* !\nâ”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”\n\nâ *Éª á´€á´ {}, á´€É´á´… Éª Êœá´€á´ á´‡ sá´˜á´‡á´„Éªá´€ÊŸ Ò“á´‡á´€á´›á´œÊ€á´‡s.*\nâ *Éª Êœá´€á´ á´‡ á´á´sá´› á´˜á´á´¡á´‡Ê€Ò“á´œÊŸÊŸ É¢Ê€á´á´œá´˜ á´á´€É´á´€É¢á´‡á´á´‡É´á´› + á´á´œsÉªá´„ Ê™á´á´› Ò“á´‡á´€á´›á´œÊ€á´‡s.*"""

buttons = [
        
    [
        InlineKeyboardButton(text="â›©ð˜¼ð˜½ð™„ð™‡ð™„ð™ð™„ð™€ð™Žâ›©", callback_data="Main_help"),
    ],
    
     
]


roy = [
    [
        InlineKeyboardButton(text="á´œá´˜á´…á´€á´›á´‡", url=f"https://t.me/naruto_support1"),
        InlineKeyboardButton(text="êœ±á´œá´˜á´˜á´Ê€á´›", url=f"https://t.me/{SUPPORT_CHAT}"),
    ],
    [
        InlineKeyboardButton(
            text="á´€á´…á´… á´á´‡ Ê™á´€Ê™Ê",
            url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
        ),
    ],
]

HELP_STRINGS = f"""
â *{BOT_NAME}  á´„ÊŸÉªá´„á´‹ á´É´ á´›Êœá´‡ Ê™á´œá´›á´›á´É´ Ê™á´‡ÊŸÊŸá´á´¡ á´›á´ É¢á´‡á´› á´…á´‡sá´„Ê€Éªá´˜á´›Éªá´É´ á´€Ê™á´á´œá´› sá´˜á´‡á´„ÉªÒ“Éªá´„s á´„á´á´á´á´€É´á´…*"""

ABHI = [
"https://telegra.ph/file/84ca7a2785fed5586bf0e.jpg",
"https://telegra.ph/file/4c3d6f66d8f665a3828c8.jpg",
"https://telegra.ph/file/a1db25822e55b36762610.jpg",
"https://telegra.ph/file/fdf6613e49b15e2f603fd.jpg",
"https://telegra.ph/file/cabe388349a857cfac208.jpg",
"https://telegra.ph/file/c6c311a6994e843c00f8b.jpg",
"https://telegra.ph/file/c6c311a6994e843c00f8b.jpg",
"https://telegra.ph/file/e5b31ab148c5eca8e4c0e.jpg",
"https://telegra.ph/file/b3a548d974cfe8d3d9fa8.jpg",
"https://telegra.ph/file/b3a548d974cfe8d3d9fa8.jpg",
"https://telegra.ph/file/b3a548d974cfe8d3d9fa8.jpg",
"https://telegra.ph/file/b3a548d974cfe8d3d9fa8.jpg",
"https://telegra.ph/file/b3a548d974cfe8d3d9fa8.jpg",
"https://telegra.ph/file/b3a548d974cfe8d3d9fa8.jpg",
"https://telegra.ph/file/b3a548d974cfe8d3d9fa8.jpg",
"https://telegra.ph/file/b3a548d974cfe8d3d9fa8.jpg",
"https://telegra.ph/file/b3a548d974cfe8d3d9fa8.jpg",
"https://telegra.ph/file/b3a548d974cfe8d3d9fa8.jpg",
"https://telegra.ph/file/b3a548d974cfe8d3d9fa8.jpg",
"https://telegra.ph/file/b3a548d974cfe8d3d9fa8.jpg",
"https://telegra.ph/file/b3a548d974cfe8d3d9fa8.jpg",
"https://telegra.ph/file/b3a548d974cfe8d3d9fa8.jpg",
"https://telegra.ph/file/b3a548d974cfe8d3d9fa8.jpg",
"https://telegra.ph/file/b3a548d974cfe8d3d9fa8.jpg",
"https://telegra.ph/file/b3a548d974cfe8d3d9fa8.jpg",
"https://telegra.ph/file/b3a548d974cfe8d3d9fa8.jpg",
"https://telegra.ph/file/b3a548d974cfe8d3d9fa8.jpg",
"https://telegra.ph/file/b3a548d974cfe8d3d9fa8.jpg",
"https://telegra.ph/file/b3a548d974cfe8d3d9fa8.jpg",   

]

NYKAA = [
    "https://telegra.ph/file/e5b31ab148c5eca8e4c0e.jpg",
    "https://telegra.ph/file/c6c311a6994e843c00f8b.jpg",    
]


DONATE_STRING = f"""â Êœá´‡Ê Ê™á´€Ê™Ê, Êœá´€á´©á´©Ê á´›á´ Êœá´‡á´€Ê€ á´›Êœá´€á´› Êá´á´œ á´¡á´€É´É´á´€ á´…á´É´á´€á´›á´‡. Êá´á´œ á´„á´€É´ á´…ÉªÊ€á´‡á´„á´›ÊŸÊ á´„á´É´á´›á´€á´„á´› á´Ê á´…á´‡á´ á´‡ÊŸá´á´˜á´‡Ê€ @naruto_of_telegram Ò“á´Ê€ á´…á´É´á´€á´›ÉªÉ´É¢ á´Ê€ Êá´á´œ á´„á´€É´ á´ ÉªsÉªá´› á´Ê sá´œá´©á´©á´Ê€á´› á´„Êœá´€á´› @naruto_support1 á´€É´á´… á´€sá´‹ á´›Êœá´‡Ê€á´‡ á´€Ê™á´á´œá´› á´…á´É´á´€á´›Éªá´É´."""

IMPORTED = {}
MIGRATEABLE = []
HELPABLE = {}
STATS = []
USER_INFO = []
DATA_IMPORT = []
DATA_EXPORT = []
CHAT_SETTINGS = {}
USER_SETTINGS = {}

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("MukeshRobot.modules." + module_name)
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__

    if imported_module.__mod_name__.lower() not in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception("Can't have two modules with the same name! Please change one")

    if hasattr(imported_module, "__help__") and imported_module.__help__:
        HELPABLE[imported_module.__mod_name__.lower()] = imported_module

    # Chats to migrate on chat_migrated events
    if hasattr(imported_module, "__migrate__"):
        MIGRATEABLE.append(imported_module)

    if hasattr(imported_module, "__stats__"):
        STATS.append(imported_module)

    if hasattr(imported_module, "__user_info__"):
        USER_INFO.append(imported_module)

    if hasattr(imported_module, "__import_data__"):
        DATA_IMPORT.append(imported_module)

    if hasattr(imported_module, "__export_data__"):
        DATA_EXPORT.append(imported_module)

    if hasattr(imported_module, "__chat_settings__"):
        CHAT_SETTINGS[imported_module.__mod_name__.lower()] = imported_module

    if hasattr(imported_module, "__user_settings__"):
        USER_SETTINGS[imported_module.__mod_name__.lower()] = imported_module


# do not async
def send_help(chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    dispatcher.bot.send_photo(
        chat_id=chat_id,
        photo=START_IMG,
        caption=text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=keyboard,
    )

def start(update: Update, context: CallbackContext):
    args = context.args
    global uptime
    uptime = get_readable_time((time.time() - StartTime))
    if update.effective_chat.type == "private":
        if len(args) >= 1:
            if args[0].lower() == "help":
                send_help(update.effective_chat.id, HELP_STRINGS)
            elif args[0].lower().startswith("ghelp_"):
                mod = args[0].lower().split("_", 1)[1]
                if not HELPABLE.get(mod, False):
                    return
                send_help(
                    update.effective_chat.id,
                    HELPABLE[mod].__help__,
                    InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="â—", callback_data="help_back")]]
                    ),
                )
            elif args[0].lower() == "markdownhelp":
                IMPORTED["exá´›Ê€á´€s"].markdown_help_sender(update)
            elif args[0].lower().startswith("stngs_"):
                match = re.match("stngs_(.*)", args[0].lower())
                chat = dispatcher.bot.getChat(match.group(1))

                if is_user_admin(chat, update.effective_user.id):
                    send_settings(match.group(1), update.effective_user.id, False)
                else:
                    send_settings(match.group(1), update.effective_user.id, True)

            elif args[0][1:].isdigit() and "rá´œÊŸá´‡s" in IMPORTED:
                IMPORTED["rá´œÊŸá´‡s"].send_rules(update, args[0], from_pm=True)

        else:
            first_name = update.effective_user.first_name
            
            x=update.effective_message.reply_sticker(
                "CAACAgIAAx0CfDXFXwACizpmIN2gvtprjupdFMn_M2jPJOBjXgACfBQAAl2TAUqcozeOx4snLR4E")
            x.delete()
            usr = update.effective_user
            lol = update.effective_message.reply_text(
                PM_START_TEX.format(usr.first_name), parse_mode=ParseMode.MARKDOWN
            )
            time.sleep(0.4)
            lol.edit_text("ðŸŒš")
            time.sleep(0.5)
            lol.edit_text("ðŸ’¸")
            time.sleep(0.3)
            lol.edit_text("ðŸ¤¡")
            time.sleep(0.4)
            lol.delete()
            
            update.effective_message.reply_photo(random.choice(NYKAA),PM_START_TEXT.format(escape_markdown(first_name),BOT_NAME,sql.num_users(),sql.num_chats()),
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=ParseMode.MARKDOWN,
                timeout=60,
            )
    else:
        update.effective_message.reply_photo(
            random.choice(NYKAA),
            caption="â Éª á´€á´ á´€ÊŸÉªá´ á´‡ Ê™á´€Ê™Ê...!\n\nâ <b>Éª á´…Éªá´…É´'á´› sÊŸá´‡á´˜á´› Ê™á´€Ê™Ê.</b> \n\nâ á´œá´˜á´›Éªá´á´‡ âž› <code>{}</code>".format(
                uptime
            ),
            reply_markup=InlineKeyboardMarkup(roy),
            parse_mode=ParseMode.HTML,
        )


def error_handler(update, context):
    """à¹ ÊŸá´É¢ á´›Êœá´‡ á´‡Ê€Ê€á´Ê€ á´€É´á´… sá´‡É´á´… á´€ á´›á´‡ÊŸá´‡É¢Ê€á´€á´ á´á´‡ssá´€É¢á´‡ á´›á´ É´á´á´›ÉªÒ“Ê á´›Êœá´‡ á´…á´‡á´ á´‡ÊŸá´á´˜á´‡Ê€."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    LOGGER.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    message = (
        "â á´€É´ á´‡xá´„á´‡á´˜á´›Éªá´É´ á´¡á´€s Ê€á´€Éªsá´‡á´… á´¡ÊœÉªÊŸá´‡ Êœá´€É´á´…ÊŸÉªÉ´É¢ á´€É´ á´œá´˜á´…á´€á´›á´‡\n"
        "â <pre>á´œá´˜á´…á´€á´›á´‡ = {}</pre>\n\n"
        "â <pre>{}</pre>"
    ).format(
        html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False)),
        html.escape(tb),
    )

    if len(message) >= 4096:
        message = message[:4096]
    # Finally, send the message
    context.bot.send_message(chat_id=OWNER_ID, text=message, parse_mode=ParseMode.HTML)


# for test purposes
def error_callback(update: Update, context: CallbackContext):
    error = context.error
    try:
        raise error
    except Unauthorized:
        print("no nono1")
        print(error)
        # remove update.message.chat_id from conversation list
    except BadRequest:
        print("no nono2")
        print("BadRequest caught")
        print(error)

        # handle malformed requests - read more below!
    except TimedOut:
        print("no nono3")
        # handle slow connection problems
    except NetworkError:
        print("no nono4")
        # handle other connection problems
    except ChatMigrated as err:
        print("no nono5")
        print(err)
        # the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError:
        print(error)
        # handle all other telegram related errors


def help_button(update, context):
    query = update.callback_query
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)

    print(query.message.chat.id)

    try:
        if mod_match:
            module = mod_match.group(1)
            text = (
                "â… *á´€á´ á´€ÉªÊŸá´€Ê™ÊŸá´‡ á´„á´á´á´á´€É´á´…s êœ°á´Ê€* *{}* â…\n".format(
                    HELPABLE[module].__mod_name__
                )
                + HELPABLE[module].__help__
            )
            query.message.edit_caption(text,
                parse_mode=ParseMode.MARKDOWN,
                
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="Ê™á´€á´„á´‹", callback_data="help_back"),InlineKeyboardButton(text="sá´œá´˜á´˜á´Ê€á´›", callback_data="mukesh_support")]]
                ),
            )

        elif prev_match:
            curr_page = int(prev_match.group(1))
            query.message.edit_caption(HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(curr_page - 1, HELPABLE, "help")
                ),
            )

        elif next_match:
            next_page = int(next_match.group(1))
            query.message.edit_caption(HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(next_page + 1, HELPABLE, "help")
                ),
            )

        elif back_match:
            query.message.edit_caption(HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, HELPABLE, "help")
                ),
            )

        # ensure no spinny white circle
        context.bot.answer_callback_query(query.id)
        # query.message.delete()

    except BadRequest:
        pass


def Mukesh_about_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "mukesh_":
        uptime = get_readable_time((time.time() - StartTime))
        query.message.edit_caption(f"*âœ¦ Éª á´€á´ {dispatcher.bot.first_name} âœ¦*"
            "\n\n*â Éª Êœá´€á´ á´‡ á´á´sá´› á´˜á´á´¡á´‡Ê€Ò“á´œÊŸÊŸ É¢Ê€á´á´œá´˜ á´á´€É´á´€É¢á´‡á´á´‡É´á´› + á´á´œsÉªá´„ Ê™á´á´› Ò“á´‡á´€á´›á´œÊ€á´‡s.*"
            "\n\n*â á´¡Ê€Éªá´›á´›á´‡É´ ÉªÉ´ á´©Êá´›Êœá´É´ á´¡Éªá´›Êœ sÇ«ÊŸá´€ÊŸá´„Êœá´‡á´Ê á´€É´á´… á´á´É´É¢á´á´…Ê™ á´€s á´…á´€á´›á´€Ê™á´€sá´‡.*"
            f"\n\n*â á´œsá´‡Ê€s âž›* {sql.num_users()}"
            f"\n*â á´„Êœá´€á´›s âž›* {sql.num_chats()}"
            "\n\nâ Éª á´„á´€É´ Ê€á´‡êœ±á´›Ê€Éªá´„á´› á´œêœ±á´‡Ê€êœ±."
            "\nâ Éª Êœá´€á´ á´‡ á´€É´ á´€á´…á´ á´€É´á´„á´‡á´… á´€É´á´›Éª-êœ°ÊŸá´á´á´… êœ±Êêœ±á´›á´‡á´."
            "\nâ á´€á´…á´ á´€É´á´„á´‡ á´á´€É´á´€É¢á´‡á´á´‡É´á´› á´„á´€á´˜á´€Ê™ÉªÊŸÉªá´›Ê."
            "\nâ á´€É´Éªá´á´‡ Ê™á´á´› Ò“á´œÉ´á´„á´›Éªá´É´á´€ÊŸÉªá´›Ê."
            "\nâ á´€Éª ÉªÉ´á´›á´‡É¢Ê€á´€á´›Éªá´É´."
            f"\n\nâ á´„ÊŸÉªá´„á´‹ á´É´ á´›Êœá´‡ Ê™á´œá´›á´›á´É´s É¢Éªá´ á´‡É´ Ê™á´‡ÊŸá´á´¡ Ò“á´Ê€ É¢á´‡á´›á´›ÉªÉ´É¢ Ê™á´€sÉªá´„ Êœá´‡ÊŸá´© á´€É´á´… ÉªÉ´Ò“á´ á´€Ê™á´á´œá´› {dispatcher.bot.first_name}.",
            parse_mode=ParseMode.MARKDOWN,
                                   
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Êœá´‡ÊŸá´˜ á´á´‡É´á´œ", callback_data="Main_help"
                        ),
                        InlineKeyboardButton(text="É´Êá´‹á´€á´€ ", url="https://t.me/nykaa_update"),
                    ],
                    [
                        InlineKeyboardButton(text="Êœá´á´á´‡", callback_data="mukesh_back"),
                    ],
                ]
            ),
            )
    elif query.data == "mukesh_support":
        query.message.edit_caption("**â á´„ÊŸÉªá´„á´‹ á´É´ á´›Êœá´‡ Ê™á´œá´›á´›á´É´s É¢Éªá´ á´‡É´ Ê™á´œá´›á´›á´É´ á´›á´ á´Šá´ÉªÉ´ á´á´œÊ€ É¢Ê€á´á´œá´˜ á´€É´á´… á´„Êœá´€É´É´á´‡ÊŸ á´›á´ Ê™á´á´› á´œá´˜á´…á´€á´›á´‡ ÉªÉ´Ò“á´Ê€á´á´€á´›Éªá´É´.**"
            f"\n\nâ ÉªÒ“ á´€É´Ê Ê™á´œÉ¢ ÉªÉ´ {dispatcher.bot.first_name}, á´©ÊŸá´‡á´€sá´‡ Ê€á´‡á´©á´Ê€á´› Éªá´› á´€á´› sá´œá´©á´©á´Ê€á´› á´„Êœá´€á´›.",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="êœ±á´œá´˜á´˜á´Ê€á´›", url=f"https://t.me/{SUPPORT_CHAT}"
                        ),
                        InlineKeyboardButton(
                            text="á´œá´˜á´…á´€á´›á´‡", url=f"https://t.me/naruto_support1"
                        ),
                    ],
                    [
                        InlineKeyboardButton(text="Êœá´á´á´‡", callback_data="mukesh_back"),
                    ],
                ]
            ),
        )
    elif query.data == "mukesh_back":
        first_name = update.effective_user.first_name 
        query.message.edit_caption(PM_START_TEXT.format(escape_markdown(first_name), BOT_NAME,sql.num_users(),sql.num_chats()),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.MARKDOWN,
            timeout=60,
        )
def MukeshRobot_Main_Callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "Main_help":
        query.message.edit_caption(f"""
 âœ¦ Êœá´‡Ê€á´‡ Éªêœ± Êœá´‡ÊŸá´˜ á´á´‡É´á´œ êœ°á´Ê€ {BOT_NAME}
""",
            parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="á´á´€É´á´€É¢á´‡", callback_data="help_back"),
                        InlineKeyboardButton(text="á´á´œsÉªá´„", callback_data="Music_")
                    ],
                    [
                        InlineKeyboardButton(text="êœ±á´˜á´€á´", callback_data="Music_roy"),
                        InlineKeyboardButton(text="á´€É´Éªá´á´‡", callback_data="source_") 
                    ],
                    [
                        InlineKeyboardButton(text="Êœá´á´á´‡", callback_data="mukesh_back")
                    ],
                ]
            ),
            )
    elif query.data=="basic_help":
        query.message.edit_caption("""âœ¿ Êœá´‡Ê€á´‡ Éªs á´€ÊŸÊŸ á´€É´Éªá´á´‡ Ê€á´€É´á´…á´á´ Éªá´É¢á´‡s á´„á´á´á´á´€É´á´…s.\n\nâ /gecg âž› sá´‡É´á´… Ê€á´€É´á´…á´á´ É¢á´‡á´„É¢ Éªá´É¢.\nâ /avatar âž› sá´‡É´á´…s Ê€á´€É´á´…á´á´ á´€á´ á´€á´›á´€Ê€ Éªá´É¢.\nâ /foxgirl âž› sá´‡É´á´…s Ê€á´€É´á´…á´á´ Ò“á´xÉ¢ÉªÊ€ÊŸ sá´á´œÊ€á´„á´‡ Éªá´á´€É¢á´‡s.\nâ /waifus âž› sá´‡É´á´…s Ê€á´€É´á´…á´á´ á´¡á´€ÉªÒ“á´œ Éªá´É¢.\nâ /neko âž› sá´‡É´á´…s Ê€á´€É´á´…á´á´ sÒ“á´¡ É´á´‡á´‹á´ sá´á´œÊ€á´„á´‡ Éªá´á´€É¢á´‡s.\nâ /gasm âž› sá´‡É´á´…s Ê€á´€É´á´…á´á´ á´Ê€É¢á´€sá´ Éªá´É¢.\nâ /cuddle âž› sá´‡É´á´…s Ê€á´€É´á´…á´á´ á´„á´œá´…á´…ÊŸá´‡ Éªá´É¢.\nâ /shinobu âž› sá´‡É´á´… Ê€á´€É´á´…á´á´ sÊœÉªÉ´á´Ê™á´œ Éªá´É¢.\nâ /megumin âž› sá´‡É´á´… Ê€á´€É´á´…á´á´ á´á´‡É¢á´œá´ÉªÉ´ Éªá´É¢.\nâ /bully âž› sá´‡É´á´… Ê€á´€É´á´…á´á´ Ê™á´œÊŸÊŸÊ Éªá´É¢.\nâ /cry âž› sá´‡É´á´… Ê€á´€É´á´…á´á´ á´„Ê€Ê Éªá´É¢.\nâ /awoo âž› sá´‡É´á´… Ê€á´€É´á´…á´á´ á´€á´¡á´á´ Éªá´É¢.""",parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="Ê™á´€á´„á´‹", callback_data="Main_help"),InlineKeyboardButton(text="ANIME", callback_data="Avisha_")
                    ]
                ]
            ),
            )
    elif query.data=="mukesh_back":
        query.message.edit_caption("""âœ¿ á´‡xá´˜á´‡Ê€á´› á´„á´á´á´á´€É´á´…s âœ¿

â… á´€á´ á´€ÉªÊŸá´€Ê™ÊŸá´‡ á´›á´ á´€á´…á´ÉªÉ´s â…

â  /unbanall âž› á´á´‡á´Ê™á´‡Ê€s Ò“Ê€á´á´ Êá´á´œÊ€ É¢Ê€á´á´œá´˜s
â  /unmuteall âž› á´œÉ´á´á´œá´›á´‡á´€ÊŸÊŸ á´€ÊŸÊŸ Ò“Ê€á´á´ Êá´á´œÊ€ É¢Ê€á´á´œá´˜

â… á´˜ÉªÉ´É´á´‡á´… Má´‡ssá´€É¢á´‡s â…

â  /pin âž› [á´á´‡ssá´€É¢á´‡] sá´‡É´á´…s á´›Êœá´‡ á´á´‡ssá´€É¢á´‡ á´›ÊœÊ€á´á´œÉ¢Êœ á´›Êœá´‡ Ê™á´á´› á´€É´á´… á´˜ÉªÉ´s Éªá´›.
â  /pin âž› á´˜ÉªÉ´s á´›Êœá´‡ á´á´‡ssá´€É¢á´‡ ÉªÉ´ Ê€á´‡á´˜ÊŸÊ
â  /unpin âž› Ê€á´‡á´á´á´ á´‡s á´›Êœá´‡ á´˜ÉªÉ´É´á´‡á´… á´á´‡ssá´€É¢á´‡.
â  /adminlist âž› ÊŸÉªsá´› á´Ò“ á´€ÊŸÊŸ á´›Êœá´‡ sá´˜á´‡á´„Éªá´€ÊŸ Ê€á´ÊŸá´‡s á´€ssÉªÉ¢É´á´‡á´… á´›á´ á´œsá´‡Ê€s.

â /bug âž› (á´á´‡ssá´€É¢á´‡) á´›á´ sá´‡É´á´… á´á´‡ssá´€É¢á´‡ á´€É´á´… á´‡Ê€Ê€á´Ê€s á´¡ÊœÉªá´„Êœ Êá´á´œ á´€Ê€á´‡ Ò“á´€á´„ÉªÉ´É¢ 
á´‡x âž› /bug Há´‡Ê TÊœá´‡Ê€á´‡ Is á´€ sá´á´á´‡á´›ÊœÉªÉ´É¢ á´‡Ê€Ê€á´Ê€ @username á´Ò“ á´„Êœá´€á´›! .""",parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="Ê™á´€á´„á´‹", callback_data="Main_help"),InlineKeyboardButton(text="êœ±á´œá´˜á´˜á´Ê€á´›", callback_data="mukesh_support")
                    ]
                ]
            ),
            )                                        
    elif query.data=="advance_help":
        query.message.edit_caption("""âœ¿ Êœá´‡Ê€á´‡ Éªs á´€ÊŸÊŸ á´„Êœá´€Ê€á´€á´„á´›á´‡Ê€ á´„á´€á´›á´„Êœá´‡Ê€ ( É¢á´€Ê™Ê™á´€Ê€ Êœá´‡Ê€á´‡á´ ) á´€É´Éªá´á´‡ á´„á´á´á´á´€É´á´…s.\n\nâ /guess âž› á´›á´ É¢á´œá´‡ss á´„Êœá´€Ê€á´€á´„á´›á´‡Ê€.\nâ /fav âž› á´€á´…á´… Êá´á´œÊ€ Ò“á´€á´ Ê€á´€á´›á´‡.\nâ /trade âž› á´›á´ á´›Ê€á´€á´…á´‡ á´„Êœá´€Ê€á´€á´„á´›á´‡Ê€s.\nâ /gift âž› É¢Éªá´ á´‡ á´€É´Ê á´„Êœá´€Ê€á´€á´„á´›á´‡Ê€ Ò“Ê€á´á´ Êá´á´œÊ€ á´„á´ÊŸÊŸá´‡á´„á´›Éªá´É´ á´›á´ á´€É´á´á´›Êœá´‡Ê€ á´œsá´‡Ê€.\nâ /collection âž› á´›á´ sá´‡á´‡ Êá´á´œÊ€ á´„á´ÊŸÊŸá´‡á´„á´›Éªá´É´.\nâ /topgroups âž› sá´‡á´‡ á´›á´á´˜ É¢Ê€á´á´œá´˜s, á´˜á´˜ÊŸ É¢á´œá´‡ssá´‡s á´á´sá´› ÉªÉ´ á´›Êœá´€á´› É¢Ê€á´á´œá´˜s.\nâ /top âž› á´›á´á´ sá´‡á´‡ á´›á´á´˜ á´œsá´‡Ê€s.\nâ /ctop âž› Êá´á´œÊ€ á´„Êœá´€á´› á´›á´á´˜.\nâ /changetime âž› á´„Êœá´€É´É¢á´‡ á´„Êœá´€Ê€á´€á´„á´›á´‡Ê€ á´€á´˜á´˜á´‡á´€Ê€ á´›Éªá´á´‡ .\nâ /herem âž› á´„Êœá´‡á´„á´‹ Êá´á´œÊ€ á´„Êœá´€Ê€á´€á´„á´›á´‡Ê€ á´„Êœá´€á´›á´„Êœ.""",parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="Ê™á´€á´„á´‹", callback_data="Main_help"),InlineKeyboardButton(text="êœ±á´œá´˜á´˜á´Ê€á´›", callback_data="mukesh_support")
                    ]
                ]
            ),
            )
    elif query.data=="expert_help":
        query.message.edit_caption(f"""âœ¿ Êœá´‡Ê€á´‡ Éªs á´€ÉªÊ€Ê€ÉªÉ´É¢, á´á´€É´É¢á´€, á´„Êœá´€Ê€á´€á´„á´›á´‡Ê€ á´€É´á´… á´‡á´›á´„.\n\nâ /anime <anime> âž› Ê€á´‡á´›á´œÊ€É´s ÉªÉ´Ò“á´Ê€á´á´€á´›Éªá´É´ á´€Ê™á´á´œá´› á´›Êœá´‡ á´€É´Éªá´á´‡.\nâ /character <á´„Êœá´€Ê€á´€á´„á´›á´‡Ê€> âž› Ê€á´‡á´›á´œÊ€É´s ÉªÉ´Ò“á´Ê€á´á´€á´›Éªá´É´ á´€Ê™á´á´œá´› á´›Êœá´‡ á´„Êœá´€Ê€á´€á´„á´›á´‡Ê€.\nâ /manga <á´á´€É´É¢á´€> âž› Ê€á´‡á´›á´œÊ€É´s ÉªÉ´Ò“á´Ê€á´á´€á´›Éªá´É´ á´€Ê™á´á´œá´› á´›Êœá´‡ á´á´€É´É¢á´€.\nâ /user  <á´œsá´‡Ê€> âž› Ê€á´‡á´›á´œÊ€É´s ÉªÉ´Ò“á´Ê€á´á´€á´›Éªá´É´ á´€Ê™á´á´œá´› á´€ á´Êá´€É´Éªá´á´‡ÊŸÉªsá´› á´œsá´‡Ê€.\nâ /upcoming âž› Ê€á´‡á´›á´œÊ€É´s á´€ ÊŸÉªsá´› á´Ò“ É´á´‡á´¡ á´€É´Éªá´á´‡ ÉªÉ´ á´›Êœá´‡ á´œá´˜á´„á´á´ÉªÉ´É¢ sá´‡á´€sá´É´s.\nâ /kaizoku <á´€É´Éªá´á´‡> âž› sá´‡á´€Ê€á´„Êœ á´€É´ á´€É´Éªá´á´‡ á´É´ á´€É´Éªá´á´‡á´‹á´€Éªá´¢á´á´‹á´œ.á´„á´á´\nâ /kayo <á´€É´Éªá´á´‡> âž› sá´‡á´€Ê€á´„Êœ á´€É´ á´€É´Éªá´á´‡ á´É´ á´€É´Éªá´á´‡á´‹á´€Êá´.á´„á´á´\nâ /airing <á´€É´Éªá´á´‡> âž› Ê€á´‡á´›á´œÊ€É´s á´€É´Éªá´á´‡ á´€ÉªÊ€ÉªÉ´É¢ ÉªÉ´Ò“á´.\n\nâ /latest âž› á´„Êœá´‡á´„á´‹ ÊŸá´€á´›á´‡sá´› á´€É´Éªá´á´‡ sÊœá´á´¡s á´€É´á´… á´‡á´˜Éªsá´á´…á´‡s.""",
                                   
            parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="Ê™á´€á´„á´‹", callback_data="Main_help"),InlineKeyboardButton(text="á´‡xá´›Ê€á´€", callback_data="mukesh_support")
                    ]
                ]
            ),
            )
    elif query.data=="donation_help":
        query.message.edit_caption("""ðŸ’¥ á´€Ê€á´›ÉªÒ“Éªá´„Éªá´€ÊŸ ÉªÉ´á´›á´‡ÊŸ ÊŸÉªÉ¢á´‡É´á´„á´‡ Ò“á´œÉ´á´„á´›Éªá´É´s ðŸ’¥\n\nâœ¿ á´€ÊŸÊŸ á´„á´á´á´á´€É´á´…s âœ¿\n\nâ á´€Ê™á´á´œá´› âž› á´›Êœá´‡ á´€á´…á´ á´€É´á´„á´‡á´… á´„Êœá´€á´› É¢á´˜á´› á´€Éª - 4 á´á´á´…á´‡ÊŸ êœ°á´Ê€ á´€É´ á´‡É´Êœá´€É´á´„á´‡á´… á´„Êœá´€á´› á´‡xá´˜á´‡Ê€Éªá´‡É´á´„á´‡. \n\nâ á´›ÊœÉªêœ± Éªêœ± á´€ É´á´‡á´¡ êœ°á´‡á´€á´›á´œÊ€á´‡, á´€É´á´… Êá´á´œ á´„á´€É´ á´œêœ±á´‡ Éªá´› á´œÉ´ÊŸÉªá´Éªá´›á´‡á´…ÊŸÊ...\n\nâ /ask âž› á´€ á´„Êœá´€á´›Ê™á´á´› á´œsÉªÉ´É¢ É¢á´˜á´› Ò“á´Ê€ Ê€á´‡sá´˜á´É´á´…ÉªÉ´É¢ á´›á´ á´œsá´‡Ê€ Ç«á´œá´‡Ê€Éªá´‡s.""",parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [ 
                    [
                        InlineKeyboardButton(text="Êœá´á´á´‡", callback_data="mukesh_back"),InlineKeyboardButton(text="êœ±á´œá´˜á´˜á´Ê€á´›", callback_data="Main_help")
                    ]
                ]
            ),
            )  
def Source_about_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "source_":
        query.message.edit_caption(
            f"""âœ¦ Êœá´‡Ê€á´‡ Éªs sá´á´á´‡ á´€É´Éªá´á´‡ á´„á´á´á´á´€á´…s Ò“á´Ê€ Êá´á´œÊ€ É¢Ê€á´á´œá´˜.
""",
            parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                     [
                        InlineKeyboardButton(text="á´¡á´€ÉªÒ“á´œs", callback_data="basic_help"),
                        InlineKeyboardButton(text="á´€ÉªÊ€ÉªÉ´É¢", callback_data="expert_help")
                    ],
                    [
                        InlineKeyboardButton(text="Êœá´‡Ê€á´‡á´", callback_data="advance_help"),
                        InlineKeyboardButton(text="á´€É´Éªá´á´‡-É¢ÉªÒ“", callback_data="Music_roy_extra") 
                    ],
                    [
                        InlineKeyboardButton(text="Ê™á´€á´„á´‹", callback_data="Main_help")
                    ],
                ]
            ),
        )
    elif query.data == "source_back":
        first_name = update.effective_user.first_name
        query.message.edit_caption(
            PM_START_TEXT.format(escape_markdown(first_name), BOT_NAME,sql.num_users(),sql.num_chats()),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.MARKDOWN,
            timeout=60,
            
        )

        
def Music_about_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "Music_":
        query.message.edit_caption(f"""âœ¿ Êœá´‡Ê€á´‡ Éªêœ± Êœá´‡ÊŸá´˜ á´á´‡É´á´œ êœ°á´Ê€ á´á´œêœ±Éªá´„ âœ¿""",
            parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="á´€á´…á´ÉªÉ´", callback_data="Music_admin"
                        ),
                        InlineKeyboardButton(
                            text="á´˜ÊŸá´€Ê", callback_data="Music_play"
                        ),
                    ],
                    [
                        InlineKeyboardButton(text="Ê™á´á´›", callback_data="Music_bot"),
                        InlineKeyboardButton(
                            text="á´‡xá´›Ê€á´€",
                            callback_data="Music_extra",
                        ),
                    ],
                    [
                        InlineKeyboardButton(text="Ê™á´€á´„á´‹", callback_data="Main_help")
                    ],
                ]
            ),
        )
    elif query.data == "Music_admin":
        query.message.edit_caption(f"*âœ¿ á´€á´…á´ÉªÉ´ á´„á´á´á´á´€É´á´…êœ± âœ¿*"
            f"""
â… á´€á´…á´ÉªÉ´s á´€É´á´… á´€á´œá´›Êœ á´œsá´‡Ê€á´€ á´„á´á´á´á´€É´á´…s â…

â /pause âž› á´©á´€á´œsá´‡ á´›Êœá´‡ á´„á´œÊ€Ê€á´‡É´á´› á´©ÊŸá´€ÊÉªÉ´É¢ sá´›Ê€á´‡á´€á´.

â /resume âž› Ê€á´‡sá´œá´á´‡ á´›Êœá´‡ á´©á´€á´œsá´‡á´… sá´›Ê€á´‡á´€á´.

â /skip âž› sá´‹Éªá´© á´›Êœá´‡ á´„á´œÊ€Ê€á´‡É´á´› á´©ÊŸá´€ÊÉªÉ´É¢ sá´›Ê€á´‡á´€á´ á´€É´á´… sá´›á´€Ê€á´› sá´›Ê€á´‡á´€á´ÉªÉ´É¢ á´›Êœá´‡ É´á´‡xá´› á´›Ê€á´€á´„á´‹ ÉªÉ´ Ç«á´œá´‡á´œá´‡.

â /end á´Ê€ /stop âž› á´„ÊŸá´‡á´€Ê€s á´›Êœá´‡ Ç«á´œá´‡á´œá´‡ á´€É´á´… á´‡É´á´… á´›Êœá´‡ á´„á´œÊ€Ê€á´‡É´á´› á´©ÊŸá´€ÊÉªÉ´É¢ sá´›Ê€á´‡á´€á´.

â /player âž› É¢á´‡á´› á´€ ÉªÉ´á´›á´‡Ê€á´€á´„á´›Éªá´ á´‡ á´©ÊŸá´€Êá´‡Ê€ á´©á´€É´á´‡ÊŸ.

â /queue âž› sÊœá´á´¡s á´›Êœá´‡ Ç«á´œá´‡á´œá´‡á´… á´›Ê€á´€á´„á´‹s ÊŸÉªsá´›.
""",
            parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=" Ê™á´€á´„á´‹ ", callback_data="Music_"),InlineKeyboardButton(text="á´›á´á´ÊŸs", callback_data="mukesh_support")
                    ]
                ]
            ),
        )
    elif query.data == "Music_play":
        query.message.edit_caption(f"*âœ¿ á´˜ÊŸá´€Ê á´„á´á´á´á´€É´á´…êœ± âœ¿*"
            f"""
â /play á´Ê€ /vplay á´Ê€ /cplay âž› Ê™á´á´› á´¡ÉªÊŸÊŸ êœ±á´›á´€Ê€á´› á´˜ÊŸá´€ÊÉªÉ´É¢ Êá´á´œÊ€ É¢Éªá´ á´‡É´ Ï™á´œá´‡Ê€Ê on á´ á´Éªá´„á´‡ á´„Êœá´€á´› á´Ê€ êœ±á´›Ê€á´‡á´€á´ ÊŸÉªá´ á´‡ ÊŸÉªÉ´á´‹êœ± á´É´ á´ á´Éªá´„á´‡ á´„Êœá´€á´›êœ±.

â /playforce á´Ê€ /vplayforce á´Ê€ /cplayforce âž› Ò“á´Ê€á´„á´‡ á´˜ÊŸá´€Ê êœ±á´›á´á´˜êœ± á´›Êœá´‡ á´„á´œÊ€Ê€á´‡É´á´› á´˜ÊŸá´€ÊÉªÉ´É¢ á´›Ê€á´€á´„á´‹ á´É´ á´ á´Éªá´„á´‡ á´„Êœá´€á´› á´€É´á´… êœ±á´›á´€Ê€á´›êœ± á´˜ÊŸá´€ÊÉªÉ´É¢ á´›Êœá´‡ êœ±á´‡á´€Ê€á´„Êœá´‡á´… á´›Ê€á´€á´„á´‹ ÉªÉ´êœ±á´›á´€É´á´›ÊŸÊ á´¡Éªá´›Êœá´á´œá´› á´…Éªêœ±á´›á´œÊ€Ê™ÉªÉ´É¢/clearing queue.

â /channelplay âž› [á´„Êœá´€á´› á´œêœ±á´‡Ê€É´á´€á´á´‡ á´Ê€ Éªá´…] á´Ê€ [á´…Éªêœ±á´€Ê™ÊŸá´‡] - á´„á´É´É´á´‡á´„á´› á´„Êœá´€É´É´á´‡ÊŸ á´›á´ á´€ É¢Ê€á´á´œá´˜ á´€É´á´… êœ±á´›Ê€á´‡á´€á´ á´á´œêœ±Éªá´„ á´É´ á´„Êœá´€É´É´á´‡ÊŸ á´ á´Éªá´„á´‡ á´„Êœá´€á´› Ò“Ê€á´á´ Êá´á´œÊ€ É¢Ê€á´á´œá´˜.

 â… Ê™á´á´› êœ±á´‡Ê€á´ á´‡Ê€ á´˜ÊŸá´€ÊÊŸÉªêœ±á´›êœ± â…
 
â /playlist âž› á´„Êœá´‡á´„á´‹ Êá´á´œÊ€ êœ±á´€á´ á´‡á´… á´˜ÊŸá´€ÊÊŸÉªêœ±á´› á´É´ êœ±á´‡Ê€á´ á´‡Ê€êœ±.
â /deleteplaylist âž› á´…á´‡ÊŸá´‡á´›á´‡ á´€É´Ê êœ±á´€á´ á´‡á´… á´á´œêœ±Éªá´„ ÉªÉ´ Êá´á´œÊ€ á´˜ÊŸá´€ÊÊŸÉªêœ±á´›
â /play âž› êœ±á´›á´€Ê€á´› á´˜ÊŸá´€ÊÉªÉ´É¢ Êá´á´œÊ€ êœ±á´€á´ á´‡á´… á´˜ÊŸá´€ÊÊŸÉªêœ±á´› Ò“Ê€á´á´ êœ±á´‡Ê€á´ á´‡Ê€êœ±.
""",
            parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="Ê™á´€á´„á´‹", callback_data="Music_"),InlineKeyboardButton(text="á´‡xá´›Ê€á´€", callback_data="mukesh_support")
                    ]
                ]
            ),
        )
    elif query.data == "Music_bot":
        query.message.edit_caption(f"*âœ¿ Ê™á´á´› á´„á´á´á´á´€É´á´…êœ± âœ¿*"
           
            f"""
â /stats âž› É¢á´‡á´› á´›á´á´˜ 10 á´›Ê€á´€á´„á´‹êœ± É¢ÊŸá´Ê™á´€ÊŸ êœ±á´›á´€á´›êœ±, á´›á´á´˜ 10 á´œêœ±á´‡Ê€êœ± á´Ò“ Ê™á´á´›, á´›á´á´˜ 10 á´„Êœá´€á´›êœ± á´É´ Ê™á´á´›, á´›á´á´˜ 10 á´˜ÊŸá´€Êá´‡á´… ÉªÉ´ á´€ á´„Êœá´€á´› á´‡á´›á´„ á´‡á´›á´„.

â /sudolist âž› á´„Êœá´‡á´„á´‹ sá´œá´…á´ á´œsá´‡Ê€s á´Ò“ á´€Ê™É¢  Ê™á´á´›

â /lyrics [á´á´œsÉªá´„ É´á´€á´á´‡] âž› sá´‡á´€Ê€á´„Êœá´‡s ÊŸÊÊ€Éªá´„s Ò“á´Ê€ á´›Êœá´‡ á´˜á´€Ê€á´›Éªá´„á´œÊŸá´€Ê€ á´á´œsÉªá´„ á´É´ á´¡á´‡Ê™.

â /song [á´›Ê€á´€á´„á´‹ É´á´€á´á´‡] or [Êá´› ÊŸÉªÉ´á´‹] âž› á´…á´á´¡É´ÊŸá´á´€á´… á´€É´Ê á´›Ê€á´€á´„á´‹ Ò“Ê€á´á´ Êá´á´œá´›á´œÊ™á´‡ ÉªÉ´ á´á´˜3 or á´á´˜4 Ò“á´Ê€á´á´€á´›êœ±.

â /player âž›  É¢á´‡t á´€ ÉªÉ´á´›á´‡Ê€á´€á´„á´›Éªá´ á´‡ á´˜ÊŸá´€ÊÉªÉ´É¢ á´˜á´€É´á´‡ÊŸ.

â… c êœ±á´›á´€É´á´…êœ± êœ°á´Ê€ á´„Êœá´€É´É´á´‡ÊŸ á´˜ÊŸá´€Ê â…

â /queue á´Ê€ /cqueue âž› á´„Êœá´‡á´„á´‹ Qá´œá´‡á´œá´‡ ÊŸÉªêœ±á´› á´êœ° á´á´œêœ±Éªá´„.
""",
            parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=" Ê™á´€á´„á´‹ ", callback_data="Music_"),InlineKeyboardButton(text="á´›á´á´ÊŸs", callback_data="mukesh_support")
                    ]
                ]
            ),
        )
    elif query.data == "Music_extra":
        query.message.edit_caption(f"*âœ¿ á´‡xá´›Ê€á´€ á´„á´á´á´á´€É´á´…êœ± âœ¿*"
            
             f"""
â /mstart âž› êœ±á´›á´€Ê€á´› á´›Êœá´‡ á´á´œêœ±Éªá´„ Ê™á´á´›.

â /mhelp âž› É¢á´‡á´› á´„á´á´á´á´€É´á´…êœ± Êœá´‡ÊŸá´˜á´‡Ê€ á´á´‡É´á´œ á´¡Éªá´›Êœ á´…á´‡á´›á´€ÉªÊŸá´‡á´… á´‡xá´˜ÊŸá´€É´á´€á´›Éªá´É´êœ± á´Ò“ á´„á´á´á´á´€É´á´…êœ±.

â /ping âž› á´˜ÉªÉ´É¢ á´›Êœá´‡ Ê™á´á´› á´€É´á´… á´„Êœá´‡á´„á´‹ Ê€á´€á´, á´„á´˜á´œ á´‡á´›á´„ êœ±á´›á´€á´›êœ± á´Ò“ Ê™á´á´›.

*â… É¢Ê€á´á´œá´˜ êœ±á´‡á´›á´›ÉªÉ´É¢êœ± â…*

â /settings âž› É¢á´‡á´› a á´„á´á´á´˜ÊŸá´‡á´›á´‡ É¢Ê€á´á´œá´˜ êœ±á´‡á´›á´›ÉªÉ´É¢êœ± á´¡Éªá´›Êœ ÉªÉ´ÊŸÉªÉ´á´‡ Ê™á´œá´›á´›á´É´êœ±
""",
            parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=" Ê™á´€á´„á´‹ ", callback_data="Music_"),InlineKeyboardButton(text="á´›á´á´ÊŸs", callback_data="mukesh_support")
                    ]
                ]
            ),
        )
    elif query.data == "Music_back":
        first_name = update.effective_user.first_name
        query.message.edit_caption(PM_START_TEXT.format(escape_markdown(first_name), BOT_NAME),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.MARKDOWN,
            timeout=60,

        )

    query = update.callback_query
    if query.data == "Music_roy":
        query.message.edit_caption(f"""âœ¿ Êœá´‡Ê€á´‡ Éªêœ± Êœá´‡ÊŸá´˜ á´á´‡É´á´œ êœ°á´Ê€ êœ±á´˜á´€á´ Ê€á´€Éªá´… âœ¿""",
            parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="êœ±á´˜á´€á´", callback_data="Music_roy_admin"
                        ),
                        InlineKeyboardButton(
                            text="Ê€á´€Éªá´…", callback_data="Music_roy_play"
                        ),
                    ],
                    [
                        InlineKeyboardButton(text="á´á´¡É´á´‡Ê€", callback_data="Music_roy_bot"),
                        InlineKeyboardButton(
                            text="á´„Êœá´€á´›-á´€Éª",
                            callback_data="donation_help",
                        ),
                    ],
                    [
                        InlineKeyboardButton(text="Ê™á´€á´„á´‹", callback_data="Main_help")
                    ],
                ]
            ),
        )
    elif query.data == "Music_roy_admin":
        query.message.edit_caption(f"*âœ¿ êœ±á´˜á´€á´  á´„á´á´á´á´€É´á´…êœ± âœ¿*"
            f"""\n\nÖ soja âž  à¹ êœ±á´˜á´€á´êœ± á´€ á´á´‡êœ±êœ±á´€É¢á´‡. à¹\n  à¹› /spam <count> <message to spam> (you can reply any message if you want bot to reply that message and do spamming)\n  à¹› /spam <count> <replying any message>\n\nÖ ð—£ð—¼ð—¿ð—»ð—¦ð—½ð—®ð—º âž  à¹ á´˜á´Ê€á´á´É¢Ê€á´€á´˜ÊœÊ êœ±á´˜á´€á´. à¹\n  à¹› /pspam <count>\n\nÖ ð—›ð—®ð—»ð—´ âž  à¹ êœ±á´˜á´€á´êœ± Êœá´€É´É¢ÉªÉ´É¢ á´á´‡êœ±êœ±á´€É¢á´‡ êœ°á´Ê€ É¢Éªá´ á´‡É´ á´„á´á´œÉ´á´›á´‡Ê€.""",
            parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=" Ê™á´€á´„á´‹ ", callback_data="Music_roy"),InlineKeyboardButton(text="á´›á´á´ÊŸs", callback_data="mukesh_support")
                    ]
                ]
            ),
        )
    elif query.data == "Music_roy_play":
        query.message.edit_caption(f"*âœ¿ Ê€á´€Éªá´… á´„á´á´á´á´€É´á´…êœ± âœ¿*"
            f"""\n\nÖ soja âž  à¹ á´€á´„á´›Éªá´ á´€á´›á´‡êœ± Ê€á´€Éªá´… á´É´ á´€É´Ê ÉªÉ´á´…Éªá´ Éªá´…á´œá´€ÊŸ á´œêœ±á´‡Ê€ êœ°á´Ê€ É¢Éªá´ á´‡É´ Ê€á´€É´É¢á´‡. à¹\n  à¹› /raid <count> <username>\n  à¹› /raid <count> <reply to user>\n\nÖ ð—¥ð—²ð—½ð—¹ð˜†ð—¥ð—®ð—¶ð—± âž  à¹ á´€á´„á´›Éªá´ á´€á´›á´‡êœ± Ê€á´‡á´˜ÊŸÊ Ê€á´€Éªá´… á´É´ á´›Êœá´‡ á´œêœ±á´‡Ê€. à¹\n  à¹› /rraid <replying to user>\n  à¹› /rraid <username>\n\nÖ ð——ð—¥ð—²ð—½ð—¹ð˜†ð—¥ð—®ð—¶ð—± âž  à¹ á´…á´‡á´€á´„á´›Éªá´ á´€á´›á´‡êœ± Ê€á´‡á´˜ÊŸÊ Ê€á´€Éªá´… á´É´ á´›Êœá´‡ á´œêœ±á´‡Ê€. à¹\n  à¹› /drraid <replying to user>\n  à¹› /drraid <username>\n\nÖ ðŒð‘ðšð¢ð âž  à¹ ÊŸá´á´ á´‡ Ê€á´€Éªá´… á´É´ á´›Êœá´‡ á´œêœ±á´‡Ê€. à¹\n  à¹› /mraid <count> <username>\n  à¹› /mraid <count> <reply to user>\n\nÖ ð’ð‘ðšð¢ð âž  à¹ êœ±Êœá´€Êá´€Ê€Éª Ê€á´€Éªá´… á´É´ á´›Êœá´‡ á´œêœ±á´‡Ê€. à¹\n  à¹› /sraid <count> <username>\n  à¹› /sraid <count> <reply to user>\n\nÖ ð‚ð‘ðšð¢ð âž  à¹ á´€Ê™á´„á´… Ê€á´€Éªá´… á´É´ á´›Êœá´‡ á´œêœ±á´‡Ê€. à¹\n  à¹› /craid <count> <username>\n  à¹› /craid <count> <reply to user>""",
            parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="Ê™á´€á´„á´‹", callback_data="Music_roy"),InlineKeyboardButton(text="á´‡xá´›Ê€á´€", callback_data="mukesh_support")
                    ]
                ]
            ),
        )
    elif query.data == "Music_roy_bot":
        query.message.edit_caption(f"*âœ¿ Ê™á´á´› á´á´¡É´á´‡Ê€ á´„á´á´á´á´€É´á´…êœ± âœ¿*"
           
            f"""\n\nÖ soja âž  à¹ á´œêœ±á´‡Ê€Ê™á´á´› á´„á´á´…êœ± à¹\n  à¹› /ping \n  à¹› /reboot\n  à¹› /sudo <reply to user>  âž› Owner Cmd\n  à¹› /logs âž› Owner Cmd\n\nÖ ð—˜ð—°ð—µð—¼ âž  à¹ á´›á´ á´€á´„á´›Éªá´ á´‡ á´‡á´„Êœá´ á´É´ á´€É´Ê á´œêœ±á´‡Ê€ à¹\n  à¹› /echo <reply to user>\n  à¹› /rmecho <reply to user>\n\nÖ ð—Ÿð—²ð—®ð˜ƒð—² âž  à¹ á´›á´ ÊŸá´‡á´€á´ á´‡ É¢Ê€á´á´œá´˜/á´„Êœá´€É´É´á´‡ÊŸ à¹\n  à¹› /leave <group/chat id>\n  à¹› /leave âž› Type in the Group bot will auto leave that group""",
            parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=" Ê™á´€á´„á´‹ ", callback_data="Music_roy"),InlineKeyboardButton(text="á´›á´á´ÊŸs", callback_data="mukesh_support")
                    ]
                ]
            ),
        )
    elif query.data == "Music_roy_extra":
        query.message.edit_caption(f"*âœ¿ á´‡xá´›Ê€á´€ á´„á´á´á´á´€É´á´…êœ± âœ¿*"
            
             f"""
â /mstart âž› êœ±á´›á´€Ê€á´› á´›Êœá´‡ á´á´œêœ±Éªá´„ Ê™á´á´›.

â /mhelp âž› É¢á´‡á´› á´„á´á´á´á´€É´á´…êœ± Êœá´‡ÊŸá´˜á´‡Ê€ á´á´‡É´á´œ á´¡Éªá´›Êœ á´…á´‡á´›á´€ÉªÊŸá´‡á´… á´‡xá´˜ÊŸá´€É´á´€á´›Éªá´É´êœ± á´Ò“ á´„á´á´á´á´€É´á´…êœ±.

â /ping âž› á´˜ÉªÉ´É¢ á´›Êœá´‡ Ê™á´á´› á´€É´á´… á´„Êœá´‡á´„á´‹ Ê€á´€á´, á´„á´˜á´œ á´‡á´›á´„ êœ±á´›á´€á´›êœ± á´Ò“ Ê™á´á´›.

*â… É¢Ê€á´á´œá´˜ êœ±á´‡á´›á´›ÉªÉ´É¢êœ± â…*

â /settings âž› É¢á´‡á´› a á´„á´á´á´˜ÊŸá´‡á´›á´‡ É¢Ê€á´á´œá´˜ êœ±á´‡á´›á´›ÉªÉ´É¢êœ± á´¡Éªá´›Êœ ÉªÉ´ÊŸÉªÉ´á´‡ Ê™á´œá´›á´›á´É´êœ±
""",
            parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=" Ê™á´€á´„á´‹ ", callback_data="Music_roy"),InlineKeyboardButton(text="Êœá´á´á´‡", callback_data="Main_help")
                    ]
                ]
            ),
        )
    elif query.data == "Music_back":
        first_name = update.effective_user.first_name
        query.message.edit_caption(PM_START_TEXT.format(escape_markdown(first_name), BOT_NAME),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.MARKDOWN,
            timeout=60,
             )
         
def get_help(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    args = update.effective_message.text.split(None, 1)

    # ONLY send help in PM
    if chat.type != chat.PRIVATE:
        if len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
            module = args[1].lower()
            update.effective_message.reply_photo(random.choice(ABHI),
                f"â á´„á´É´á´›á´€á´„á´› á´á´‡ ÉªÉ´ á´˜á´ á´›á´ É¢á´‡á´› Êœá´‡ÊŸá´˜ á´Ò“ {module.capitalize()}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Êœá´‡ÊŸá´˜",
                                url="t.me/{}?start=ghelp_{}".format(
                                    context.bot.username, module
                                ),
                            )
                        ]
                    ]
                ),
            )
            return
        update.effective_message.reply_photo(random.choice(NYKAA),"â á´¡Êœá´‡Ê€á´‡ á´…á´ Êá´á´œ á´¡á´€É´á´› á´›á´ á´á´˜á´‡É´ á´›Êœá´‡ sá´‡á´›á´›ÉªÉ´É¢s á´á´‡É´á´œ?.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="á´á´©á´‡É´ ÉªÉ´ á´©Ê€Éªá´ á´€á´›á´‡",
                            url="https://t.me/{}?start=help".format(context.bot.username),
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="á´á´©á´‡É´ Êœá´‡Ê€á´‡",
                            callback_data="help_back",
                        )
                    ],
                ]
            ),
        )
        return

    elif len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
        module = args[1].lower()
        text = (
            "Here is the available help for the *{}* module:\n".format(
                HELPABLE[module].__mod_name__
            )
            + HELPABLE[module].__help__
        )
        send_help(
            chat.id,
            text,
            InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="â—", callback_data="help_back"),InlineKeyboardButton(text="sá´œá´˜á´˜á´Ê€á´›", callback_data="mukesh_support")]]
            ),
        )

    else:
        send_help(chat.id, HELP_STRINGS)


def send_settings(chat_id, user_id, user=False):
    if user:
        if USER_SETTINGS:
            settings = "\n\n".join(
                "*{}*:\n{}".format(mod.__mod_name__, mod.__user_settings__(user_id))
                for mod in USER_SETTINGS.values()
            )
            dispatcher.bot.send_message(
                user_id,
                "These are your current settings:" + "\n\n" + settings,
                parse_mode=ParseMode.MARKDOWN,
            )

        else:
            dispatcher.bot.send_message(
                user_id,
                "Seems like there aren't any user specific settings available :'(",
                parse_mode=ParseMode.MARKDOWN,
            )

    else:
        if CHAT_SETTINGS:
            chat_name = dispatcher.bot.getChat(chat_id).title
            dispatcher.bot.send_message(
                user_id,
                text="Which module would you like to check {}'s settings for?".format(
                    chat_name
                ),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )
        else:
            dispatcher.bot.send_message(
                user_id,
                "Seems like there aren't any chat settings available :'(\nSend this "
                "in a group chat you're admin in to find its current settings!",
                parse_mode=ParseMode.MARKDOWN,
            )


def settings_button(update: Update, context: CallbackContext):
    query = update.callback_query
    user = update.effective_user
    bot = context.bot
    mod_match = re.match(r"stngs_module\((.+?),(.+?)\)", query.data)
    prev_match = re.match(r"stngs_prev\((.+?),(.+?)\)", query.data)
    next_match = re.match(r"stngs_next\((.+?),(.+?)\)", query.data)
    back_match = re.match(r"stngs_back\((.+?)\)", query.data)
    try:
        if mod_match:
            chat_id = mod_match.group(1)
            module = mod_match.group(2)
            chat = bot.get_chat(chat_id)
            text = "*{}* has the following settings for the *{}* module:\n\n".format(
                escape_markdown(chat.title), CHAT_SETTINGS[module].__mod_name__
            ) + CHAT_SETTINGS[module].__chat_settings__(chat_id, user.id)
            query.message.reply_text(text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="â—",
                                callback_data="stngs_back({})".format(chat_id),
                            )
                        ]
                    ]
                ),
            )

        elif prev_match:
            chat_id = prev_match.group(1)
            curr_page = int(prev_match.group(2))
            chat = bot.get_chat(chat_id)
            query.message.reply_text("""Hi there! There are quite a few settings for {} - go ahead and pick what "
                you're interested in.""".format(chat.title),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        curr_page - 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif next_match:
            chat_id = next_match.group(1)
            next_page = int(next_match.group(2))
            chat = bot.get_chat(chat_id)
            query.message.reply_text(text=
                """Hi there! There are quite a few settings for {} - go ahead and pick what 
                you're interested in.""".format(chat.title),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        next_page + 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif back_match:
            chat_id = back_match.group(1)
            chat = bot.get_chat(chat_id)
            query.message.reply_text("""Hi there! There are quite a few settings for {} - go ahead and pick what 
                you're interested in.""".format(escape_markdown(chat.title)),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )

        # ensure no spinny white circle
        bot.answer_callback_query(query.id)
        query.message.delete()
    except BadRequest as excp:
        if excp.message not in [
            "Message is not modified",
            "Query_id_invalid",
            "Message can't be deleted",
        ]:
            LOGGER.exception("Exception in settings buttons. %s", str(query.data))


def get_settings(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    msg = update.effective_message  # type: Optional[Message]

    # ONLY send settings in PM
    if chat.type != chat.PRIVATE:
        if is_user_admin(chat, user.id):
            text = "à¹ á´„ÊŸÉªá´„á´‹ Êœá´‡Ê€á´‡ á´›á´ É¢á´‡á´› á´›ÊœÉªs á´„Êœá´€á´›'s sá´‡á´›á´›ÉªÉ´É¢s á´€s á´¡á´‡ÊŸÊŸ á´€s Êá´á´œÊ€s"
            msg.reply_photo(random.choice(ABHI),text,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="sá´‡á´›á´›ÉªÉ´É¢s",
                                url="t.me/{}?start=stngs_{}".format(
                                    context.bot.username, chat.id
                                ),
                            )
                        ]
                    ]
                ),
            )
        else:
            text = "â á´„ÊŸÉªá´„á´‹ Êœá´‡Ê€á´‡ á´›á´ á´„Êœá´‡á´„á´‹ Êá´á´œÊ€ sá´‡á´›á´›ÉªÉ´É¢s"

    else:
        send_settings(chat.id, user.id, True)


def donate(update: Update, context: CallbackContext):
    user = update.effective_message.from_user
    chat = update.effective_chat  # type: Optional[Chat]
    bot = context.bot
    if chat.type == "private":
        update.effective_message.reply_text(
            DONATE_STRING, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True
        )

        if OWNER_ID != 6590287973:
            update.effective_message.reply_text(
                f"à¹ á´›Êœá´‡ á´…á´‡á´ á´‡ÊŸá´á´©á´‡Ê€ á´Ò“ {dispatcher.bot.first_name} sá´á´œÊ€á´„á´‡ á´„á´á´…á´‡ Éªs [É¢Éªá´›Êœá´œÊ™](https://github.com/noob-mukesh/nothing?)"
                f"\n\nà¹ Ê™á´œá´› Êá´á´œ á´„á´€É´ á´€ÊŸsá´ á´…á´É´á´€á´›á´‡ á´›á´ á´›Êœá´‡ á´©á´‡Ê€sá´É´ á´„á´œÊ€Ê€á´‡É´á´›ÊŸÊ Ê€á´œÉ´É´ÉªÉ´É¢ á´á´‡ : [Êœá´‡Ê€á´‡]",
                parse_mode=ParseMode.MARKDOWN,
                
            )

    else:
        try:
            bot.send_message(
                user.id,
                DONATE_STRING,
                parse_mode=ParseMode.MARKDOWN,
                
            )

            update.effective_message.reply_text(
                "â Éªá´ á´‡ á´˜á´'á´‡á´… Êá´á´œ á´€Ê™á´á´œá´› á´…á´É´á´€á´›ÉªÉ´É¢ á´›á´ á´Ê á´„Ê€á´‡á´€á´›á´Ê€!"
            )
        except Unauthorized:
            update.effective_message.reply_text(
                "â á´„á´É´á´›á´€á´„á´› á´á´‡ ÉªÉ´ á´˜á´ Ò“ÉªÊ€sá´› á´›á´ É¢á´‡á´› á´…á´É´á´€á´›Éªá´É´ ÉªÉ´Ò“á´Ê€á´á´€á´›Éªá´É´."
            )


def migrate_chats(update: Update, context: CallbackContext):
    msg = update.effective_message  # type: Optional[Message]
    if msg.migrate_to_chat_id:
        old_chat = update.effective_chat.id
        new_chat = msg.migrate_to_chat_id
    elif msg.migrate_from_chat_id:
        old_chat = msg.migrate_from_chat_id
        new_chat = update.effective_chat.id
    else:
        return

    LOGGER.info("Migrating from %s, to %s", str(old_chat), str(new_chat))
    for mod in MIGRATEABLE:
        mod.__migrate__(old_chat, new_chat)

    LOGGER.info("Successfully migrated!")
    raise DispatcherHandlerStop


def main():
    global x
    x=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="á´€á´…á´… á´á´‡ Ê™á´€Ê™Ê",
                            url="https://t.me/avishaxbot?startgroup=true"
                            )
                       ]
                ]
                     )
    if SUPPORT_CHAT is not None and isinstance(SUPPORT_CHAT, str):
        try:
            dispatcher.bot.send_photo(
                f"@{SUPPORT_CHAT}",
                photo=f"{START_IMG}",
                caption=f"""
âœ¦ã…¤{BOT_NAME} Éªs á´€ÊŸÉªá´ á´‡ Ê™á´€Ê™Ê âœ¦
     â”â”â”â”â”â”â”â” ðŸ®âœ¿ðŸ® â”â”â”â”â”â”â”â”
**â… á´á´€á´…á´‡ Ê™Ê âž› [Ê€á´Ê-á´‡á´…Éªá´›x](https://t.me/naruto_support1)**
**â… á´˜Êá´›Êœá´É´ á´ á´‡Ê€sÉªá´É´ âž›** `{y()}`
**â… ÊŸÉªÊ™Ê€á´€Ê€Ê á´ á´‡Ê€sÉªá´É´ âž›** `{telever}`
**â… á´›á´‡ÊŸá´‡á´›Êœá´É´ á´ á´‡Ê€sÉªá´É´ âž›** `{tlhver}`
**â… á´©ÊÊ€á´É¢Ê€á´€á´ á´ á´‡Ê€sÉªá´É´ âž›** `{pyrover}`
     â”â”â”â”â”â”â”â” ðŸ®âœ¿ðŸ® â”â”â”â”â”â”â”â”
""",reply_markup=x,
                parse_mode=ParseMode.MARKDOWN,
            )
        except Unauthorized:
            LOGGER.warning(
                f"Bot isn't able to send message to @{SUPPORT_CHAT}, go and check!"
            )
        except BadRequest as e:
            LOGGER.warning(e.message)
    start_handler = CommandHandler("start", start, run_async=True)

    help_handler = CommandHandler("help", get_help, run_async=True)
    help_callback_handler = CallbackQueryHandler(
        help_button, pattern=r"help_.*", run_async=True
    )

    settings_handler = CommandHandler("settings", get_settings, run_async=True)
    settings_callback_handler = CallbackQueryHandler(
        settings_button, pattern=r"stngs_", run_async=True
    )

    about_callback_handler = CallbackQueryHandler(
        Mukesh_about_callback, pattern=r"mukesh_", run_async=True
    )
    source_callback_handler = CallbackQueryHandler(
        Source_about_callback, pattern=r"source_", run_async=True
    )
    music_callback_handler = CallbackQueryHandler(
        Music_about_callback, pattern=r"Music_",run_async=True
    )
    mukeshrobot_main_handler = CallbackQueryHandler(
        MukeshRobot_Main_Callback, pattern=r".*_help",run_async=True)
    donate_handler = CommandHandler("donate", donate)
    migrate_handler = MessageHandler(Filters.status_update.migrate, migrate_chats)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(about_callback_handler)
    dispatcher.add_handler(music_callback_handler)
    dispatcher.add_handler(settings_handler)
    dispatcher.add_handler(help_callback_handler)
    dispatcher.add_handler(settings_callback_handler)
    dispatcher.add_handler(migrate_handler)
    dispatcher.add_handler(donate_handler)
    dispatcher.add_handler(mukeshrobot_main_handler)
    dispatcher.add_error_handler(error_callback)
    dispatcher.add_handler(source_callback_handler)
    LOGGER.info("Using long polling.")
    updater.start_polling(timeout=15, read_latency=4, drop_pending_updates=True)

    if len(argv) not in (1, 3, 4):
        telethn.disconnect()
    else:
        telethn.run_until_disconnected()

    updater.idle()


if __name__ == "__main__":
    LOGGER.info("Successfully loaded modules: " + str(ALL_MODULES))
    telethn.start(bot_token=TOKEN)
    pbot.start()
    main()
        
