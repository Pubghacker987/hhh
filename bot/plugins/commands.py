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
        Constants.start_msg.format(m.from_user.first_name, Vars.CAPTION),
        reply_markup=ikb(Constants.start_kb),
        disable_web_page_preview=True,
        quote=True,
    )


@Client.on_message(
    filters.command("help") & filters.private,
)
async def help_bot(_, m: Message):
    return await m.reply_text(
        Messages.page1_help,
        reply_markup=ikb(Constants.page1_help_kb),
        disable_web_page_preview=True,
    )


@Client.on_callback_query(filters.regex("^help_callback."))
async def help_callback_func(_, q: CallbackQuery):
    qdata = q.data.split(".")[1]
    if qdata in ("start", "page1"):
        await q.message.edit_text(
            Constants.page1_help,
            reply_markup=ikb(Constants.page1_help_kb),
            disable_web_page_preview=True,
        )
    elif qdata == "page2":
        await q.message.edit_text(
            Constants.page2_help,
            reply_markup=ikb(Constants.page2_help_kb),
            disable_web_page_preview=True,
        )
    await q.answer()
