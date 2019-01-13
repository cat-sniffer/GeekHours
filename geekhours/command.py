""" command.py is the module to manipulates the database from the command-line. """

__all__ = ['Command']

from typing import List
from geekhours.database import Database


class Command:
    """ Command class provides command-line interface to manipulate the database. """

    def __init__(self, db_name: str):
        self.database = Database(db_name)
        self.database.create_table()

    def show(self, arg: str):
        """ Call database.show() """
        records = self.database.show(arg)
        print(records)

    def insert_course(self, arg: List[str]):
        """ Call database.insert_course() """
        self.database.insert_course(arg)

    def insert_donelist(self, date: str, course: str, duration: str):
        """ Call database.insert_donelist() """
        self.database.insert_donelist(date, course, duration)

    def remove_course(self, arg: str):
        """ Call database.remove_course() """
        self.database.remove_course(arg)

    def remove_donelist(self, date: str, course: str):
        """ Call database.remove_donelist() """
        self.database.remove_donelist(date, course)
