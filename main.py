import telebot
from telebot import types
from telebot.types import ReplyKeyboardMarkup
import database
from database import show_users_from_db, is_name_and_streak, add_user_to_db

bot = telebot.TeleBot('8219633615:AAFW_6GsVXxvPhKBRrLRRS_XQtAaSHy8D2I')


@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    hello_btn = types.KeyboardButton(text="хуй")
    markup.add(hello_btn)
    bot.send_message(message.chat.id, "Привет {}, напиши старт если хочешь пройти дальше!".format(message.from_user.first_name), reply_markup=markup)


@bot.message_handler(content_types=["text"])
def get_text(message):
    if message.text == "старт":
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text="Узнать стрик")
        btn2 = types.KeyboardButton(text="Посмотреть лидерборд")
        btn3 = types.KeyboardButton(text="Ссылка на фурри порно!")
        btn4 = types.KeyboardButton(text="Записаться в бота")
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, "Чего тебе?", reply_markup=markup)


    elif message.text == "Узнать стрик":
        bot.send_message(message.chat.id, "функция не работает ¯_(ツ)_/¯ LOL")


    elif message.text == "Посмотреть лидерборд":
        show_users_from_db(bot, message)


    elif message.text == "Ссылка на фурри порно!":
        bot.send_message(message.chat.id, "охох, сосунооок, [держи)](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%2Fid%2FOIP.rZGj_gJShU8yYjGuWDpt5wHaEK%3Fpid%3DApi&f=1&ipt=29e6c7334085381777a48c20c77245bd685f1eb48daf011beb29f68c5df73b64&ipo=images)", parse_mode='Markdown')


    elif message.text == "Записаться в бота":
        bot.send_message(message.chat.id, "Напиши имя и текущий стрик. Например: Вован 0")

    #если человек написал имя и текущий стрик
    elif is_name_and_streak(message.text):
            add_user_to_db(message.from_user, message.text.split()[0], message.text.split()[1])
            bot.send_message(message.chat.id, 'окей, ты записан, напиши "Узнать стрик"')


    else:
        bot.send_message(message.chat.id, "idk what you want ¯_(ツ)_/¯ LOL")


bot.polling(none_stop=True, interval=0)