import telebot
from telebot import types
from datetime import datetime, timedelta

date_format = "%m/%d/%Y %I:%M %p"

def add_user_to_db(user: telebot.types.User, name, streak : str):
    with open("database.txt", "a", encoding='utf-8') as f:
        #get formatted into string date of streak
        current_date = datetime.now()
        streak_beginning_date = current_date - timedelta(days=int(streak))
        formatted_streak_beginning_date = streak_beginning_date.strftime(date_format)

        #actually adding user to db
        user_str = str(user.id) + " " + name + " " + str(streak) + " " + formatted_streak_beginning_date+ "\n"
        f.write(user_str)

def update_db():
    content = ""
    with open("database.txt", "r", encoding='utf-8') as f:
        line = f.readline()
        words = line.split(" ")

        #amount of days between current time and start of streak
        difference = (datetime.now - words[-1]).days
        words[2] = difference
        content += " ".join(words) + "\n"

    with open("database.txt", "w", encoding='utf-8') as f:
        f.write(content)


def show_users_from_db(bot, message: types.Message):
    with open("database.txt", "r", encoding='utf-8') as f:
        text = ""
        for line_number, line in enumerate(f, start=1):
            text += line
            print(line_number, line)
        if (text == ""):
            bot.send_message(message.chat.id, "лол, че ты хочешь, никого ж нет. Зарегайся сначала")
        else:
            bot.send_message(message.chat.id, text)


def is_name_and_streak(text: str) -> bool:
    words = text.split()

    if len(words) == 2 and words[1].isdigit:
        return True
    return False

