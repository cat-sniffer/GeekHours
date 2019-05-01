""" Unit test for Database module. """

import unittest
import sqlite3
from geekhours.database import Database
from geekhours.util import create_db, remove_db


class TestDatabase(unittest.TestCase):
    """ Test cases of the unit test for Database class """

    @classmethod
    def setUpClass(cls):
        """ Prepare the test fixtures

        setUpClass() is the first method to be called.
        """
        cls._db_path, cls._db_name = create_db()
        setup_db = Database(cls._db_name)
        setup_db.create_table()
        setup_db.close_db()
        cls._donelist = 'donelist'
        cls._course = 'course'
        cls._course_name = 'python'
        cls._date = '2018-08-01'
        cls._duration = '5'
        cls._courses = [('python'), ('art'), ('math')]

    @classmethod
    def tearDownClass(cls):
        """ Remove database and directory

        tearDownClass() is called after all the tests have run.
        """
        remove_db(cls._db_path, cls._db_name)

    def setUp(self):
        """ Connect database

        setUp() is called before calling each test function.
        """
        self.database = Database(self._db_name)

    def tearDown(self):
        """ Delete records and close database

        tearDown() is called after each test function is run.
        """
        self.database.cur.execute('DELETE FROM donelist')
        self.database.con.commit()
        self.database.cur.execute('DELETE FROM course')
        self.database.con.commit()
        self.database.close_db()

    def test_close_db(self):
        """ Test for close_db()

        Check that the object-id of qlite3.connect() is closed.
        """
        connected_id = (hex(id(self.database.con)))
        self.database.close_db()
        closed_id = self.database.con.close
        closed_id = str(closed_id)
        self.assertIn(connected_id, closed_id)

        # Open database to make tearDown pass
        self.database = Database(self._db_name)

    def test_create_table(self):
        """ Test for create_table()

        Check that the created table is the expected one.
        """
        # Prepare the table schemas
        expected_donelist = ("CREATE TABLE donelist ("
                             "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                             "date TEXT NOT NULL, "
                             "course TEXT NOT NULL, "
                             "duration TEXT NOT NULL)")

        expected_course = ("CREATE TABLE course ("
                           "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                           "name TEXT NOT NULL UNIQUE)")

        # donelist
        donelist = self.database.cur.execute("SELECT sql from sqlite_master \
                                             WHERE type = 'table' AND name = 'donelist'")
        # Cast string to tuple to assertEqual() table schemas
        expected_donelist = tuple([expected_donelist])
        self.assertEqual(donelist.fetchone(), expected_donelist)

        # course
        course = self.database.cur.execute("SELECT sql from sqlite_master \
                                           WHERE type = 'table' AND name = 'course'")
        expected_course = tuple([expected_course])
        self.assertEqual(course.fetchone(), expected_course)

    def test_get_column(self):
        """ Test get_colmun()

        Assert get_colmun() returns colmun names of the records.
        """
        course_columns = ['id', 'name']
        donelist_columns = ['id', 'date', 'course', 'duration']

        self.database.insert_course(self._courses)
        self.assertEqual(self.database.get_column(self._course), course_columns)
        self.database.insert_donelist(self._date, self._course_name, self._duration)
        self.assertEqual(self.database.get_column(self._donelist), donelist_columns)

    def test_show(self):
        """ Test for show()

        Check:
        * if valid table name is passed, return records of the table.
        * if invalid table name is passed, return False.
        """
        invalid_table = 'test'

        # course
        self.database.insert_course(self._courses)
        ret = self.database.show(self._course)
        i = 0

        while i < len(ret):
            self.assertEqual(ret[i][1], self._courses[i])
            i += 1

        with self.assertRaises(RuntimeError):
            self.database.show(invalid_table)

        # donelist
        self.database.insert_donelist(self._date, self._course_name, self._duration)
        ret = self.database.show(self._donelist)
        self.assertEqual(ret[0][1], self._date)
        self.assertEqual(ret[0][2], self._course_name)
        self.assertEqual(ret[0][3], self._duration)

        with self.assertRaises(RuntimeError):
            self.database.show(invalid_table)

    def test_insert_course(self):
        """ Test for insert_course()

        Check:
        * when SQL statement succeeds, None will be returned.
        * when SQL statement fails, exception will be returned.
        """
        courses = [('python'), ('python')]
        self.assertIsNone(self.database.insert_course(self._courses))

        with self.assertRaises(sqlite3.IntegrityError):
            self.database.insert_course(courses)

    def test_insert_donelist(self):
        """ Test for insert_donelist()

        Check that
        * None is returned when SQL statement succeeds.
        * Exception is returned when SQL statement fails.
        * ValueError is raised if the date is not in YYYY-MM-DD format.
        """
        self.database.insert_course(self._courses)
        self.assertIsNone(
            self.database.insert_donelist(self._date, self._course_name, self._duration))

        course_name = 'japanese'

        with self.assertRaises(RuntimeError):
            self.database.insert_donelist(self._date, course_name, self._duration)

        with self.assertRaises(RuntimeError):
            self.database.insert_donelist(self._date, self._course_name, self._duration)

    def test_remove_course(self):
        """ Test for remove_course()

        Check that
        * None is returned when SQL statement succeeds.
        * Exception is returned when SQL statement fails.
        """
        self.database.insert_course(self._courses)
        self.assertIsNone(self.database.remove_course(self._course_name))

        with self.assertRaises(RuntimeError):
            self.database.remove_course(self._course_name)

    def test_remove_donelist(self):
        """ Test for remove_donelist()

        Check that
        * None is returned when SQL statement succeeds.
        * Exception is returned when SQL statement fails.
        """
        self.database.insert_course(self._courses)
        self.database.insert_donelist(self._date, self._course_name, self._duration)
        self.assertIsNone(self.database.remove_donelist(self._date, self._course_name))

        with self.assertRaises(RuntimeError):
            self.database.remove_donelist(self._date, self._course_name)

    def test_get_total_hours(self):
        """ Test get_total_hours()

        Assert that get_total_hours() returns the total hours as expected.
        """
        total = [('Total: ', 4)]
        self.database.insert_course(self._courses)
        self.database.insert_donelist('2019-04-01', 'python', '2')
        self.database.insert_donelist('2019-05-01', 'art', '2')
        self.assertEqual(self.database.get_total_hours(), total)

    def test_get_total_hours_course(self):
        """ Test get_total_hours_course()

        Assert that get_total_hours_course() returns the total number of
        hours per course as expected.
        """
        check_total = [('art', 6), ('python', 4)]

        self.database.insert_course(self._courses)
        self.database.insert_donelist('2019-04-01', 'python', '2')
        self.database.insert_donelist('2019-05-01', 'python', '2')
        self.database.insert_donelist('2019-04-30', 'art', '3')
        self.database.insert_donelist('2019-05-01', 'art', '3')
        total = self.database.get_total_hours_course()
        self.assertEqual(total, check_total)

    def test_get_total_hours_week(self):
        """ Test get_total_hours_week()

        Assert:
            * get_total_hours_course() returns the total hours per week
              as expected.
            * If the course name is passed as an argument, return the
              total hours per week for each course.
        """
        self.database.insert_course(self._courses)

        # Monday python
        self.database.insert_donelist('2019-04-01', 'python', '1')
        self.database.insert_donelist('2019-04-29', 'python', '1')
        self.database.insert_donelist('2019-04-29', 'art', '2')
        self.database.insert_donelist('2019-05-06', 'art', '2')

        # Tuesday python
        self.database.insert_donelist('2019-04-02', 'python', '2')
        self.database.insert_donelist('2019-04-30', 'python', '2')
        self.database.insert_donelist('2019-05-07', 'art', '3')

        courses = [('1', 6), ('2', 7)]
        python = [('1', 2), ('2', 4)]
        art = [('1', 4), ('2', 3)]

        self.assertEqual(self.database.get_total_hours_week(), courses)
        self.assertEqual(self.database.get_total_hours_week(course='python'), python)
        self.assertEqual(self.database.get_total_hours_week(course='art'), art)

    def test_get_total_hours_month(self):
        """ Test get_total_hours_month()

        Assert:
            * get_total_hours_course() returns the total hours per month
              as expected.
            * If the course name is passed as an argument, return the
              total hours per month for each course.
        """
        self.database.insert_course(self._courses)

        # April
        self.database.insert_donelist('2019-04-01', 'python', '2')
        self.database.insert_donelist('2019-04-01', 'art', '2')
        self.database.insert_donelist('2019-04-29', 'art', '2')

        # May python
        self.database.insert_donelist('2019-05-01', 'python', '2')
        self.database.insert_donelist('2019-05-02', 'python', '2')
        self.database.insert_donelist('2019-05-03', 'art', '5')

        courses = [('04', 6), ('05', 9)]
        python = [('04', 2), ('05', 4)]
        art = [('04', 4), ('05', 5)]

        self.assertEqual(self.database.get_total_hours_month(), courses)
        self.assertEqual(self.database.get_total_hours_month(course='python'), python)
        self.assertEqual(self.database.get_total_hours_month(course='art'), art)
