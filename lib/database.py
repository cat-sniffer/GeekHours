""" Database.py is a moule to comunicate with a database. """

import sqlite3

__all__ = ['Database']

class Database:
    """ Database class initializes and manipulates SQLite3 database. """
    def __init__(self):
        self.con = None
        self.cur = None

    def connect_db(self, db_name):
        """ Connect to the database """
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()

    def close_db(self):
        """ Close the database """
        if self.con:
            self.con.close()

    def create_table(self):
        """
        Create table.

        donelist: Table for registration of date, course name and duration you studied.
        course: Table for validation of course name.
        """
        donelist = ("CREATE TABLE donelist ("
                    "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                    "date TEXT NOT NULL, "
                    "course TEXT NOT NULL, "
                    "duration TEXT NOT NULL)")

        course = ("CREATE TABLE course ("
                  "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                  "name TEXT NOT NULL)")

        self.cur.execute(donelist)
        self.cur.execute(course)
        self.con.commit()
