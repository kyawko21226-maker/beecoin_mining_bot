import telebot
import random
import time

TOKEN = "YOUR_BOT_TOKEN"

bot = telebot.TeleBot(TOKEN)

users = {}

@bot.message_handler(commands=['start'])
def start(message):
    users[message.chat.id] = {"coin": 0, "last_mine": 0}
    bot.reply_to(message, "🚀 Welcome to BeeCoin Bot!\n\nCommands:\n/mine - Mine coin\n/balance - Check balance\n/ad - Watch ad")

@bot.message_handler(commands=['mine'])
def mine(message):
    user = users.get(message.chat.id)
    
    if not user:
        bot.reply_to(message, "Type /start first")
        return

    now = time.time()
    if now - user["last_mine"] < 10:
        bot.reply_to(message, "⏳ Wait before mining again!")
        return

    earn = round(random.uniform(0.01, 0.05), 3)
    user["coin"] += earn
    user["last_mine"] = now

    bot.reply_to(message, f"⛏ You mined {earn} BEE!")

@bot.message_handler(commands=['balance'])
def balance(message):
    user = users.get(message.chat.id)
    if user:
        bot.reply_to(message, f"💰 Your balance: {user['coin']} BEE")
    else:
        bot.reply_to(message, "Type /start first")

@bot.message_handler(commands=['ad'])
def ad(message):
    user = users.get(message.chat.id)
    if not user:
        bot.reply_to(message, "Type /start first")
        return

    earn = 0.02
    user["coin"] += earn

    bot.reply_to(message, "📺 You watched an ad and earned 0.02 BEE!")

bot.infinity_polling()
