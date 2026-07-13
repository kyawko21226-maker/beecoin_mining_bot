import telebot
import random
import time
import os
from flask import Flask
from threading import Thread

TOKEN = "8725569296:AAGAiZvDpvzgJkO-0El7R37RxYDHrboddX0"
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive!"

users = {}

@bot.message_handler(commands=['start'])
def start(message):
    users[message.chat.id] = {"coin": 0}
    bot.reply_to(message, "🚀 Welcome to BeeCoin Bot!\nUse /mine")

@bot.message_handler(commands=['mine'])
def mine(message):
    user = users.get(message.chat.id)
    if not user:
        bot.reply_to(message, "Type /start first")
        return

    earn = round(random.uniform(0.01, 0.05), 3)
    user["coin"] += earn
    bot.reply_to(message, f"⛏ You mined {earn} BEE!")

def run_bot():
    bot.infinity_polling()

def run():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT

def keep_alive():
    Thread(target=run).start()

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable not found.")

bot = telebot.TeleBot(TOKEN)

users = {}

def get_user(chat_id):
    if chat_id not in users:
        users[chat_id] = {
            "coins": 0,
            "usdt": 0.0,
            "last_daily": 0,
            "watching_ad": False,
            "pending_reward": 0
        }
    return users[chat_id]

@bot.message_handler(commands=["start"])
def start(message):
    get_user(message.chat.id)
    bot.reply_to(
        message,
        "🐝 Welcome to BeeCoin Bot!\n\n"
        "/daily - Daily Bonus\n"
        "/ads - Watch Ads\n"
        "/balance - Balance\n"
        "/exchange - Exchange Coins\n"
        "/withdraw - Withdraw"
    )

@bot.message_handler(commands=["daily"])
def daily_bonus(message):
    user = get_user(message.chat.id)
    now = time.time()

    if now - user["last_daily"] < 86400:
        bot.reply_to(message, "⏳ Daily bonus မရသေးပါ။")
        return

    user["coins"] += 10
    user["last_daily"] = now
    bot.reply_to(message, "🎁 +10 Coins")

@bot.message_handler(commands=["ads"])
def ads(message):
    user = get_user(message.chat.id)

    if user["watching_ad"]:
        bot.reply_to(message, "⚠️ Ad ကြည့်နေပါတယ်။")
        return

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Ad 1", callback_data="ad_1"))
    markup.add(types.InlineKeyboardButton("Ad 2", callback_data="ad_2"))
    markup.add(types.InlineKeyboardButton("Ad 3", callback_data="ad_3"))

    bot.send_message(message.chat.id, "ရွေးပါ", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data.startswith("ad_"))
def watch_ad_callback(call):
    user = get_user(call.message.chat.id)

    rewards = {
        "ad_1": (10, 5),
        "ad_2": (10, 3),
        "ad_3": (5, 2)
    }

    duration, reward = rewards[call.data]

    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, f"📺 {duration} sec...")

    time.sleep(duration)

    user["coins"] += reward

    bot.send_message(call.message.chat.id, f"✅ +{reward} Coins")

@bot.message_handler(commands=["balance"])
def balance(message):
    user = get_user(message.chat.id)

    bot.reply_to(
        message,
        f"💰 Balance\n\n"
        f"🪙 Coins: {user['coins']}\n"
        f"💵 USDT: {user['usdt']:.3f}"
    )


@bot.message_handler(commands=["exchange"])
def exchange(message):
    user = get_user(message.chat.id)

    if user["coins"] < 10:
        bot.reply_to(message, "❌ အနည်းဆုံး 10 Coins လိုပါတယ်။")
        return

    groups = user["coins"] // 10
    coins_used = groups * 10
    usdt = groups * 0.001

    user["coins"] -= coins_used
    user["usdt"] += usdt

    bot.reply_to(
        message,
        f"✅ {coins_used} Coins → {usdt:.3f} USDT"
    )


@bot.message_handler(commands=["withdraw"])
def withdraw(message):
    user = get_user(message.chat.id)

    args = message.text.split()

    if len(args) != 3:
        bot.reply_to(
            message,
            "အသုံးပြုပုံ:\n/withdraw ADDRESS AMOUNT"
        )
        return

    address = args[1]

    try:
        amount = float(args[2])
    except ValueError:
        bot.reply_to(message, "❌ Amount မှားနေပါတယ်။")
        return

    if amount < 0.05:
        bot.reply_to(message, "❌ အနည်းဆုံး 0.05 USDT ထုတ်နိုင်ပါတယ်။")
        return

    if user["usdt"] < amount:
        bot.reply_to(message, "❌ Balance မလုံလောက်ပါ။")
        return

    fee = 0.01
    receive = amount - fee

    user["usdt"] -= amount

    bot.reply_to(
        message,
        f"✅ Withdraw Request\n\n"
        f"Address:\n{address}\n\n"
        f"Amount: {amount:.3f} USDT\n"
        f"Fee: {fee:.2f} USDT\n"
        f"You Receive: {receive:.3f} USDT\n\n"
        f"Admin မှ စစ်ဆေးပြီး လွှဲပေးပါမည်။"
    )


if __name__ == "__main__":
    keep_alive()
    print("Bot started...")
    bot.infinity_polling(skip_pending=True)
