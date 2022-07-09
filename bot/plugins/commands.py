from pyrogram import filters
from pyrogram.types import CallbackQuery, Message

from vidmergebot.bot_class import VidMergeBot
from vidmergebot.utils.constants import Constants
from vidmergebot.utils.ikb import ikb
from vidmergebot.vars import Vars


@Client.on_message(
    filters.command("start") & filters.private,
)
async def start_bot(_, m: Message):
    return await m.reply_text(
        Messages.START_MSG.format(m.from_user.first_name, Messages.CAPTION),
        reply_markup=ikb(Messages.start_kb),
        disable_web_page_preview=True,
        quote=True,
    )


@Client.on_message(
    filters.command("help") & filters.private,
)
async def help_bot(_, m: Message):
    return await m.reply_text(
        Messages.HELP_MSG,
        reply_markup=ikb(Messages.page1_help_kb),
        disable_web_page_preview=True,
    )



