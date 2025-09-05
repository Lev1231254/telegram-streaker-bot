import database
from database import *

file_name = "streaks.json"

#check if reply is name and streak
def is_name_and_streak(text: str) -> bool:
    name = text.split()[0]
    streak_num = text.split()[1]


    if len(text.split()) == 2:
        try:
            float(streak_num)
            return True
        except ValueError:
            return False
    return False


#does message have form: name "str"
def is_change_name(text: str) -> bool:
    words = text.split()
    return len(words) == 2 and (words[0] == "/set_name") and len(words[1]) < 50


def is_change_description(text: str) -> bool:
    return text[0:10] == "/set_desc\n"


def convert_reply_to_streak(message : types.Message) -> Streak:
    user_id = str(message.from_user.id)
    name = message.text.split()[0]
    streak_num = message.text.split()[1]
    description = ""
    #save last description
    if get_streak_by_id("streaks.json", str(message.chat.id)).user_id != "0":
        description = get_streak_by_id("streaks.json", str(message.chat.id)).description

    result = Streak(user_id, name, streak_num, description)
    return result


def send_given_streak(bot : telebot.TeleBot, message : types.Message, user_streak : Streak) -> None:
    # update all streak numbers in db
    update_users_streak_number(file_name)

    reply = user_streak.name + " " + user_streak.streak_num

    bot.send_message(message.chat.id, reply)


def send_user_streak(bot : telebot.TeleBot, message : types.Message) -> None:
    update_users_streak_number(file_name)
    user_streak = get_streak_by_id(file_name, str(message.from_user.id))

    if user_streak.user_id == 0:
        bot.send_message(message.chat.id, "у тебя нет стрика")

    else: send_given_streak(bot, message, user_streak)


def send_streaks(bot : telebot.TeleBot, message : types.Message) -> None:
    #update all streak numbers in db
    update_users_streak_number(file_name)

    data = read_streaks(file_name)
    reply = ""

    i = 1
    for streak_dict in data:
        reply += str(i) + " | " + streak_dict["name"] + " | стрик: " + streak_dict["streak_num"] + "\n"
        i += 1

    bot.send_message(message.chat.id, reply)

def send_variable(bot : telebot.TeleBot, user_id : str,  message : types.Message, variable : str) -> None:
    update_users_streak_number(file_name)

    value = get_variable(file_name, user_id, variable)


    if value != "":
        bot.send_message(message.chat.id, value)
    else:
        bot.send_message(message.chat.id, "couldn't find variable")


def is_var_safe_to_change(variable: str, value : str) -> bool:
    if variable == "name" or variable == "description": return True

    elif variable == "streak_num":
        try:
            float(value)
            return True
        except ValueError:
            return False

    return False

