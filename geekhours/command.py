""" command.py is the module to manipulates the database from the command-line. """

__all__ = ['Command']

import csv
import json
from pathlib import Path
from typing import List, Tuple
from geekhours.database import Database


class Command:
    """ Command class provides command-line interface to manipulate the database. """

    def __init__(self, db_name: str):
        self.database = Database(db_name)
        self.database.create_table()

    def show_column(self, arg: str):
        """ Call database.get_column() """
        column = self.database.get_column(arg)
        return column

    def show(self, arg: str):
        """ Call database.show() """
        records = self.database.show(arg)
        return records

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

    @staticmethod
    def dump_to_csv(records: str, csvfile: str, fields: Tuple):
        """ dump outputs to comma separated CSV.

        args:
            records: Target data to dump.
            csvfile: File path to save.
            fields: Tuple object of a header row of the records.
        """
        csvfile = Path(csvfile)

        if csvfile.exists():
            raise FileExistsError('{} exists'.format(csvfile))
        with open(str(csvfile), 'w', newline='') as outcsv:
            writer = csv.DictWriter(outcsv, fieldnames=fields)
            writer.writeheader()
            csv_writer = csv.writer(outcsv, delimiter=',')
            for record in records:
                csv_writer.writerow(record)

    @staticmethod
    def dump_to_json(records: str, jsonfile: str):
        """ dump outputs to JSON and write it to a file.

        args:
            records: Target data to write.
            jsonfile: File path to save.
        """
        jsonfile = Path(jsonfile)

        if jsonfile.exists():
            raise FileExistsError('{} exists'.format(jsonfile))
        with open(str(jsonfile), 'w') as outjson:
            json.dump(records, outjson)
