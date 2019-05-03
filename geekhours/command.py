""" command.py is the module to manipulates the database from the command-line. """

__all__ = ['Command']

import csv
import json
from pathlib import Path
from typing import Dict, List, Sequence, Tuple
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

    def show_total_hours(self):
        """ Call database.get_total_hours() """
        key = ['total_hours']
        records = self.database.get_total_hours()
        formatted = self.map_keys_to_dict(key, records)
        formatted.update(self.show_total_hours_course())
        formatted.update(self.show_total_hours_week())
        formatted.update(self.show_total_hours_month())
        return formatted

    def show_total_hours_course(self):
        """ Call database.get_total_hours_course() """
        key = ['total_hours_per_course']
        records = self.database.get_total_hours_course()
        formatted = self.map_keys_to_dict(key, records)
        return formatted

    def show_total_hours_week(self, course: str = None):
        """ Call database.get_total_hours_week() """
        key = ['total_hours_per_week']
        records = self.database.get_total_hours_week(course)
        records = self.name_months_and_days(records)
        formatted = self.map_keys_to_dict(key, records)
        return formatted

    def show_total_hours_month(self, course: str = None):
        """ Call database.get_total_hours_month() """
        key = ['total_hours_per_month']
        records = self.database.get_total_hours_month(course)
        records = self.name_months_and_days(records)
        formatted = self.map_keys_to_dict(key, records)
        return formatted

    def map_keys_to_dict(self, keys: List, seq: List) -> Dict:
        """
        Make a dictionary key and value pairs of the 0th element and 1st
        elementthe of seq. Then map key to the dictionary made,
        and return it as a new dictionary.

        {key: {elem_0: elem_1}}

        Args:
            keys: A list of arbitrary keys.
            seq: Sequence composed two of elements.
        """
        res = self.make_dict_from_sequence(seq)
        return self.map_keys_to_seq(keys, res)

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

    @staticmethod
    def name_months_and_days(records: List) -> List:
        """ Name the months and the days of week

        Take a list containing the day numbers or month numbers in the
        0th element of tuple. Then replace it with the corresponding name
        and return it as a new list.

        e.g.
        [('0', ELEM), ('1', ELEM), ...] -> [('Sun', ELEM), ('Mon', ELEM), ...]
        [('01', ELEM), ('02', ELEM), ...] -> [('Jan', ELEM), ('Feb', ELEM), ...]

        Day number | Day
        ---------- | ----
        0          | Sun
        1          | Mon
        ...        | ...
        6          | Sat

        Month number | Month
        ------------ | -----
        01           | Jan
        02           | Feb
        ...          | ...
        12           | Dec

        """
        months_and_days = {
            '01': 'Jan',
            '02': 'Feb',
            '03': 'Mar',
            '04': 'Apr',
            '05': 'May',
            '06': 'Jun',
            '07': 'Jul',
            '08': 'Aug',
            '09': 'Sep',
            '10': 'Oct',
            '11': 'Nov',
            '12': 'Dec',
            '0': 'Sun',
            '1': 'Mon',
            '2': 'Tue',
            '3': 'Wed',
            '4': 'Thu',
            '5': 'Fri',
            '6': 'Sat',
        }

        named = []

        for record in records:
            if record[0] in months_and_days:
                entry = (months_and_days[record[0]], record[1])
                named.append(entry)

        return named

    @staticmethod
    def map_keys_to_seq(keys: List, *seq: Sequence) -> Dict:
        """
        Take a list of keys and register them as key of a dictionary,
        and register the elements of sequence as value.

        Args:
            keys: A list of arbitrary keys.
            seq : Sequence to register as value of the dictionary.
        """
        count = 0
        res = dict.fromkeys(keys)

        for key in keys:
            res[key] = seq[count]
            count += 1

        return res

    @staticmethod
    def make_dict_from_sequence(seq: Sequence) -> Dict:
        """
        Take a sequence and register the 0th element of it as a key,
        and the 1st element as a value of a dictionary.

        Args:
            seq: Sequence composed two of elements.
        """
        res = {}
        for elem in seq:
            res.fromkeys([elem[0]])
            res[elem[0]] = elem[1]

        return res
