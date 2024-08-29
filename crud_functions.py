import sqlite3


def initiate_db():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    )
    ''')

    title = ['Клей для пенополистирола ZM-01', 'Клей для плитки ZM-51', 'Клей для блоков ZM-22', 'Штукатурка гладкая цементно-известковая ZM-41']
    description = ['Предназначен для приклеивания теплоизоляционных плит из пенополистирола', 'Предназначен для приклеивания керамической плитки', 'Предназначена для возведения стен из блоков из ячеистого бетона', 'Предназначена для машинного и ручного оштукатуривания']
    price = ['417 ₽/шт', '353 ₽/шт', '384 ₽/шт', '395 ₽/шт']

    cursor.execute('INSERT INTO Products(title, description, price) VALUES (?, ?, ?)',
                   (f'{title[0]}', f'{description[0]}', f'{price[0]}'))
    cursor.execute('INSERT INTO Products(title, description, price) VALUES (?, ?, ?)',
                   (f'{title[1]}', f'{description[1]}', f'{price[1]}'))
    cursor.execute('INSERT INTO Products(title, description, price) VALUES (?, ?, ?)',
                   (f'{title[2]}', f'{description[2]}', f'{price[2]}'))
    cursor.execute('INSERT INTO Products(title, description, price) VALUES (?, ?, ?)',
                   (f'{title[3]}', f'{description[3]}', f'{price[3]}'))

    connection = sqlite3.connect('initiate.db')
    cursor = connection.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users(
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER NOT NULL,
            balance INTEGER NOT NULL
            )
            ''')

    connection.commit()
    connection.close()


initiate_db()


def get_all_products():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT title, description, price FROM Products")
    db = cursor.fetchall()
    return list(db)


def add_user(username, email, age):
    connection = sqlite3.connect('initiate.db')
    cursor = connection.cursor()
    new_user = cursor.execute("SELECT COUNT(*) FROM Users").fetchone()[0] + 1
    cursor.execute(f'''INSERT INTO Users VALUES('{new_user}', '{username}', '{email}', '{age}', '1000')''')
    connection.commit()


def is_included(username):
    connection = sqlite3.connect('initiate.db')
    cursor = connection.cursor()
    check_user = cursor.execute('SELECT * FROM Users WHERE username = ?', (username,)).fetchone()
    if check_user is None:
        return False
    connection.commit()
    return True