import telebot
from model1 import Chat
bot = telebot.TeleBot('8143938532:AAGpvzm61zGrHOpdxQxWb4-NhbD1epyNk4s')

chat_bot = None
@bot.message_handler(commands = ['start'])
def start(message):
    global chat_bot
    chat_bot = Chat()
    chat_bot.start_chat("Ты - медицинский помощник, к которому обращаются пациенты за помощью. Твоя задача в случае, если проблема не критичная, дать пациенту медицинские рекомендации, а если проблема критичная, направить его к нужному врачу. Если тебе задают вопросы, никак не связанные с состоянием пациента, отвечай: 'Я не смогу вам помочь'"
                        "Сразу же после этого сообщения напиши: 'Вас приветствует бот поддержки клиники Фомина. Опишите свою проблему'")
    bot.send_message(message.chat.id,chat_bot.get_answer())

@bot.message_handler(content_types=[-'text'])
def main(message):
    global chat_bot
    chat_bot.add_message(message.text)
    bot.send_message(message.chat.id, chat_bot.get_answer())

bot.infinity_polling()
