import telebot
import random
import os

# دریافت توکن از متغیر محیطی برای امنیت بیشتر
TOKEN = os.getenv("BOT_TOKEN")  
bot = telebot.TeleBot(TOKEN)

# ذخیره شناسه‌ها و کاربران
anonymous_messages = {}

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "👋 سلام! این یک ربات پیام ناشناس است.\n\n"
                                      "🔹 برای دریافت شناسه ناشناس: /getid\n"
                                      "🔹 برای ارسال پیام ناشناس: /send شناسه پیام")

@bot.message_handler(commands=["getid"])
def get_id(message):
    anon_id = str(random.randint(10000, 99999))  # تولید شناسه تصادفی
    anonymous_messages[anon_id] = message.chat.id  # ذخیره شناسه و چت‌آی‌دی
    bot.send_message(message.chat.id, f"🆔 شناسه ناشناس شما: `{anon_id}`\n"
                                      "🔹 این شناسه را به دیگران بدهید تا برای شما پیام ارسال کنند.", parse_mode="Markdown")

@bot.message_handler(commands=["send"])
def send_anonymous(message):
    try:
        parts = message.text.split(" ", 2)
        if len(parts) < 3:
            bot.send_message(message.chat.id, "⚠️ فرمت اشتباه! مثال:\n`/send 12345 سلام!`", parse_mode="Markdown")
            return

        anon_id, msg = parts[1], parts[2]  # دریافت شناسه و پیام
        if anon_id in anonymous_messages:
            receiver_id = anonymous_messages[anon_id]  # پیدا کردن دریافت‌کننده پیام
            bot.send_message(receiver_id, f"📩 *پیام ناشناس دریافت شد:*\n\n_{msg}_", parse_mode="Markdown")
            bot.send_message(message.chat.id, "✅ پیام شما ارسال شد!")
        else:
            bot.send_message(message.chat.id, "❌ شناسه یافت نشد!")
    except Exception as e:
        bot.send_message(message.chat.id, "❌ خطایی رخ داد!")

bot.polling()
