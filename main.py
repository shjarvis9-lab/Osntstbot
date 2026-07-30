import os
import requests
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Environment Variable se Bot Token load karna (Render me set karein)
BOT_TOKEN = os.getenv("8899435136:AAEMC8MzuLy5E3dm0rcrRqwL0HFX6pp7TuM")
bot = telebot.TeleBot(BOT_TOKEN)

# Start command handler with Inline Buttons
@bot.message_handler(commands=['start'])
def start_command(message):
    user_name = message.from_user.first_name
    
    # Buttons create karna
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    btn_help = InlineKeyboardButton("ℹ️ Help", callback_data="cb_help")
    btn_about = InlineKeyboardButton("👨‍💻 About", callback_data="cb_about")
    markup.add(btn_help, btn_about)

    welcome_text = (
        f"👋 **Namaste {user_name}!**\n\n"
        "Welcome to your multi-purpose Telegram Bot.\n\n"
        "**Commands Available:**\n"
        "• `/start` - Restart the bot\n"
        "• `/check <username>` - GitHub public profile lookup\n"
        "• `/ip <ip_address>` - Public IP location check"
    )
    
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=markup)

# Callback queries handle karna (Buttons par click karne ke liye)
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "cb_help":
        bot.answer_callback_query(call.id, "Help Menu")
        bot.send_message(
            call.message.chat.id, 
            "📌 **How to use:**\n"
            "1. Type `/check octocat` to see GitHub stats.\n"
            "2. Type `/ip 8.8.8.8` to check public IP info."
        )
    elif call.data == "cb_about":
        bot.answer_callback_query(call.id, "About Bot")
        bot.send_message(call.message.chat.id, "🚀 **Bot Status:** Active & Online on Render.")

# Public GitHub Profile Lookup Command
@bot.message_handler(commands=['check'])
def handle_check(message):
    query = message.text.replace('/check', '').strip()
    
    if not query:
        bot.reply_to(message, "⚠️ Usage: `/check <username>` (Example: `/check torvalds`)", parse_mode="Markdown")
        return

    try:
        url = f"https://api.github.com/users/{query}"
        res = requests.get(url)
        
        if res.status_code == 200:
            data = res.json()
            response_text = (
                f"👤 **GitHub User:** {data.get('login')}\n"
                f"🏷️ **Name:** {data.get('name', 'N/A')}\n"
                f"📦 **Public Repos:** {data.get('public_repos')}\n"
                f"👥 **Followers:** {data.get('followers')}\n"
                f"🔗 **Profile:** {data.get('html_url')}"
            )
        else:
            response_text = "❌ User not found."
    except Exception:
        response_text = "⚠️ Service connection error."

    bot.reply_to(message, response_text, parse_mode="Markdown")

# Public IP Info Command
@bot.message_handler(commands=['ip'])
def handle_ip(message):
    ip_input = message.text.replace('/ip', '').strip()
    
    if not ip_input:
        bot.reply_to(message, "⚠️ Usage: `/ip <ip_address>` (Example: `/ip 8.8.8.8`)", parse_mode="Markdown")
        return

    try:
        res = requests.get(f"http://ip-api.com/json/{ip_input}")
        data = res.json()
        
        if data.get('status') == 'success':
            response_text = (
                f"🌐 **IP Address:** {data.get('query')}\n"
                f"🏳️ **Country:** {data.get('country')}\n"
                f"🏙️ **City:** {data.get('city')}\n"
                f"🏢 **ISP:** {data.get('isp')}"
            )
        else:
            response_text = "❌ Invalid IP address."
    except Exception:
        response_text = "⚠️ Unable to fetch IP details."

    bot.reply_to(message, response_text, parse_mode="Markdown")

# Start Bot Listener
if __name__ == '__main__':
    bot.infinity_polling()
