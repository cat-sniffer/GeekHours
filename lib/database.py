""" Database.py is a moule to comunicate with a database. """

import sqlite3
from typing import List

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
                  "name TEXT NOT NULL UNIQUE)")

        self.cur.execute(donelist)
        self.cur.execute(course)
        self.con.commit()

    def show(self, table):
        """  Show table """
        if table is self.course:
            ret = self.cur.execute('SELECT * FROM course').fetchall()
            print(ret)
        elif table is self.donelist:
            ret = self.cur.execute('SELECT * FROM donelist').fetchall()
            print(ret)
        else:
            raise RuntimeError("No such table.")
        return ret

    def insert_course(self, courses: List[str]):
        """ Insert course name.

        Insert course name into the 'course' table.
        Insertion of the course name which is already registered will be discarded.
        """
        for elem in courses:
            with self.con:
                self.con.execute('INSERT INTO course(name) VALUES (?)', (elem,))
                print("Add '{}' in course.".format(elem))
        return None

    def insert_donelist(self, date: str, course: str, duration: str):
        """ Insert donelist.

        Insert donelist into the 'donelist' table.
        The course name must be a registered name in the 'course' table.
        """
        ret = self.con.execute('SELECT name FROM course WHERE name=?', (course,))
        check = ret.fetchall()

        if not check:
            print("No such course in 'course' table.")
            return False

        with self.con:
            self.con.execute('INSERT INTO donelist(date, course, duration) VALUES (?, ?, ?)',
                             (date, course, duration,))
            print("Add '{} {} {}' in donelist.".format(date, course, duration))
        return None

    def update_course(self, old_course: str, new_course: str):
        """ Update course name of 'course' table.

        Replace old_course by new_course.
        """
        ret = self.con.execute('SELECT name FROM course WHERE name=?', (old_course,))
        check = ret.fetchall()

        if not check:
            raise RuntimeError("No such course in 'course' table.")

        with self.con:
            self.cur.execute('UPDATE course SET name=? WHERE name=?', (new_course, old_course,))
            print("Updated '{}' by '{}'".format(old_course, new_course))

        return None

    def update_donelist(self, old_date, old_course: str, new_date: str, new_course: str, new_duration: str):
        """ Update record of 'donelist' table.

        Search record by date and course name, and if found matched record replace the record by
        new record.
        """
        ret = self.con.execute('SELECT date, course FROM donelist WHERE date=? AND course=?',
                               (old_date, old_course,))
        check = ret.fetchall()

        if not check:
            raise RuntimeError("No such record in 'donelist' table.")

        with self.con:
            self.cur.execute('UPDATE donelist SET date=?, course=?, duration=?\
                             WHERE date=? AND course=?',
                             (new_date, new_course, new_duration, old_date, old_course,))
            print('Updated record.')

        return None

    def remove_course(self, course: str):
        """ Remove course name from 'course' table. """
        ret = self.con.execute('SELECT name FROM course WHERE name=?', (course,))
        check = ret.fetchall()

        if not check:
            raise RuntimeError("No such course in 'course' table.")

        with self.con:
            self.cur.execute('DELETE FROM course WHERE name=?', (course,))
            print("Removed '{}' from course.".format(course))

        return None

    def remove_donelist(self, date: str, course: str):
        """ Remove record from 'donelist' table.

        Search record by date and course name and if found matched record, it will be removed.
        """
        ret = self.con.execute('SELECT date, course FROM donelist WHERE date=? AND course=?',
                               (date, course,))
        check = ret.fetchall()

        if not check:
            raise RuntimeError("No such record in 'donelist' table.")

        with self.con:
            self.cur.execute('DELETE FROM donelist WHERE date=? AND course=?',
                             (date, course,))
            print('Removed record.')

        return None
