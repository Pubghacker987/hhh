from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client
from bot.config import Messages, BotCommands
from bot.helpers.utils import CustomFilters
from pyrogram import Client, filters


@Client.on_message(filters.private & filters.incoming & filters.text & (filters.command(BotCommands.Settings)) & CustomFilters.auth_users)

def _setting_file_name(client, message):
    user_id = message.from_user.id
    sent_message = message.reply_text('**Select the required Settings...**', reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text="📁 File Name", callback_data="setting")]
        ]), reply_to_message_id=user_id)
