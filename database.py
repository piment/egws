import sqlite3 as s3
db_name = "/home/egws/ESCAPE_GAMES"
def create_table(room):
    """Create Table for a room"""
    try:
        db = s3.connect(db_name)
    except:
        print("Connexion à la base " + db_name + " impossible")
    try:
        cursor = db.cursor()
        try:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS '""" + room + """'(
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                society TEXT,
                date TEXT,
                time TEXT,
                status TEXT
            )    
            """)
        except:
            print("Error: Can't create the SQL request")
        try:
            db.commit()
        except:
            print("Error: Can't commit the SQL request")
    except:
        print("Error: Table cannot be created")
    db.close()

def drop_table(room):
    """Drop room table from the database"""
    try:
        db = s3.connect(db_name)
    except:
        print('Error "drop_table()" : Can\'t connect to DB')
    try:
        cursor = db.cursor()
        cursor.execute("""DROP TABLE '""" + room + """'""")
        db.commit()
        db.close()
    except:
        print('Error "drop_table()" : Can\'t drop table')

def get_all_datas(room):
    """Get all the datas for a room"""
    db = s3.connect(db_name)
    cursor = db.cursor()
    cursor.execute("""
            SELECT * FROM '""" + room + """'
        """)
    datas = cursor.fetchall()
    db.commit()
    db.close()
    return datas

def add_datas(room, datas):
    """Add datas to room table"""
    db = s3.connect(db_name)
    cursor = db.cursor()
    for line in datas:
        info = [line[0], line[2], line[3], line[4]]
        check = check_entry(room, line[2], line[3], line[4])
        if check[0] == False:
            cursor.execute("""INSERT INTO '""" + room + """' (society, date, time, status) VALUES(?, ?, ?, ?)""", info)
        else:
            cursor.execute("""UPDATE '""" + room + """' SET status = '""" + line[4] + """' WHERE id='""" + str(check[1][0][0]) + """'""")


    db.commit()
    db.close()

def check_entry(room, date, time, status):

    db = s3.connect(db_name)
    cursor = db.cursor()
    cursor.execute("""SELECT * FROM '""" + room + """' WHERE date='""" + date + """' AND time='""" + time + """'""")
    res = cursor.fetchall()

    if len(res) > 0:
        checked = True
    else:
        checked = False
    return (checked, res)
