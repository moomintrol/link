import sqlite3

connect = sqlite3.connect('database.db', check_same_thread=False)
cursor = connect.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS "users"
("id" INTEGER NOT NULL,
"login" TEXT NOT NULL,
"password" TEXT NOT NULL,
primary key ("id" AUTOINCREMENT)
);''')
connect.commit()

cursor.execute('''CREATE TABLE IF NOT EXISTS "links"
("id" INTEGER NOT NULL,
"long" TEXT NOT NULL,
"short" TEXT NOT NULL,
"count" INT NOT NULL,
"access_id" INTEGER NOT NULL,
"owner_id" INTEGER NOT NULL,
primary key ("id" AUTOINCREMENT)
);''')
connect.commit()

cursor.execute('''CREATE TABLE IF NOT EXISTS "accesses"
("id" INTEGER NOT NULL,
"level_eng" TEXT NOT NULL,
"level_ru" TEXT NOT NULL,
primary key ("id" AUTOINCREMENT)
);''')
connect.commit()

#регистрация
def registration(login,password):
    cursor.execute('''INSERT INTO
        users (login,password)
        VALUES (?,?) 
        ''', (login,password,))
    connect.commit()

def searchUser(login):
    return cursor.execute('''SELECT password 
        FROM users
        WHERE login = ? 
        ''', (login,)).fetchone()

def searchUserId(login):
    return cursor.execute('''SELECT id 
        FROM users
        WHERE login = ? 
        ''', (login,)).fetchone()

def auth(login,password):
    cursor.execute('''SELECT * 
        FROM users
        WHERE login = ? 
        AND password = ?
        ''', (login, password,)).fetchone()
    return "Вы вошли"

def addLink(long,short,access_id,owner_id,count = 0):
    cursor.execute('''INSERT INTO
        links (long,short,count,access_id,owner_id)
        VALUES (?,?,?,?,?)
        ''', (long,short,count,access_id,owner_id))
    connect.commit()

def seacrAccesses():
    return cursor.execute('''SELECT * FROM accesses
    ''',()).fetchall()

def addAccesses(level_eng,level_ru):
    cursor.execute('''INSERT INTO
        accesses (level_eng,level_ru)
        VALUES (?,?)
        ''', (level_eng,level_ru))
    connect.commit()
    return "Добавление категории прошло успешно"

def searchUserLinks(user_id):
    return cursor.execute('''SELECT links.long, links.short, links.count, accesses.level_ru
    FROM links
    INNER JOIN accesses ON accesses.id = links.access_id
    WHERE links.owner_id = ?
    ''', (user_id,)).fetchall()

def seacrhPseudonym(pseudonym):
    return cursor.execute('''SELECT short 
    FROM links
    WHERE short = ?''',(pseudonym,)).fetchall()

def seacrhLongUser(long_link, user_id):
    return cursor.execute('''SELECT long 
    FROM links
    WHERE long = ? AND owner_id = ?''',(long_link,user_id)).fetchall()

def seacrhInfoLink(user_id, long_link):
    return cursor.execute('''SELECT long, short, access_id
    FROM links 
    WHERE owner_id = ? AND long = ?''',(user_id,long_link)).fetchall()

def updateLink(long,short,access_id,user_id):
    cursor.execute('''UPDATE links
    SET short = ?, access_id = ?
    WHERE owner_id = ? AND long = ?''',(short,access_id,user_id,long))
    connect.commit()

def deleteLink(long_link, user_id):
    cursor.execute('''DELETE
    FROM links
    WHERE long = ? AND owner_id = ?''',(long_link,user_id))
    connect.commit()
    return "Удалил"

def searchLinkInfo(short):
    return cursor.execute('''SELECT long, count, access_id, owner_id
    FROM links
    WHERE short = ?''',(short,)).fetchall()

def updateCount(long,count):
    cursor.execute('''UPDATE links
    SET count = ?
    WHERE long = ?''',(count,long))
    connect.commit()

def accessesInfo():
    return cursor.execute('''SELECT level_ru
    FROM accesses''').fetchall()