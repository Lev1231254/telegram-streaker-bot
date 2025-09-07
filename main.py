import telebot
from telebot import types
from telebot.types import ReplyKeyboardMarkup
from bot_db_handler import *
import time, os, logging


logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

db_file = "streaks.json"



bot = telebot.TeleBot(os.environ["telegram-api-token"])

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
    logging.info(str(message.from_user.id) + " " + message.text)

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
    logging.info(str(message.from_user.id) + " " + message.text)

    try:
        bot.send_message(message.chat.id, reply_info)
    except Exception as e:
        logging.error("help_user: "+ str(e))

    user_states[message.from_user.id] = None

@bot.message_handler(commands=["lb"])
def handle_lb(message):
    logging.info(str(message.from_user.id) + " " + message.text)

    try:
        send_streaks(bot, message)
    except Exception as e:
        logging.error("handle_lb: "+ str(e))

    user_states[message.from_user.id] = None


#fast streak function
@bot.message_handler(commands=["streak"])
def handle_streak_command(message):
    logging.info(str(message.from_user.id) + " " + message.text)

    try:
        send_user_streak(bot, message)
    except Exception as e:
        logging.error("handle_streak_command: "+ str(e))

    user_states[message.from_user.id] = None


@bot.message_handler(commands=["reset"])
def handle_reset_command(message):
    logging.info(str(message.from_user.id) + " " + message.text)


    try:
        set_variable(db_file, str(message.from_user.id), "streak_num", "0")
        bot.send_message(message.chat.id, "streak reset")

    except Exception as e:
        logging.error("handle_reset_command: "+ str(e))

    user_states[message.from_user.id] = None

#get any variable, not fast but strong
@bot.message_handler(commands=["get"])
def handle_get_command(message):
    logging.info(str(message.from_user.id) + " " + message.text)

    try:
        user_states[message.from_user.id] = "Waiting for variable to get"
        bot.send_message(message.chat.id, "write: 'variable' or 'username' 'variable'")
    except Exception as e:
        logging.error("handle_get_command: "+ str(e))


@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == "Waiting for variable to get")
def handle_get_input(message):
    logging.info(str(message.from_user.id) + " " + message.text)


    try:
        text = message.text

        if len(text.split()) == 1:
            send_variable(bot, str(message.from_user.id), message, text)

        elif len(text.split()) == 2:
            user_name = text.split()[0]
            variable = text.split()[1]

            user_id = find_id_by_name(db_file, user_name)

            send_variable(bot, user_id, message, variable)
    except Exception as e:
        logging.error("handle_get_input: "+ str(e))

    user_states[message.from_user.id] = None


#set allowed variables, not fast, but strong
@bot.message_handler(commands=["set"])
def handle_set_command(message):
    logging.info(str(message.from_user.id) + " " + message.text)

    try:
        user_states[message.from_user.id] = "Waiting for variable to set"
        bot.send_message(message.chat.id, "write: 'variable' 'value'")
    except Exception as e:
        logging.error("handle_set_command: "+ str(e))


@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == "Waiting for variable to set")
def handle_set_input(message):
    logging.info(str(message.from_user.id) + " " + message.text)

    try:
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
    except Exception as e:
        logging.error("handle_set_input: "+ str(e))

    user_states[message.from_user.id] = None


@bot.message_handler(commands=["add"])
def handle_add_command(message):
    logging.info(str(message.from_user.id) + " " + message.text)

    try:
        user_states[message.from_user.id] = "Waiting for variables to add"
        bot.send_message(message.chat.id, "Write: 'name' 'streak'")
    except Exception as e:
        logging.error("handle_add_command: "+ str(e))


@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == "Waiting for variables to add")
def handle_add_input(message):
    logging.info(str(message.from_user.id) + " " + message.text)


    try:
        text = message.text
        if len(text.split()) == 2 and is_name_and_streak(text):
            user_streak = convert_reply_to_streak(message)
            add_streak("streaks.json", user_streak)
            bot.send_message(message.chat.id, "streak added")

    except Exception as e:
        logging.error("handle_add_input: " + str(e))

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
        logging.error(e)
        time.sleep(5)
        continue