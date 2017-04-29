from time import *
import json
from crawlers import *
import helpers
import database as db

"""
    Escape Game Web Crawler
    V.0.1.0
    By: R.MURA
"""

start_cursor = time()

with open("/home/egws/rooms.json",'r') as file:
    """Load the societies to scrap from json file"""
    societies = json.load(file)

with open("/home/egws/logs.txt", "a") as file:
    file.write("\n=====================\n")
    file.write(strftime("%d/%m/%Y - %H:%M:%S", localtime()) + "\n")
    file.write("=====================\n\n")
    for id, society in enumerate(societies):

        file.write("# Scrap for : " + society["name"]+ " -> Started at "+ strftime("%H:%M:%S", localtime()) + "\n\n")

        scrap_society = Bookeo(society["name"], society["url"], society["frame"])
        datas = []
        for room in society["rooms"]:
            scrap_datas = scrap_society.scrap_datas(room)
            db.create_table(helpers.parse_text(room))
            db.add_datas(helpers.parse_text(room), scrap_datas)
            datas.append(scrap_datas)

        for a in range(0, len(datas)):
            for b in range(0, len(datas[a])):
                file.write(str(datas[a][b]) + "\n")

        del room, datas
        file.write("\n# Scrap for : " + society["name"] + " -> Ended at " + strftime("%H:%M:%S", localtime()) + "\n\n")
        file.write("=====================================================\n\n")
    stop_cursor = time() - start_cursor
    file.write(strftime("%d/%m/%Y-%H:%M:%S", localtime()) + " - All Rooms scrapped in " + str(round(stop_cursor)) + " Sec.\n")
