import telebot
#from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from telebot import types
from model2 import Chat
from Strings import *
bot = telebot.TeleBot('8143938532:AAGpvzm61zGrHOpdxQxWb4-NhbD1epyNk4s')
medical_chat_id = -4574195928
chat_bot = None
@bot.message_handler(commands = ['start'])
def start(message):
    global chat_bot
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

@bot.message_handler(content_types=['text'])
def main(message):
    global chat_bot
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
        chat_bot.add_message("Напиши краткую сводку по моему состоянию именно в таком виде, в котором её можно будет отправить врачув")
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
    if message.text == "Закончить диалог":
        bot.send_message(message.chat.id, "Спасибо, что воспользовались нашими услугами!")
        chat_bot = None
    if chat_bot is None:
        pass
    chat_bot.add_message(message.text)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Закончить диалог")
    btn2 = types.KeyboardButton("Консультация с дежурным врачом")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, chat_bot.get_answer(),reply_markup=markup)



bot.infinity_polling()
