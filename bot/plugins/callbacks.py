from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client

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
