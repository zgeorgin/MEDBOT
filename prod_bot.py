import telebot
#from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from telebot import types
import threading
from model2 import Chat
from Strings import *
import sqlite3
bot = telebot.TeleBot('7941203917:AAFi_nyJaxG9s5H1FWagx65oKYzvrjMAHh8')
medical_chat_id = -4574195928
all_users_states = {}
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
SPEED INTEGER,
COMFORT INTEGER,
EMOTION INTEGER,
PRICE INTEGER
)
''')
connection.commit()
connection.close()
def start_dialog(message):
    global all_users_states
    lock = threading.Lock()
    with lock:
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
    all_users_states[message.chat.id] = {"started": True, "Bot": chat_bot, "ready": True, "Vote":[-1, -1, -1, -1]}



@bot.message_handler(commands = ['start'])
def start(message):
    start_dialog(message)

@bot.message_handler(content_types=['text'])
def main(message):
    if message.chat.id == medical_chat_id:
        return
    global all_users_states
    if message.chat.id not in all_users_states.keys():
        start_dialog(message)
    lock = threading.Lock()
    new_data = None
    with lock:
        connection_main = sqlite3.connect('Medbot.db')
        cursor_start = connection_main.cursor()
        cursor_start.execute(f"SELECT Chat FROM Chats WHERE username = '{message.from_user.username}'")
        data = cursor_start.fetchall()
        if len(data) == 0:
            cursor_start.execute('INSERT INTO Chats (username, chat) VALUES (?, ?)',
                                 (message.from_user.username, message.text))
            new_data = message.text
        else:
            new_data = data[0][0] + "\n" + message.text
            cursor_start.execute(f"UPDATE Chats SET chat = '{new_data}' WHERE username = '{message.from_user.username}'")
        connection_main.commit()
        connection_main.close()
    chat_bot = all_users_states[message.chat.id]["Bot"]
    print(message.from_user.username)
    if message.text == "Экстренный вызов":
        bot.send_message(message.chat.id, bot_emergency)
        return
    if message.text == "Медицинская консультация":
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton("Консультация с Лией")
        btn2 = types.KeyboardButton("Консультация с дежурным врачом")
        btn3 = types.KeyboardButton("Запись к врачу")
        btn4 = types.KeyboardButton("Возврат в главное меню")
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, text="Выберите нужную опцию", reply_markup=markup)
        return
    if message.text == "Возврат в главное меню":
        start_dialog(message)
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
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("0")
        btn2 = types.KeyboardButton("1")
        btn3 = types.KeyboardButton("2")
        btn4 = types.KeyboardButton("Возврат в главное меню")
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, bot_marks[0], reply_markup=markup)
        all_users_states[message.chat.id]['ready'] = False
        all_users_states[message.chat.id]['Vote'][0] = -2
        return
    if message.text in ['1', '2', '3'] and not all_users_states[message.chat.id]['ready']:
        marks = all_users_states[message.chat.id]['Vote']
        for i in range(len(marks)):
            if marks[i] == -2:
                marks[i] = int(message.text)
                if i == len(marks) - 1:
                    lock = threading.Lock()
                    with lock:
                        connection_vote = sqlite3.connect('Medbot.db')
                        cursor_start = connection_vote.cursor()
                        cursor_start.execute('INSERT INTO Marks (username, SPEED, COMFORT, EMOTION, PRICE) VALUES (?, ?, ?, ?, ?)',
                                             (message.from_user.username, marks[0], marks[1], marks[2], marks[3]))
                        all_users_states[message.chat.id]['ready'] = True
                        connection_vote.commit()
                        connection_vote.close()
                        bot.send_message(message.chat.id, "Большое спасибо за оценку! Она поможет нам стать лучше!")
                        all_users_states[message.chat.id]["started"] = False
                    continue
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton("0")
                btn2 = types.KeyboardButton("1")
                btn3 = types.KeyboardButton("2")
                btn4 = types.KeyboardButton("Возврат в главное меню")
                markup.add(btn1, btn2, btn3, btn4)
                bot.send_message(message.chat.id, bot_marks[i + 1], reply_markup=markup)
                marks[i + 1] = -2
                return

    if message.text == "Закончить диалог":
        bot.send_message(message.chat.id, "Спасибо, что воспользовались нашими услугами!")
        chat_bot = None
        all_users_states[message.chat.id]["started"] = False

    if message.text == "Начать диалог":
        start_dialog(message)
        return

    markup = types.ReplyKeyboardMarkup()
    if not all_users_states[message.chat.id]['ready']:
        return
    if all_users_states[message.chat.id]["started"]:
        btn1 = types.KeyboardButton("Закончить диалог")
        btn2 = types.KeyboardButton("Консультация с дежурным врачом")
        chat_bot.add_message(message.text)
        markup.add(btn1, btn2)
        answer = chat_bot.get_answer()
        bot.send_message(message.chat.id, answer, reply_markup=markup)

        lock = threading.Lock()
        with lock:
            connection_user = sqlite3.connect('Medbot.db')
            cursor_start = connection_user.cursor()
            new_data += "\n" + answer
            cursor_start.execute(f"UPDATE Chats SET chat = '{new_data}' WHERE username = '{message.from_user.username}'")
            connection_user.commit()
            connection_user.close()
    else:
        btn1 = types.KeyboardButton("Начать диалог")
        btn2 = types.KeyboardButton("Обратная связь")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, text = "Хотите начать новый диалог?", reply_markup=markup)





bot.infinity_polling()
