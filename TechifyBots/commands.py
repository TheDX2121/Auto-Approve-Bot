import random
from pyrogram import Client, filters, enums
from pyrogram.errors import *
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from config import *
import asyncio
from Script import text
from .database import tb

@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    if await tb.get_user(message.from_user.id) is None:
        await tb.add_user(message.from_user.id, message.from_user.first_name)
        bot = await client.get_me()
        await client.send_message(
            LOG_CHANNEL,
            text.LOG.format(
                message.from_user.id,
                getattr(message.from_user, "dc_id", "N/A"),
                message.from_user.first_name or "N/A",
                f"@{message.from_user.username}" if message.from_user.username else "N/A",
                bot.username
            )
        )
    await message.reply_photo(
        photo=random.choice(PICS),
        caption=text.START.format(message.from_user.mention),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('⇆ 𝖠𝖽𝖽 𝖬𝖾 𝖳𝗈 𝖸𝗈𝗎𝗋 𝖦𝗋𝗈𝗎𝗉 ⇆', url=f"https://telegram.me/RitsamApprovebot?startgroup=true&admin=invite_users")],
            [InlineKeyboardButton('ℹ️ 𝖠𝖻𝗈𝗎𝗍', callback_data='about'),
             InlineKeyboardButton('📚 𝖧𝖾𝗅𝗉', callback_data='help')],
            [InlineKeyboardButton('⇆ 𝖠𝖽𝖉 𝖬𝖾 𝖳𝗈 𝖸𝗈𝗎𝖗 𝖢𝖍𝖆𝖓𝖓𝖊𝖑 ⇆', url=f"https://telegram.me/RitsamApprovebot?startchannel=true&admin=invite_users")]
        ])
    )

@Client.on_message(filters.command("help") & filters.private)
async def help_cmd(client, message):
    tb = await message.reply("❓ <b>𝘏𝘢𝘷𝘪𝘯𝘨 𝘛𝘳𝘰𝘶𝘣𝘭𝘦?</b>\n\n𝘐𝘧 𝘺𝘰𝘶'𝘳𝘦 𝘧𝘢𝘤𝘪𝘯𝘨 𝘢𝘯𝘺 𝘱𝘳𝘰𝘣𝘭𝘦𝘮 𝘤𝘰𝘯𝘵𝘢𝘤𝘵 𝘴𝘶𝘱𝘱𝘰𝘳𝘵.")
    await asyncio.sleep(300)
    await tb.delete()
    try:
        await message.delete()
    except:
        pass

@Client.on_message(filters.command('accept') & filters.private)
async def accept(client, message):
    show = await message.reply("**Please Wait.....**")
    user_data = await tb.get_session(message.from_user.id)
    if user_data is None:
        return await show.edit("**To accept join requests, please /login first.**")
    try:
        acc = Client("joinrequest", session_string=user_data, api_id=API_ID, api_hash=API_HASH)
        await acc.connect()
    except:
        return await show.edit("**Your login session has expired. Use /logout first, then /login again.**")
    await show.edit("**Forward a message from your Channel or Group (with forward tag).\n\nMake sure your logged-in account is an admin there with full rights.**")
    fwd_msg = await client.listen(message.chat.id)
    if fwd_msg.forward_from_chat and fwd_msg.forward_from_chat.type not in [enums.ChatType.PRIVATE, enums.ChatType.BOT]:
        chat_id = fwd_msg.forward_from_chat.id
        try:
            info = await acc.get_chat(chat_id)
        except:
            return await show.edit("**Error: Ensure your account is admin in this Channel/Group with required rights.**")
    else:
        return await message.reply("**Message not forwarded from a valid Channel/Group.**")
    await fwd_msg.delete()
    msg = await show.edit("**Accepting all join requests... Please wait.**")
    try:
        while True:
            await acc.approve_all_chat_join_requests(chat_id)
            await asyncio.sleep(1)
            join_requests = [req async for req in acc.get_chat_join_requests(chat_id)]
            if not join_requests:
                break
        await msg.edit("**✅ Successfully accepted all join requests.**")
    except Exception as e:
        await msg.edit(f"**An error occurred:** `{str(e)}`")

@Client.on_chat_join_request()
async def approve_new(client, m):
    if not NEW_REQ_MODE:
        return
    try:
        await client.approve_chat_join_request(m.chat.id, m.from_user.id)
        try:
            # Static 2x2 grid buttons with manual public channel URLs
            buttons = [
                [
                    InlineKeyboardButton("✅ Channel 1", url="https://t.me/RitsamHub"),
                    InlineKeyboardButton("✅ Channel 2", url="https://t.me/Vrubhi")
                ],
                [
                    InlineKeyboardButton("✅ Channel 3", url="https://t.me/Vebanu"),
                    InlineKeyboardButton("✅ Channel 4", url="https://t.me/Vebanu_x")
                ]
            ]
            
            # Send photo (from PICS variable) with caption and buttons
            await client.send_photo(
                m.from_user.id,
                photo=PICS[0] if PICS else "https://i.ibb.co/zVwBJ9Sd/IMG-20260331-124835-571.jpg",
                caption=f"{m.from_user.mention},\n\nYour request to join {m.chat.title} has been accepted!",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        except:
            pass
    except Exception as e:
        print(str(e))
        pass