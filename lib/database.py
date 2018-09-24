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

    def insert(self, table, val):
        """
        Insert a new record into a table.
        In the following cases, insertion will be discurded.

        course:
        * When course name which is already registered is used for insertion

        donelist:
        * When course name which is not in the table 'course' is used for insertsion
        """
        ##### course
        if table is self.course:
            course = self.cur.execute('SELECT * FROM course')
            course_names = course.fetchall()
            if course_names:
                for elem in val:
                    ret = any(elem in course for course in course_names)
                    if ret:
                        print("'{}' already exists. This was not inserted.".format(elem))
                    else:
                        self.cur.execute('INSERT INTO course(name) VALUES (?)', (elem,))
                        self.con.commit()
                        print("Add new course '{}' in course.".format(val))
            else:
                for elem in val:
                    self.cur.execute('INSERT INTO course(name) VALUES (?)', (elem,))
                self.con.commit()
                print("Add new course '{}' in course.".format(val))

        ##### donelsit
        elif table is self.donelist:
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
            sys.exit()

    def update(self, table, course_name, val, date=None):
        """
        Update a record with replacing.

        donelist: Search by date and course name.
        If found a matched record, the record will be replaced with new fields.

        course: Search by course name.
        If found a matched record, the record will be replaced with a new course name.
        """
        ##### donelist
        if table is self.donelist:
            donelist = self.cur.execute('SELECT * FROM donelist WHERE course=? AND date=?',
                                        (course_name, date,))
            ret = donelist.fetchall()
            if ret:
                self.cur.execute('UPDATE donelist SET date=?, course=?, duration=? WHERE course=?\
                                 AND date=?', (val[0], val[1], val[2], course_name, date,))
                self.con.commit()
            else:
                print("NO such fields '{}' '{}' in '{}'.".format(date, course_name, table))

        ##### course
        elif table is self.course:
            course = self.cur.execute('SELECT * FROM course WHERE name=?', (course_name,))
            ret = course.fetchall()
            if ret:
                self.cur.execute('UPDATE course SET name=? WHERE name=?', (val, course_name,))
                self.con.commit()
            else:
                print("NO such course name '{}' in '{}.'".format(course_name, table))

        else:
            print("No such table '{}'.".format(table))
            print('Failed to update record.')
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
