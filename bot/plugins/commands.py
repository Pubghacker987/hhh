from pyrogram import filters
from pyrogram.types import CallbackQuery, Message
from bot.config import Messages



@Client.on_message(
    filters.command("start") & filters.private,
)
async def start_bot(_, m: Message):
    return await m.reply_text(
        Messages.START_MSG.format(m.from_user.first_name, Messages.CAPTION),
        reply_markup=Messages.START_BUTTONS,
        disable_web_page_preview=True,
        quote=True,
    )


@Client.on_message(
    filters.command("help") & filters.private,
)
async def help_bot(_, m: Message):
    return await m.reply_text(
        Messages.HELP_MSG,
        reply_markup=Messages.HELP_BUTTONS,
        disable_web_page_preview=True,
    )



