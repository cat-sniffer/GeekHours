""" Database.py is a moule to comunicate with a database. """

import sqlite3
from sys import exit

__all__ = ['Database']

class Database:
    """ Database class initializes and manipulates SQLite3 database. """
    def __init__(self):
        self.con = None
        self.cur = None
        self.donelist = 'donelist'
        self.course = 'course'

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

    def show(self, table):
        """  Show table """
        if self.donelist:
            self.cur.execute('SELECT * FROM donelist').fetchall()
        elif self.course:
            self.cur.execute('SELECT * FROM course').fetchall()
        else:
            print("No such table '{}'.".format(table))
            exit()

    def insert(self, table, val):
        """
        Insert a new record into a table.
        If course name which is not in this table is used for insertion into donelist,
        the record will be discurded.
        """
        ##### course
        if table is self.course:
            course = self.cur.execute('SELECT * FROM course')
            course_names = course.fetchall()
            if course_names:
                """
                Check if the same records already exist.
                Validate 'val' and avoid duplication.
                """
                for elem in val:
                    ret = any(elem in course for course in course_names)
                    if ret:
                        print("'{}' already exists. This was not inserted.".format(elem))
                    else:
                        self.cur.execute('INSERT INTO course(name) VALUES (?)', (elem,))
                        self.con.commit()
                        print("Add new course '{}' in course.".format(val))
            else:
                """
                If no records in table,
                add 'val' without validation.
                """
                for elem in val:
                    self.cur.execute('INSERT INTO course(name) VALUES (?)', (elem,))
                self.con.commit()
                print("Add new course '{}' in course.".format(val))

        ##### donelsit
        elif table is self.donelist:
            """
            Validate the input course name
            exists in the table 'course'.
            """
            course = self.cur.execute('SELECT * FROM course')
            course_names = course.fetchall()
            ret = any(val[1] in course for course in course_names)
            if ret:
                self.cur.execute('INSERT INTO donelist(date, course, duration) VALUES (?, ?, ?)',
                                 val)
                self.con.commit()
                print("Add new record '{}' in donelist.".format(val))
            else:
                print("Invalid course name '{}'.".format(val[1]))

        else:
            print("No such table '{}'.".format(table))
            print('Failed to insert a record.')
            exit()
