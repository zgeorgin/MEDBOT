
import telebot
#from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from telebot import types
from model2 import Chat
from Strings import *
import sqlite3
bot = telebot.TeleBot('7941203917:AAFi_nyJaxG9s5H1FWagx65oKYzvrjMAHh8')
medical_chat_id = -4574195928
all_users_states = {}
def start_dialog(message):
    global all_users_states
    connection_start = sqlite3.connect('Medbot.db')
    cursor_start = connection_start.cursor()
    cursor_start.execute("SELECT id FROM Users WHERE chat = ?", (message.chat.id,))
    data = cursor_start.fetchall()
    if len(data) == 0:
        cursor_start.execute('INSERT INTO Users (username, chat) VALUES (?, ?)',
                             (message.from_user.username, message.chat.id))
    connection_start.commit()
    connection_start.close()
    chat_bot = Chat()
    prompt = Prompt
    chat_bot.start_chat(prompt)
    btn1 = types.KeyboardButton(text="Экстренный вызов")
    btn2 = types.KeyboardButton(text="Медицинская консультация")
    btn3 = types.KeyboardButton(text="Информация о клинике")
    btn4 = types.KeyboardButton(text="Обратная связь")
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, bot_greetings, reply_markup=keyboard)
    all_users_states[message.chat.id] = {"started": True, "Bot": chat_bot}
connection = sqlite3.connect('Medbot.db')
cursor = connection.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
chat INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Chats (
username TEXT NOT NULL,
chat TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Marks (
username TEXT NOT NULL,
SPEED INTEGER
COMFORT INTEGER
EMOTION INTEGER
PRICE INTEGER
)
''')

@bot.message_handler(commands = ['start'])
def start(message):
    start_dialog(message)

@bot.message_handler(content_types=['text'])
def main(message):
    global all_users_states
    if message.chat.id not in all_users_states.keys():
        start_dialog(message)
    chat_bot = all_users_states[message.chat.id]["Bot"]
    print(message.from_user.username)
    if message.text == "Экстренный вызов":
        bot.send_message(message.chat.id, bot_emergency)
        return
    if message.text == "Медицинская консультация":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Консультация с Лией")
        btn2 = types.KeyboardButton("Консультация с дежурным врачом")
        btn3 = types.KeyboardButton("Запись к врачу")
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id, text="Выберите нужную опцию", reply_markup=markup)
        return
    if message.text == "Консультация с дежурным врачом":
        bot.send_message(message.chat.id, text=bot_consultation_message)
        chat_bot.add_message("Напиши краткую сводку по моему состоянию именно в таком виде, в котором её можно будет отправить врачу")
        bot.send_message(medical_chat_id, text=f"Пользователь {message.from_user.username} нуждается в помощи! Состояние: {chat_bot.get_answer()}")
        return
    if message.text == "Запись к врачу":
        bot.send_message(message.chat.id, text=bot_record_message)
        return
    if message.text == "Информация о клинике":
        bot.send_message(message.chat.id, bot_info_message)
        return
    if message.text == "Обратная связь":
        bot.send_message(message.chat.id, bot_vote_message)
        return
    if message.text == "Закончить диалог":
        bot.send_message(message.chat.id, "Спасибо, что воспользовались нашими услугами!")
        chat_bot = None
        all_users_states[message.chat.id]["started"] = False

    if message.text == "Начать диалог":
        start_dialog(message)
        return
    if chat_bot is None:
        pass

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if all_users_states[message.chat.id]["started"]:
        btn1 = types.KeyboardButton("Закончить диалог")
        btn2 = types.KeyboardButton("Консультация с дежурным врачом")
        chat_bot.add_message(message.text)
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, chat_bot.get_answer(), reply_markup=markup)
    else:
        btn1 = types.KeyboardButton("Начать диалог")
        markup.add(btn1)
        bot.send_message(message.chat.id, text = "Хотите начать новый диалог?", reply_markup=markup)





bot.infinity_polling()
