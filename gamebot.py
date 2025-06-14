import telebot
from telebot import types
import random
import threading
import os
from flask import Flask, request

TOKEN = "8000562573:AAFqDqdnhr84hRcxl_wz-3sUpx3EmW0cdA8"
bot = telebot.TeleBot(TOKEN)
WEBHOOK_URL = "https://gamebot-1234.onrender.com"

questions = [
    "Назви 5 марок автомобілів",
    "Назви 5 країн Європи",
    "Назви 5 тварин Африки",
    "Назви 5 перших страв",
    "Назви 5 видів транспорту",
    "Назви 5 голлівудських зірок",
    "Назви 5 річок України",
    "Назви 5 кольорів",
    "Назви 5 фруктів",
    "Назви 5 овочів",
    "Назви 5 міст України",
    "Назви 5 видів спорту",
    "Назви 5 океанів або морів",
    "Назви 5 країн Азії",
    "Назви 5 предметів у школі",
    "Назви 5 тварин, які живуть у лісі",
    "Назви 5 музичних інструментів",
    "Назви 5 жанрів фільмів",
    "Назви 5 квітів",
    "Назви 5 мов світу",
    "Назви 5 гірських вершин",
    "Назви 5 свят",
    "Назви 5 видів одягу",
    "Назви 5 комп’ютерних ігор",
    "Назви 5 мультфільмів",
    "Назви 5 видів чаю",
    "Назви 5 планет",
    "Назви 5 пор року",
    "Назви 5 українських пісень",
    "Назви 5 письменників",
    "Назви 5 фільмів про супергероїв",
    "Назви 5 тварин з ферми",
    "Назви 5 типів транспорту",
    "Назви 5 смартфонів",
    "Назви 5 видів спорядження для кемпінгу",
    "Назви 5 хобі",
    "Назви 5 способів пересування",
    "Назви 5 парних предметів",
    "Назви 5 емоцій",
    "Назви 5 книг",
    "Назви 5 міст в Америці",
    "Назви 5 напоїв",
    "Назви 5 видів м’яса",
    "Назви 5 птахів",
    "Назви 5 ссавців",
    "Назви 5 риб",
    "Назви 5 казкових персонажів",
    "Назви 5 страв з картоплі",
    "Назви 5 видів сиру",
    "Назви 5 марок одягу",
    "Назви 5 солодощів",
    "Назви 5 фільмів Disney",
    "Назви 5 мов програмування",
    "Назви 5 знаменитостей з YouTube",
    "Назви 5 спортивних команд",
    "Назви 5 настільних ігор",
    "Назви 5 країн Африки",
    "Назви 5 фільмів про любов",
    "Назви 5 професій"
]

active_questions = {}

@bot.message_handler(commands=['start'])
def start_game(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Нова гра"))
    bot.send_message(message.chat.id, "Привіт! Натисни 'Нова гра', щоб розпочати.", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Нова гра")
def new_game(message):
    chat_id = message.chat.id
    active_questions[chat_id] = questions.copy()
    send_question(message)

def send_question(message):
    chat_id = message.chat.id
    if chat_id not in active_questions or not active_questions[chat_id]:
        bot.send_message(chat_id, "Гру завершено! Натисни 'Нова гра', щоб почати спочатку.")
        return

    question = random.choice(active_questions[chat_id])
    active_questions[chat_id].remove(question)
    bot.send_message(chat_id, f"🎯 Завдання:\n{question}\n⏱ У тебе є 10 секунд!")
    threading.Timer(8.0, lambda: bot.send_message(chat_id, "⌛ Час вийшов! Натисни 'Нова гра' або чекай наступне питання.")).start()

app = Flask(__name__)

@app.route('/bot', methods=['POST'])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return '', 200

@app.route('/', methods=['GET'])
def index():
    return 'Бот працює!'

def start_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/bot")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

if __name__ == "__main__":
    start_webhook()
