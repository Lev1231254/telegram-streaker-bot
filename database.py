import telebot
from telebot import types
from datetime import datetime, timedelta
import json
import streak
from streak import *
from decimal import *

def read_streaks(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []  # If the file doesn't exist, start with an empty list
    return data


#convert "name streak" reply to a Streak class



def is_streak_in_json(file_name, target_streak: Streak):
    data = read_streaks(file_name)
    for streak_dict in data:
        if streak_dict['user_id'] == target_streak.user_id:
            return True

    return False


def dump_streak(file_name, streak_to_dump : Streak):
    data = read_streaks(file_name)

    data.append(streak_to_dump.__dict__)
    data = sorted(data, key=lambda streak_dict: streak_dict["beginning_date"])

    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


#if streak found, updates streak in db. If not found doesn't do anything
def update_user_streak(file_name, streak_to_update : Streak):
    data = read_streaks(file_name)

    for streak_dict in data:
        if streak_dict['user_id'] == streak_to_update.user_id:
            streak_dict['name'] = streak_to_update.name
            streak_dict['streak_num'] = streak_to_update.streak_num
            streak_dict['beginning_date'] = streak_to_update.beginning_date

    data = sorted(data, key=lambda streak: streak["beginning_date"])

    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def add_streak(file_name, streak_to_add : Streak):
    streak_to_add.beginning_date = streak_to_add.get_beginning_date()

    if is_streak_in_json(file_name, streak_to_add):
        update_user_streak(file_name, streak_to_add)
    else:
        dump_streak(file_name, streak_to_add)


def update_users_streak_number(file_name):
    data = read_streaks(file_name)
    for streak_dict in data:
        streak_class = dict_to_streak(streak_dict)
        streak_dict['streak_num'] = streak_class.get_streak()

    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def get_streak_by_id(file_name, user_id: str) -> Streak:
    data = read_streaks(file_name)

    for streak_dict in data:
        if streak_dict['user_id'] == user_id:
            return dict_to_streak(streak_dict)

    return null_streak


def update_name(file_name, streak_to_update : Streak, name : str) -> None:
    data = read_streaks(file_name)

    for streak_dict in data:
        if streak_dict["user_id"] == streak_to_update.user_id:
            streak_dict["name"] = name

    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def sort_streaks(file_name):
    data = read_streaks(file_name)
    result = sorted(data, key=lambda streak: streak['beginning_date'])

    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(result, file, ensure_ascii=False, indent=4)


def update_description(file_name, user_id : str, text : str) -> None:
    data = read_streaks(file_name)

    for streak_dict in data:
        if streak_dict['user_id'] == user_id:
            streak_dict['description'] = text

    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def decipher_shortenings(variable : str) -> str:
    if variable == "streak": return "streak_num"
    elif variable == "desc": return "description"
    return variable


def get_variable(file_name, user_id : str, variable : str) -> str:
    data = read_streaks(file_name)

    #count for shortenings
    variable = decipher_shortenings(variable)

    for streak_dict in data:
        if streak_dict['user_id'] == user_id:
            try:
                return streak_dict[variable]
            except KeyError:
                return ""
    return ""


def set_variable(file_name, user_id : str, variable : str, value : str) -> None:
    data = read_streaks(file_name)

    #count for shortenings
    variable = decipher_shortenings(variable)

    #change variable if possible
    for streak_dict in data:
        if streak_dict['user_id'] == user_id:
            streak_dict[variable] = value
            if variable == "streak_num":
                streak = dict_to_streak(streak_dict)
                streak_dict["beginning_date"] = streak.get_beginning_date()

    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def find_id_by_name(file_name, name : str) -> str:
    data = read_streaks(file_name)

    for streak_dict in data:
        if streak_dict['name'] == name:
            return streak_dict['user_id']
    return null_streak.user_id
