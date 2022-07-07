from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client
from bot.config import Messages, BotCommands
from pyrogram import Client, filters

@Client.on_callback_query()
def cb_handler(client, query):

    if query.data == "setting":
        query.answer()
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✔️ YES", callback_data="YES"),
                InlineKeyboardButton("❌ NO", callback_data="NO")]
        ])

        f = open("./settings.txt", "r")
        setting = f.read()

        emojiCurrent = ""
        
        if setting == "YES":
            emojiCurrent += "✔️"
        elif setting == "NO":
            emojiCurrent += "❌"
        

        query.message.edit_text(
            f"**Please Select Yes to PARSE File Name as Torrent File Name\nOR Select NO to keep the File Name Same\n\nCurrent Setting: {emojiCurrent} {setting}**",
            reply_markup=keyboard,
            disable_web_page_preview=True
        )
        return
    
    elif query.data == "YES":
        query.answer()
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 BACK", callback_data="setting")]
        ])
        f = open("./settings.txt", "a")
        deleteContent = open('./settings.txt', 'r+')
        f.truncate(0)
        f.write(f"{query.data}")
        query.message.edit_text(
            f"**✔️ Settings Applied Succcessfully...\n\nClick on Go Back to Change the Settings**",
            reply_markup=keyboard,
            disable_web_page_preview=True
        )
        return
    
    elif query.data == "NO":
        query.answer()
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 BACK", callback_data="setting")]
        ])
        f = open("./settings.txt", "a")
        deleteContent = open('./settings.txt', 'r+')
        f.truncate(0)
        f.write(f"{query.data}")
        query.message.edit_text(
            "**✔️ Settings Applied Succcessfully...\n\nClick on Go Back Button to Change the Settings**",
            reply_markup=keyboard,
            disable_web_page_preview=True
        )
        return
    if query.data == "home":
        await query.message.edit_text(
            text=Messages.START_TEXT.format(update.from_user.mention),
            reply_markup=Messages.START_BUTTONS,
            disable_web_page_preview=True
        )
    elif query.data == "help":
        await query.message.edit_text(
            text=Messages.HELP_TEXT,
            reply_markup=Messages.HELP_BUTTONS,
            disable_web_page_preview=True
        )
    elif query.data == "about":
        await query.message.edit_text(
            text=Messages.ABOUT_TEXT,
            reply_markup=Messages.ABOUT_BUTTONS,
            disable_web_page_preview=True
        )
