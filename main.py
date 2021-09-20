# (c) @AbirHasan2005
# I just made this for searching a channel message from inline.
# Maybe you can use this for something else.
# I first made this for @AHListBot ...
# Edit according to your use.

from configs import Config
from pyrogram import Client, filters, idle
from pyrogram.errors import QueryIdInvalid
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, InlineQuery, InlineQueryResultArticle, \
    InputTextMessageContent

# Bot Client for Inline Search
Bot = Client(
    session_name=Config.BOT_SESSION_NAME,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)
# User Client for Searching in Channel.
User = Client(
    session_name=Config.USER_SESSION_STRING,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH
)


@Bot.on_message(filters.private & filters.command("start"))
async def start_handler(_, event: Message):
    await event.reply_text(
        "Hi, I am Messages Search Bot!\n\n"
        "**Made By:** Substitute\n"
        "**Bot For:** @For_Otaku",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("💫JOIN ANIME CHANNEL💫", url="https://t.me/For_Otaku"),
             InlineKeyboardButton("✨ANIME CHAT✨", url="https://t.me/fateunionchat")],
            [InlineKeyboardButton("⚡ONGOING CHANNEL⚡", url="https://t.me/Otaku_union_ongoing)],
            [InlineKeyboardButton("Search Inline", switch_inline_query_current_chat=""), InlineKeyboardButton("Go Inline", switch_inline_query="")]
        ])
    )


@Bot.on_inline_query()
async def inline_handlers(_, event: InlineQuery):
    answers = list()
    # If Search Query is Empty
    if event.query == "":
        answers.append(
            InlineQueryResultArticle(
                title="This is Inline Messages Search Bot!",
                description="You can search Channel All Messages using this bot.",
                input_message_content=InputTextMessageContent(
                    message_text="This Bot Is Made To Search Anime In An Efficient Way On @For_Otaku\n\n"
                                 "Made by Substitute",
                    disable_web_page_preview=True
                ),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Search Here", switch_inline_query_current_chat="")],
                    [InlineKeyboardButton("💫ANIME CHANNEL💫", url="https://t.me/for_otaku"),
                     InlineKeyboardButton("✨CHAT GROUP✨", url="https://t.me/fateunionchat")],
                    [InlineKeyboardButton("⚡ONGOING CHANNEL⚡", url="https://t.me/otaku_union_ongoing")]
                ])
            )
        )
    # Search Channel Message using Search Query Words
    else:
        async for message in User.search_messages(chat_id=Config.CHANNEL_ID, limit=50, query=event.query):
            if message.text:
                answers.append(InlineQueryResultArticle(
                    title="{}".format(message.text.split("\n", 1)[0]),
                    description="{}".format(message.text.rsplit("\n", 1)[-1]),
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Search Again", switch_inline_query_current_chat="")]]),
                    input_message_content=InputTextMessageContent(
                        message_text=message.text.markdown,
                        parse_mode="markdown",
                        disable_web_page_preview=True
                    )
                ))
    try:
        await event.answer(
            results=answers,
            cache_time=0
        )
        print(f"[{Config.BOT_SESSION_NAME}] - Answered Successfully - {event.from_user.first_name}")
    except QueryIdInvalid:
        print(f"[{Config.BOT_SESSION_NAME}] - Failed to Answer - {event.from_user.first_name}")

# Start Clients
Bot.start()
User.start()
# Loop Clients till Disconnects
idle()
# After Disconnects,
# Stop Clients
Bot.stop()
User.stop()
