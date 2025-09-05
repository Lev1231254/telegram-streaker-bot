from datetime import datetime, timedelta
import json


date_format = "%m/%d/%Y-%H:%M:%S"

class Streak:
    def __init__(self, user_id : str, name : str, streak_num : str, description : str):
        self.user_id = user_id
        self.name = name
        self.streak_num = streak_num
        self.beginning_date = None
        self.description = description


    #use ONLY when adding new streak or when user updated streak_num
    def get_beginning_date(self) -> str:
        beginning_date = datetime.now() - timedelta(days=float(self.streak_num))
        return beginning_date.strftime(date_format)


    def get_streak(self) -> str:
        difference = datetime.now() - datetime.strptime(self.beginning_date, date_format)
        return "{:.2f}".format(difference.total_seconds() / 3600 / 24)


def dict_to_streak(streak_dict: dict) -> Streak:
    result = Streak(streak_dict['user_id'], streak_dict['name'], streak_dict['streak_num'], streak_dict['description'])
    result.beginning_date = streak_dict['beginning_date']
    return result


null_streak = Streak("0", "Noname", "0", "")