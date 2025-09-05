import telebot
from telebot import types
from telebot.types import ReplyKeyboardMarkup
from bot_db_handler import *
import time

bot = telebot.TeleBot('8219633615:AAFW_6GsVXxvPhKBRrLRRS_XQtAaSHy8D2I')

sort_streaks("streaks.json")
reply_info = ("/add - добавиться в бота\n" +
              "/lb - посмотреть лидерборд\n" +
              "/streak - посмотреть свой стрик\n" +
              "/get - получить переменную\n" +
              "/set - поменять переменную\n" +
              "/reset - ресетнуть стрик\n\n" +
              "🤓Список переменных для /get и /set:\n" +
              "   streak - стрик\n" +
              "   name - имя\n" +
              "   desc - описание\n")

user_states = {}

@bot.message_handler(commands=["start"])
def start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    btn_add = types.KeyboardButton(text="/add")
    btn_lb = types.KeyboardButton(text="/lb")
    btn_streak = types.KeyboardButton(text="/streak")
    btn_get = types.KeyboardButton(text="/get")
    btn_set = types.KeyboardButton(text="/set")
    btn_reset = types.KeyboardButton(text="/reset")

    markup.add(btn_add, btn_lb, btn_streak, btn_get, btn_set, btn_reset)

    bot.send_message(message.chat.id, reply_info, reply_markup=markup)

    user_states[message.from_user.id] = None


@bot.message_handler(commands=["help"])
def help_user(message):
    bot.send_message(message.chat.id, reply_info)
    user_states[message.from_user.id] = None


@bot.message_handler(commands=["lb"])
def handle_lb(message):
    send_streaks(bot, message)
    user_states[message.from_user.id] = None


#fast streak function
@bot.message_handler(commands=["streak"])
def handle_streak(message):
    send_user_streak(bot, message)
    user_states[message.from_user.id] = None



@bot.message_handler(commands=["reset"])
def handle_reset_command(message):
    set_variable("streaks.json", str(message.from_user.id), "streak_num", "0")
    bot.send_message(message.chat.id, "streak reset")

    user_states[message.from_user.id] = None



#get any variable, not fast but strong
@bot.message_handler(commands=["get"])
def handle_get_command(message):
    user_states[message.from_user.id] = "Waiting for variable to get"
    bot.send_message(message.chat.id, "write: 'variable' or 'username' 'variable'")


@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == "Waiting for variable to get")
def handle_get_input(message):
    text = message.text

    if len(text.split()) == 1:
        send_variable(bot, str(message.from_user.id), message, text)

    elif len(text.split()) == 2:
        user_name = text.split()[0]
        variable = text.split()[1]

        user_id = find_id_by_name("streaks.json", user_name)

        send_variable(bot, user_id, message, variable)


    user_states[message.from_user.id] = None


#set allowed variables, not fast, but strong
@bot.message_handler(commands=["set"])
def handle_set_command(message):
    user_states[message.from_user.id] = "Waiting for variable to set"
    bot.send_message(message.chat.id, "write: 'variable' 'value'")


@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == "Waiting for variable to set")
def handle_set_input(message):
    text = message.text

    if len(text.split()) >= 2:
        variable = text.split()[0]
        value = text[(len(variable) + 1):]

        #check for shortenings
        variable = decipher_shortenings(variable)

        if is_var_safe_to_change(variable, value):
            set_variable("streaks.json", str(message.from_user.id), variable, value)
            bot.send_message(message.chat.id, "set " + variable + " to " + value)

        else:
            #write only if user misspelled the first word or type of the second is incorrect
            if len(text.split()) == 2: bot.send_message(message.chat.id, "no such variable or wrong type")

    user_states[message.from_user.id] = None



@bot.message_handler(commands=["add"])
def handle_add_command(message):
    user_states[message.from_user.id] = "Waiting for variables to add"
    bot.send_message(message.chat.id, "Write: 'name' 'streak'")


@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == "Waiting for variables to add")
def handle_add_input(message):
    text = message.text
    if len(text.split()) == 2 and is_name_and_streak(text):
        user_streak = convert_reply_to_streak(message)
        add_streak("streaks.json", user_streak)
        bot.send_message(message.chat.id, "streak added")
    user_states[message.from_user.id] = None


# @bot.message_handler(content_types=["text"])
# def handle_text(message):
    # if message.text == "/streak" or message.text == "/стрик":
    #     send_user_streak(bot, message)
    #
    # elif message.text == "/leaderboard" or message.text == "/лидерборд" or message.text == "/lb":
    #     send_streaks(bot, message)


    # elif is_add_name_and_streak(message.text):
    #     user_streak = convert_reply_to_streak(message)
    #     add_streak("streaks.json", user_streak)
    #     bot.send_message(message.chat.id, "streak added")
    #
    # #if message is: name "name"
    # elif is_change_name(message.text):
    #     user_streak = get_streak_by_id("streaks.json", str(message.from_user.id))
    #     update_name("streaks.json", user_streak, message.text.split()[1])
    #     bot.send_message(message.chat.id, "name changed")
    #
    # elif is_change_description(message.text):
    #     update_description("streaks.json", str(message.from_user.id), message.text[19:])


    #OLD GET FUNCTIONS

    # elif message.text == "/get_desc":
    #     description = get_streak_by_id("streaks.json", str(message.from_user.id)).description
    #     if description != "":
    #         bot.send_message(message.chat.id, description)
    #     else:
    #         bot.send_message(message.chat.id, "You dont have description")

    # elif message.text.split()[0] == "/get" and len(message.text.split()) == 2:
    #     send_variable(bot, str(message.from_user.id), message, message.text.split()[1])
    #
    # elif message.text.split()[0] == "/get" and len(message.text.split()) == 3:
    #     user_id = find_id_by_name("streaks.json", message.text.split()[1])
    #     send_variable(bot, user_id, message, message.text.split()[2])


while True:
    try:
        bot.polling(non_stop=True, interval=1)
    except Exception as e:
        user_states = {}
        print(datetime.now(), e)
        time.sleep(5)
        continue