import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.config import Messages, BotCommands


@Client.on_message(filters.command(["start"]) & filters.private)
async def start(bot, update):

    await update.reply_text(
        text=Messages.START_MSG.format(update.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=Messages.START_BUTTONS
    )
