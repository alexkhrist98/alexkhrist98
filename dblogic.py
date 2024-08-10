#this file contains database functions. Note that you should declare username and password inside .env file

import psycopg2
import dotenv
import Girlclass
import os

dotenv.load()
dbhost = os.getenv("DBHOST")
dbuser = os.getenv("DBUSER")
dbpass = os.getenv('DBPASS')
name = os.getenv("DBNAME")
#this code makes a connection to database to see if it runs ok. Returns a tuple with all user data

#creates a record after registration.
def makenewgirl(userid, takepill, mustpill, numinc):
    with psycopg2.connect(database=name, user=dbuser, password=dbpass, host=dbhost) as con:
        cursor = con.cursor()
        cursor.execute(f"INSERT INTO girls (userid, takepill, mustpill, numinc) VALUES (%s, %s, %s, %s)", (userid, takepill, mustpill, numinc))
        con.commit()
        print("New girl is added to database")

#fetches all users and creates a list of tuples
def fetchallusers():
    with psycopg2.connect(database=name, user=dbuser, password=dbpass, host=dbhost) as con:
        cursor = con.cursor()
        cursor.execute('SELECT * FROM girls')
        userlist = cursor.fetchall()
        return userlist or None

#takes a string with userid and returns a tuple if finds one
def getuser(userid):
    with psycopg2.connect(database=name, user=dbuser, password=dbpass, host=dbhost) as con:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM girls WHERE userid = %s", (userid, ))
        user = cursor.fetchall()
        return user or None


#takes in a string with userid and deletes a user if finds one
def deleteuser(userid):
    with psycopg2.connect(database=name, user=dbuser, password=dbpass, host=dbhost) as con:
        cursor = con.cursor()
        cursor.execute("DELETE FROM girls WHERE userid = %s", (userid,))
        con.commit()
        print(f"user {userid} is deleated")
        return True

#updates data in the database. Takes a girl object as an argument
def updateuser(object: Girlclass.Girl):
    userid = object.get_userid()
    takepill = object.get_takepill()
    mustpill = object.get_mustpill()
    numinc = object.get_numinc()
    with psycopg2.connect(database=name, user=dbuser, password=dbpass, host=dbhost) as con:
        cursor = con.cursor()
        cursor.execute('UPDATE girls SET takepill = %s, mustpill = %s, numinc = %s WHERE userid = %s', (takepill, mustpill, numinc, userid))
        con.commit()
#Creates a database and a table
if __name__ != '__main__':
    with psycopg2.connect(database=name, user=dbuser, password=dbpass, host=dbhost) as con:
        cursor = con.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS girls (
        userid INTEGER PRIMARY KEY,
        takepill BOOLEAN,
        mustpill BOOLEAN,
        numinc INTEGER)''')

        con.commit()