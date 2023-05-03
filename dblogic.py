#this file contains all necessary functions to work with db
#Be aware that all methods are named in camelcase
#if you run this script, it will create a database and a table girls inside

import sqlite3
import Girlclass

name = "girls.db" #name of the database

#this code makes a connection to database to see if it runs ok. Returns a tuple with all user data
with sqlite3.connect(name) as con:
    cursor = con.cursor()
    cursor.execute('SELECT * FROM girls')
    data = cursor.fetchall()
    print(data)
    print("Database is ready to go")

#creates a record after registration.
def makenewgirl(userid, takepill, mustpill, numinc):
    with sqlite3.connect(name) as con:
        cursor = con.cursor()
        cursor.execute(f"INSERT INTO girls VALUES (?, ?, ?, ?)", (userid, takepill, mustpill, numinc))
        con.commit()
        print("New girl is added to database")

#fetches all users and creates a list of tuples
def fetchallusers():
    with sqlite3.connect(name) as con:
        cursor = con.cursor()
        cursor.execute('SELECT * FROM girls')
        userlist = cursor.fetchall()
        return userlist

#takes a string with userid and returns a tuple if finds one
def getuser(userid):
    with sqlite3.connect(name) as con:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM girls WHERE userid = ?", (userid, ))
        user = cursor.fetchall()
        return user


#takes in a string with userid and deletes a user if finds one
def deleteuser(userid):
    with sqlite3.connect(name) as con:
        cursor = con.cursor()
        cursor.execute("DELETE FROM girls WHERE userid = ?", (userid,))
        con.commit()
        print(f"user {userid} is deleated")
        return True

#updates data in the database. Takes a girl object as an argument
def updateuser(object: Girlclass.Girl):
    userid = object.get_userid()
    takepill = object.get_takepill()
    mustpill = object.get_mustpill()
    numinc = object.get_numinc()
    with sqlite3.connect(name) as con:
        cursor = con.cursor()
        cursor.execute('UPDATE girls SET takepill = ?, mustpill = ?, numinc = ? WHERE userid = ?', (takepill, mustpill, numinc, userid))
        con.commit()
        print("Update complete fo -r" + object.get_userid())
#Creates a database and a table
if __name__ == '__main__':
    with sqlite3.connect(name) as con:
        cursor = con.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS girls (
        userid TEXT,
        takepill BOOLEAN,
        mustpill BOOLEAN
        numinc INTEGER)''')
        con.commit()

