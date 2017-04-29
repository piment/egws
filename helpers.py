from time import *
from datetime import *

def get_date_fr(offset=False):
    days = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
    months = ["janvier", "fevrier", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre",
              "novembre", "décembre"]

    month_num = localtime()[1] - 1

    if not offset:
        day_num = localtime()[2]
        day_week_num = localtime()[6]

    else:
        if (localtime()[6] + offset) > 6:
            day_week_num = localtime()[6] + offset - 7
            if (localtime()[2] + offset) > 30:
                if (month_num % 2) == 0:
                    day_num = localtime()[2] + offset - 31
                    month_num = month_num + 1
                else:
                    day_num = localtime()[2] + offset - 30
                    month_num = month_num + 1
            else:
                day_num = localtime()[2] + offset
        else:
            day_week_num = localtime()[6] + offset
            if (localtime()[2] + offset) > 30:
                if (month_num % 2) == 0:
                    day_num = localtime()[2] + offset - 31
                    month_num = month_num + 1
                else:
                    day_num = localtime()[2] + offset - 30
                    month_num = month_num + 1
            else:
                day_num = localtime()[2] + offset
    date_fr = str(days[day_week_num] + " " + str(day_num) + " " +  months[month_num])

    return date_fr



def parse_scrap_date(date):

    if date.lower() == "aujourd'hui" or date.lower() == "aujourd’hui":
        date = get_date_fr()
    elif date.lower() == "demain":
        try:
            date = get_date_fr(1)
        except:
            date = "ERR03"
    else:
        date = date.replace(",", "")

    return date

def parse_text(text):
    text = text.replace("à", "a").lower()
    text = text.replace("'", "").lower()
    return text.replace(" ", "_").lower()