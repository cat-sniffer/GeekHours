""" Unit test for Command module. """

import sqlite3
import unittest
from geekhours.command import Command
from geekhours.util import create_db, remove_db


class TestCommand(unittest.TestCase):
    """ Test cases of the unit test for Command class """

    @classmethod
    def setUpClass(cls):
        """ Prepare the test fixtures

        Create temporary database and test directory first.
        """
        cls._db_path, cls._db_name = create_db()
        cls._command = Command(cls._db_name)
        cls._course_name_python = 'python'
        cls._course_name_math = 'math'
        cls._course_name_eng = 'english'
        cls._courses = [cls._course_name_python, cls._course_name_math, cls._course_name_eng]
        cls._date = '2018-11-01'
        cls._duration = '5'
        cls._donelist = [cls._date, cls._course_name_python, cls._duration]

    @classmethod
    def tearDownClass(cls):
        """ Clean-up the fixtures

        Remove database and directory after all the tests have run.
        """
        remove_db(cls._db_path, cls._db_name)

    def setUp(self):
        """ Prepare the fields

        Put values into the fields before calling each test function.
        """
        self._command.insert_course(self._courses)
        self._command.insert_donelist(self._date, self._course_name_python, self._duration)

    def tearDown(self):
        """ Remove fields

        Remove values of the fields after each test function is run.
        """
        self._command.remove_donelist(self._date, self._course_name_python)
        self._command.remove_course(self._course_name_python)
        self._command.remove_course(self._course_name_math)
        self._command.remove_course(self._course_name_eng)

    def test_show_column(self):
        """ Test show_column()

        Assert:
            * show_colmun() calls Database.get_column() and it succeeds.
            * Returns the colmun names as expected.
        """
        course_columns = ['id', 'name']
        donelist_columns = ['id', 'date', 'course', 'duration']

        self.assertListEqual(self._command.show_column('course'), course_columns)
        self.assertListEqual(self._command.show_column('donelist'), donelist_columns)

    def test_show(self):
        """ Test for show()

        Assert;
            * Command.show() calls the Database.show() and it succeeds.
            * RuntimeError is raised if an invalid table name is passed.
        """
        # course
        courses = self._command.show('course')
        count = 0

        while count < len(courses):
            print(courses[count][1])
            self.assertEqual(courses[count][1], self._courses[count])
            count += 1

        # donelist
        records = self._command.show('donelist')
        self.assertEqual(records[0][1], self._date)
        self.assertEqual(records[0][2], self._course_name_python)
        self.assertEqual(records[0][3], self._duration)

        wrong_name = None

        with self.assertRaises(RuntimeError):
            self._command.show(wrong_name)

    def test_insert_course(self):
        """ Test for insert_course()

        Assert insert_course() calls the Database.insert_course().
        """
        self._command.remove_course(self._course_name_python)
        self._command.remove_course(self._course_name_math)
        self._command.remove_course(self._course_name_eng)
        self.assertIsNone(self._command.insert_course(self._courses))

        wrong_course = [None]
        with self.assertRaises(sqlite3.IntegrityError):
            self._command.insert_course(wrong_course)

    def test_insert_donelist(self):
        """ Test for insert_donelist()

        Assert insert_donelist() calls the Database.insert_donelist().
        """
        self._command.remove_donelist(self._date, self._course_name_python)
        self.assertIsNone(
            self._command.insert_donelist(self._date, self._course_name_python, self._duration))
        wrong_duration = None
        with self.assertRaises(sqlite3.IntegrityError):
            self._command.insert_donelist('2018-12-12', self._course_name_python, wrong_duration)

    def test_remove_course(self):
        """ Test for insert_course()

        Assert insert_course() calls the Database.remove_course().
        """
        self.assertIsNone(self._command.remove_course(self._course_name_python))
        self.assertIsNone(self._command.remove_course(self._course_name_math))
        self.assertIsNone(self._command.remove_course(self._course_name_eng))

        wrong_course = 'music'
        with self.assertRaises(RuntimeError):
            self._command.remove_course(wrong_course)

        # Insertion for tearDown()
        self._command.insert_course(self._courses)

    def test_remove_donelist(self):
        """ Test for remove_donelist()

        Assert remove_donelist() calls the Database.remove_donelist().
        """
        self.assertIsNone(self._command.remove_donelist(self._date, self._course_name_python))

        wrong_date = '00000000'
        with self.assertRaises(RuntimeError):
            self._command.remove_donelist(wrong_date, self._course_name_python)

        # Insertion for tearDown()
        self._command.insert_donelist(self._date, self._course_name_python, self._duration)

    def test_dump_to_csv(self):
        """ Test dump_to_csv()

        Assert:
            * The method succeeds with no error and returns None.
            * FileExistsError is raised if file already exists.
        """
        records = self._command.show('course')
        csvfile = self._db_path + 'test.csv'
        fields = self._command.show_column('course')
        self.assertIsNone(self._command.dump_to_csv(records, csvfile, fields))

        with self.assertRaises(FileExistsError):
            self._command.dump_to_csv(records, csvfile, fields)

    def test_dump_to_json(self):
        """ Test dump_to_json()

        Assert:
            * The method succeeds with no error and returns None.
            * FileExistsError is raised if file already exists.
        """
        records = self._command.show('donelist')
        jsonfile = self._db_path + 'test.json'
        self.assertIsNone(self._command.dump_to_json(records, jsonfile))

        with self.assertRaises(FileExistsError):
            self._command.dump_to_json(records, jsonfile)

    def test_show_total_hours(self):
        """ Test show_total_hours()

        Assert that show_total_hours() calls Database.get_total_hours()
        and returns the total hours as expected.
        """
        expected_res = {
            'total_hours': {
                'Total: ': 5
            },
            'total_hours_per_course': {
                'python': 5
            },
            'total_hours_per_week': {
                'Thu': 5
            },
            'total_hours_per_month': {
                'Nov': 5
            }
        }
        self.assertEqual(self._command.show_total_hours(), expected_res)

    def test_show_total_hours_course(self):
        """ Test show_total_hours_course()

        Assert show_total_hours_course() calls
        Database.get_total_hours_course() and returns the total hours per
        course as expected.
        """
        self._command.insert_donelist('2019-05-02', self._course_name_math, '3')
        expected_res = {'total_hours_per_course': {'math': 3, 'python': 5}}
        self.assertDictEqual(self._command.show_total_hours_course(), expected_res)

        # Cleanup
        self._command.remove_donelist('2019-05-02', self._course_name_math)

    def test_show_total_hours_week(self):
        """ Test show_total_hours_week()

        Assert:
            * show_total_hours_week() calls
              database.get_total_hours_week() and it succeeds.
            * Returns the total hours per week as expected.
            * If the course name is passed as an argument, returns the
              total hours per week for each course.
        """
        # Saturday
        self._command.insert_donelist('2019-06-01', self._course_name_math, '3')
        self._command.insert_donelist('2019-06-08', self._course_name_math, '3')

        # Thursday
        self._command.insert_donelist('2019-06-06', self._course_name_python, '5')

        expected_res = {'total_hours_per_week': {'Thu': 10, 'Sat': 6}}
        self.assertDictEqual(self._command.show_total_hours_week(), expected_res)

        # Cleanup
        self._command.remove_donelist('2019-06-01', self._course_name_math)
        self._command.remove_donelist('2019-06-08', self._course_name_math)
        self._command.remove_donelist('2019-06-06', self._course_name_python)

    def test_show_total_hours_month(self):
        """ Test show_total_hours_month()

        Assert:
            * show_total_hours_month() calls
              database.get_total_hours_month() and it succeeds.
            * Returns the total hours per month as expected.
            * If the course name is passed as an argument, returns the
              total hours per month for each course.
        """
        # June
        self._command.insert_donelist('2019-06-01', self._course_name_math, '3')
        self._command.insert_donelist('2019-06-08', self._course_name_math, '3')

        # November
        self._command.insert_donelist('2019-11-01', self._course_name_python, '5')

        expected_res_total = {'total_hours_per_month': {'Jun': 6, 'Nov': 10}}
        expected_res_math = {'total_hours_per_month': {'Jun': 6}}
        expected_res_python = {'total_hours_per_month': {'Nov': 10}}

        self.assertDictEqual(self._command.show_total_hours_month(), expected_res_total)
        self.assertDictEqual(self._command.show_total_hours_month(course='python'),
                             expected_res_python)
        self.assertDictEqual(self._command.show_total_hours_month(course='math'),
                             expected_res_math)

        # Cleanup
        self._command.remove_donelist('2019-06-01', self._course_name_math)
        self._command.remove_donelist('2019-06-08', self._course_name_math)
        self._command.remove_donelist('2019-11-01', self._course_name_python)

    def test_name_months_and_days(self):
        """ Test name_months_and_days()

        Assert that the method succeeds with no error and returns
        names of the months and the days of week.
        """
        month_day_nums = [
            ('01', 1),
            ('02', 2),
            ('12', 12),
            ('0', 1),
            ('1', 10),
            ('6', 60),
        ]
        expected_res = [
            ('Jan', 1),
            ('Feb', 2),
            ('Dec', 12),
            ('Sun', 1),
            ('Mon', 10),
            ('Sat', 60),
        ]
        self.assertEqual(self._command.name_months_and_days(month_day_nums), expected_res)

    def test_map_keys_to_seq(self):
        """ Test map_keys_to_seq()

        Assert that the method succeeds with no error and returns
        a expected dictionary.
        """
        keys = ['per_course', 'per_month']
        total_per_course = [('art', 200), ('math', 100)]
        total_per_month = [('Apr', 200), ('May', 200)]

        expected_res = ({
            'per_course': [('art', 200), ('math', 100)],
            'per_month': [('Apr', 200), ('May', 200)]
        })
        self.assertDictEqual(
            self._command.map_keys_to_seq(keys, total_per_course, total_per_month), expected_res)

    def test_make_dict_from_sequence(self):
        """ Test make_dict_from_sequence()

        Assert that the method succeeds with no error and returns
        a expected dictionary.
        """
        total_courses = [('art', 31), ('eng', 73), ('math', 100), ('python', 105)]
        total_days = [('Sun', 36), ('Mon', 55), ('Tue', 45), ('Wed', 22), ('Thu', 54), ('Fri', 39),
                      ('Sat', 58)]
        total_months = [('Apr', 233), ('May', 76)]

        expected_total_courses = {'art': 31, 'eng': 73, 'math': 100, 'python': 105}
        expected_total_days = {
            'Sun': 36,
            'Mon': 55,
            'Tue': 45,
            'Wed': 22,
            'Thu': 54,
            'Fri': 39,
            'Sat': 58
        }
        expected_total_months = {'Apr': 233, 'May': 76}

        self.assertDictEqual(self._command.make_dict_from_sequence(total_courses),
                             expected_total_courses)
        self.assertDictEqual(self._command.make_dict_from_sequence(total_days),
                             expected_total_days)
        self.assertDictEqual(self._command.make_dict_from_sequence(total_months),
                             expected_total_months)

    def test_map_keys_to_dict(self):
        """ Test map_keys_to_dict()

        Assert that the method succeeds with no error and returns
        a expected dictionary.
        """
        keys = ["total_hours_per_course"]
        seq = [('cooking', 5), ('history', 6)]
        records = self._command.map_keys_to_dict(keys, seq)
        expected_res = {"total_hours_per_course": {"cooking": 5, "history": 6}}
        self.assertDictEqual(records, expected_res)
