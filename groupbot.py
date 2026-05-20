from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

import requests

# ============================================
# BOT CONFIG
# ============================================

BOT_TOKEN = "8801949889:AAF71zkfUnH1ZiHYGyZTzHAKfQwagT7lDdA"

# CHANNEL USERNAME
CHANNEL_USERNAME = "@wingcodepartnerofficial"

# SUPPORT GROUP LINK
GROUP_LINK = "https://t.me/numberrinformation"

# SUPPORT GROUP ID
SUPPORT_GROUP_ID = -1003820245087

# ADMIN USER ID
ADMIN_ID = 8519622120


# AADHAR API
AADHAR_API = "YOUR_AADHAR_API"

# ============================================
# CHECK GROUP + CHANNEL JOIN
# ============================================

async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # ONLY SUPPORT GROUP
    if update.effective_chat.id != SUPPORT_GROUP_ID:

        keyboard = [
            [
                InlineKeyboardButton(
                    "👥 JOIN SUPPORT GROUP",
                    url=GROUP_LINK
                )
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "⚠️This Bot is Only Group🔒\n\n"
        "👇Click The Link And Join Our Group🔥\n\n"
        "• Use Our Service For Free💪 \n\n",
            reply_markup=reply_markup
        )

        return False

    user_id = update.effective_user.id

    try:

        member = await context.bot.get_chat_member(
            chat_id=CHANNEL_USERNAME,
            user_id=user_id
        )

        if member.status in [
            "member",
            "administrator",
            "creator"
        ]:

            return True

        else:

            keyboard = [
                [
                    InlineKeyboardButton(
                        "📢 JOIN CHANNEL",
                        url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}"
                    )
                ]
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(
                "**🔒ACESS DENIED ⚠️**\n\n"
           "📌you Must Join In our channel to use our commands\n\n"                         "👇click Bellow Join Channel🔑\n\n"
           "After Joining Channel /start The bot and Use our Service❤️\n\n.",
                reply_markup=reply_markup
            )

            return False

    except:
        return False


# ============================================
# START COMMAND
# ============================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    joined = await check_join(update, context)

    if not joined:
        return

    text = """
🤖 WELCOME TO OSINT BOT

AVAILABLE COMMANDS:

/help
/num <number> Number Intelligence 
/aadhar <aadhar_number> Aadhar Intelligence

EXAMPLES:

/num 9876543210
/aadhar 123412341234
"""

    await update.message.reply_text(text)


# ============================================
# HELP COMMAND
# ============================================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    joined = await check_join(update, context)

    if not joined:
        return

    text = """
📌 AVAILABLE COMMANDS

/num <number> Number Intelligence 
/aadhar <aadhar_number> Aadhar Intelligence 

ADMIN COMMANDS:

/ping
/stats
/broadcast

EXAMPLES:

/num 9876543210
/vehicle AP09AB1234
/aadhar 123412341234
"""

    await update.message.reply_text(text)

# ============================================
# NUMBER COMMAND
# ============================================

async def num(update: Update, context: ContextTypes.DEFAULT_TYPE):

    joined = await check_join(update, context)

    if not joined:
        return

    if len(context.args) == 0:

        await update.message.reply_text(
            "❌ Usage:\n/num 9876543210"
        )

        return

    number = context.args[0]

    url = f"https://nv6.ek4nsh.in/api/proxy?num={number}"

    try:

        response = requests.get(url)

        if response.status_code != 200:

            await update.message.reply_text(
                "❌ Number data not found."
            )

            return

        data = response.json()

        # CHECK RESULTS
        if "results" not in data:

            await update.message.reply_text(
                "❌ Number data not found."
            )

            return

        results = data["results"]

        if not results:

            await update.message.reply_text(
                "❌ Number data not found."
            )

            return

        result_text = f"📱 Number Search Results for: {number}\n"

        count = 1

        for item in results:

            result_text += f"""

━━━━━━━━━━━━━━━
🔎 Result {count}

👤 Name: {item.get('name', 'N/A')}
👨 Father: {item.get('fname', 'N/A')}
📞 Alt: {item.get('alt', 'N/A')}
🪪 Aadhar: {item.get('id', 'N/A')}

📌 Address:
{item.get('address', 'N/A')}

📡 Circle: {item.get('circle', 'N/A')}
📧 Email: {item.get('email', 'N/A')}
"""

            count += 1

        await update.message.reply_text(result_text)

    except Exception as e:

        await update.message.reply_text(
            f"❌ Number data not found.\n\n{e}"
        )


# ============================================
# AADHAR COMMAND
# ============================================

async def aadhar(update: Update, context: ContextTypes.DEFAULT_TYPE):

    joined = await check_join(update, context)

    if not joined:
        return

    if len(context.args) == 0:

        await update.message.reply_text(
            "❌ Usage:\n/aadhar 123412341234"
        )

        return

    aadhar_number = context.args[0]

    url = f"{AADHAR_API}{aadhar_number}"

    try:

        response = requests.get(url)

        if response.status_code == 200:

            text = response.text

            if (
                "not found" in text.lower()
                or "false" in text.lower()
                or text.strip() == ""
            ):

                await update.message.reply_text(
                    "❌ Aadhar data not found."
                )

                return

            await update.message.reply_text(
                f"🪪 AADHAR RESULT:\n\n{text}"
            )

        else:

            await update.message.reply_text(
                "❌ Aadhar data not found."
            )

    except Exception:

        await update.message.reply_text(
            "❌ Aadhar data not found."
        )


# ============================================
# ADMIN COMMAND : PING
# ============================================

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    await update.message.reply_text(
        "✅ BOT IS ONLINE"
    )


# ============================================
# ADMIN COMMAND : STATS
# ============================================

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    await update.message.reply_text(
        f"""
📊 BOT STATS

GROUP ID:
{SUPPORT_GROUP_ID}

CHANNEL:
{CHANNEL_USERNAME}

BOT STATUS:
ONLINE ✅
"""
    )


# ============================================
# ADMIN COMMAND : BROADCAST
# ============================================

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    if len(context.args) == 0:

        await update.message.reply_text(
            "❌ Usage:\n/broadcast message"
        )

        return

    message = " ".join(context.args)

    try:

        await context.bot.send_message(
            chat_id=SUPPORT_GROUP_ID,
            text=f"📢 ADMIN MESSAGE\n\n{message}"
        )

        await update.message.reply_text(
            "✅ Broadcast sent successfully."
        )

    except Exception as e:

        await update.message.reply_text(
            f"❌ Error:\n{e}"
        )


# ============================================
# MAIN
# ============================================

def main():

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # USER COMMANDS
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("num", num))
    app.add_handler(CommandHandler("aadhar", aadhar))

    # ADMIN COMMANDS
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("broadcast", broadcast))

    print("================================")
    print(" BOT IS RUNNING SUCCESSFULLY ")
    print("================================")

    app.run_polling()


# ============================================

if __name__ == "__main__":
    main()
