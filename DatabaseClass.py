import sqlite3


class PlayerScore:
    def __init__(self):
        self.myDatabase = sqlite3.connect('database.db')

        cursor = self.myDatabase.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS scores ( 
                    timeID      integer,
                    time        real,
                    nameID      integer,
                    PRIMARY KEY ("timeID" AUTOINCREMENT),
                    FOREIGN KEY ("nameID") REFERENCES players ("nameID")
                    )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS players (
                    nameID      integer,
                    name        text,
                    PRIMARY KEY ("nameID" AUTOINCREMENT)
                    )''')

    def menu(self):

        while True:
            print('welcome to the database')
            menu = ('''
            1 - Create New User
            2 - Login
            3 - Display the database
            4 - Exit
            - ''')

            userChoice = input(menu)

            if userChoice == '1':
                self.newUser()

            elif userChoice == '2':

                while True:
                    enter = self.login()
                    if enter == 'login':

                        enter = self.userMenu()
                        if enter == 'exit':
                            break

                    elif enter == 'exit':
                        break

            elif userChoice == '4':
                print('Goodbye')
                break

            else:
                print('input not recognized')

    def newUser(self):
        print('Add a new user')
        while True:
            username = input("Enter a username: ")
            cursor = self.myDatabase.cursor()
            cursor.execute('SELECT * FROM user WHERE username = ?', [username])

            if cursor.fetchall():
                print('Username Taken')
            else:
                break

        forename = input('Please enter your first name: ')
        surname = input('Please enter your last name: ')
        password = input('Please enter a password: ')
        password2 = input('Please re-enter your password: ')
        while password != password2:
            print('Passwords did not match')
            password = input('Please enter a password: ')
            password2 = input('Please re-enter your password: ')
        self.username = username
        self.password = password
        self.forename = forename
        self.surname = surname
        self.score = 30275

        cursor.execute('''INSERT INTO user(username, forename, surname, password)
                          VALUES(?, ?, ?, ?)''', [username, forename, surname, password])
        self.myDatabase.commit()

    def login(self):
        while True:
            cursor = self.myDatabase.cursor()
            username = input('Enter your username: ')
            password = input('Enter your password: ')
            cursor.execute('SELECT * FROM user WHERE username = ? AND password = ?', [username, password])
            results = cursor.fetchall()

            if results:
                for i in results:
                    print('Welcome ' + i[2])
                    return 'login'

            else:
                print("username or password not recognized")

                again = input("Do you want to try again (Y/N)").lower()
                while again != "n" and again != "y":
                    print("You did not enter a Y or N as your Input")
                    again = input("Do you want to try again (Y/N)").lower()

                if again == 'y':
                    pass

                else:
                    return "exit"

    def userMenu(self):

        while True:

            menu = ('''
            1 - Profile
            2 - log out
            - ''')

            userChoice = input(menu)

            if userChoice == '1':
                return 'exit'

            if userChoice == '2':
                return 'exit'

    def insertScores(self, score, name):
        cursor = self.myDatabase.cursor()
        cursor.execute('INSERT INTO players (name) VALUES (?)', [name])
        cursor.execute('SELECT nameID FROM players WHERE name = (?)', [name])
        cursor.execute('INSERT INTO scores (time, nameID) VALUES (?, ?)', [score, cursor.fetchone()])
        self.myDatabase.commit()
        cursor.execute('SELECT * FROM scores')
        for item in cursor.fetchall():
            print(item)

    def allScores(self):
        cursor = self.myDatabase.cursor()
        cursor.execute('SELECT * FROM players')
        print(cursor.fetchall())
        cursor.execute('SELECT * FROM scores')
        print(cursor.fetchall())

    def sortScores(self):
        cursor = self.myDatabase.cursor()
        cursor.execute('SELECT * FROM scores ORDER BY time')
        print(cursor.fetchall())

    def changeUser(self, name, newname):
        cursor = self.myDatabase.cursor()
        cursor.execute('UPDATE SET name = (?) WHERE name = (?)', (newname, name))
        self.myDatabase.commit()


# db = PlayerScore()
# db.insertScores(input("score: "), input("username: "))
