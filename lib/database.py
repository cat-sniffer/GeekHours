""" Database.py is a moule to comunicate with a database. """

import sqlite3
import sys

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
            sys.exit()

    def remove(self, table, course_name, date=None):
        """
        Remove a record from a table.

        donelist: Search by date and course name.
        If found a matched record, the record will be deleted.

        course: Search by course name.
        If found a matched record, the record will be deleted.
        """
        ##### donelist
        if table is self.donelist:
            donelist = self.cur.execute('SELECT * FROM donelist WHERE course=? AND date=?',
                                        (course_name, date,))
            ret = donelist.fetchall()
            if ret:
                self.cur.execute('DELETE FROM donelist WHERE course=? AND date=?',
                                 (course_name, date,))
                self.con.commit()
            else:
                print("NO such fields '{}' '{}' in '{}'.".format(date, course_name, table))

        ##### course
        elif table is self.course:
            course = self.cur.execute('SELECT * FROM course WHERE name=?', (course_name,))
            ret = course.fetchall()
            if ret:
                self.cur.execute('DELETE FROM course WHERE name=?', (course_name,))
                self.con.commit()
            else:
                print("NO such course name '{}' in '{}'.".format(course_name, table))

        else:
            print("No such table '{}'.".format(table))
            print('Failed to remove record.')
            sys.exit()
