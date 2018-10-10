""" Unit test for Database module. """

from os import remove, rmdir
import unittest
import sqlite3
from tempfile import mkstemp, mkdtemp
from lib.database import Database

class TestDatabase(unittest.TestCase):
    """ Test cases of the unit test for Database class """
    @classmethod
    def setUpClass(cls):
        """ Prepare the test fixtures

        setUpClass() is the first method to be called.
        """
        cls._db_path = mkdtemp()
        cls._db_name = mkstemp(suffix='.db', dir=cls._db_path)
        cls._db_name = str(cls._db_name[1])
        cls._db = Database()
        cls._db.connect_db(cls._db_name)
        cls._db.create_table()
        cls._db.close_db()
        cls._donelist = 'donelist'
        cls._course = 'course'
        cls._course_name = 'python'
        cls._date = '0801'
        cls._duration = '5'
        cls._courses = [('python'), ('art'), ('math')]

    @classmethod
    def tearDownClass(cls):
        """ Remove database and directory

        tearDownClass() is called after all the tests have run.
        """
        remove(cls._db_name)
        rmdir(cls._db_path)

    def setUp(self):
        """ Connect database

        setUp() is called before calling each test function.
        """
        self._db.connect_db(self._db_name)

    def tearDown(self):
        """ Delete records and close database

        tearDown() is called after each test function is run.
        """
        self._db.cur.execute('DELETE FROM donelist')
        self._db.con.commit()
        self._db.cur.execute('DELETE FROM course')
        self._db.con.commit()
        self._db.close_db()

    def test_connect_db(self):
        """ Test for connect_db()

        Check that connect_db() is successful and None is returned.
        """
        ret = self._db.connect_db(self._db_name)
        self.assertIsNone(ret)

    def test_close_db(self):
        """ Test for close_db()

        Check that the object-id of qlite3.onnenct() is closed.
        """
        self._db.connect_db(self._db_name)
        self._db.close_db()
        connected_id = (hex(id(self._db.con)))
        closed_id = self._db.con.close
        closed_id = str(closed_id)
        self.assertIn(connected_id, closed_id)

        # Open database to make tearDown pass
        self._db.connect_db(self._db_name)

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

        ##### donelist
        donelist = self._db.cur.execute("SELECT sql from sqlite_master \
                                             WHERE type = 'table' AND name = 'donelist'")
        # Cast string to tuple to assertEqual() table schemas
        expected_donelist = tuple([expected_donelist])
        self.assertEqual(donelist.fetchone(), expected_donelist)

        ##### course
        course = self._db.cur.execute("SELECT sql from sqlite_master \
                                           WHERE type = 'table' AND name = 'course'")
        expected_course = tuple([expected_course])
        self.assertEqual(course.fetchone(), expected_course)

        with self.assertRaises((sqlite3.OperationalError)):
            self._db.create_table()

    def test_show(self):
        """ Test for show()

        Check:
        * if valid table name is passed, return records of the table.
        * if invalid table name is passed, return False.
        """
        invalid_table = 'test'

        ##### course
        self._db.insert_course(self._courses)
        ret = self._db.show(self._course)
        i = 0

        while i < len(ret):
            self.assertEqual(ret[i][1], self._courses[i])
            i += 1

        with self.assertRaises(RuntimeError):
            self._db.show(invalid_table)

        ###### donelist
        self._db.insert_donelist(self._date, self._course_name, self._duration)
        ret = self._db.show(self._donelist)
        self.assertEqual(ret[0][1], self._date)
        self.assertEqual(ret[0][2], self._course_name)
        self.assertEqual(ret[0][3], self._duration)

        with self.assertRaises(RuntimeError):
            self._db.show(invalid_table)

    def test_insert_course(self):
        """ Test for insert_course()

        Check:
        * when SQL statement succeeds, None will be returned.
        * when SQL statement fails, exception will be returned.
        """
        courses = [('python'), ('python')]
        ret = self._db.insert_course(self._courses)
        self.assertIsNone(ret)

        with self.assertRaises(sqlite3.IntegrityError):
            self._db.insert_course(courses)

    def test_insert_donelist(self):
        """ Test for insert_donelist()

        Check that
        * None is returned when SQL statement succeeds.
        * Exception is returned when SQL statement fails.
        """
        self._db.insert_course(self._courses)
        ret = self._db.insert_donelist(self._date, self._course_name, self._duration)
        self.assertIsNone(ret)

        course_name = 'japanese'
        with self.assertRaises(RuntimeError):
            self._db.insert_donelist(self._date, course_name, self._duration)

        with self.assertRaises(RuntimeError):
            self._db.insert_donelist(self._date, self._course_name, self._duration)

    def test_update_course(self):
        """ Test for update_course()

        Check that
        * None is returned when SQL statement succeeds.
        * Exception is returned when SQL statement fails.
        """
        new_course = 'history'
        self._db.insert_course(self._courses)
        ret = self._db.update_course(self._course_name, new_course)
        self.assertIsNone(ret)

        with self.assertRaises(RuntimeError):
            self._db.update_course(self._course_name, new_course)

    def test_update_donelist(self):
        """ Test for update_doelist()

        Check that
        * None is returned when SQL statement succeeds.
        * Exception is returned when SQL statement fails.
        """
        new_date = '1001'
        new_course = 'history'
        new_duration = '1'

        self._db.insert_course(self._courses)
        self._db.insert_donelist(self._date, self._course_name, self._duration)
        ret = self._db.update_donelist(self._date, self._course_name, new_date, new_course, new_duration)
        self.assertIsNone(ret)

        with self.assertRaises(RuntimeError):
            self._db.update_donelist(self._date, self._course_name, new_date, new_course, new_duration)

    def test_remove_course(self):
        """ Test for remove_course()

        Check that
        * None is returned when SQL statement succeeds.
        * Exception is returned when SQL statement fails.
        """
        self._db.insert_course(self._courses)
        ret = self._db.remove_course(self._course_name)
        self.assertIsNone(ret)

        with self.assertRaises(RuntimeError):
            self._db.remove_course(self._course_name)

    def test_remove_donelist(self):
        """ Test for remove_donelist()

        Check that
        * None is returned when SQL statement succeeds.
        * Exception is returned when SQL statement fails.
        """
        self._db.insert_course(self._courses)
        self._db.insert_donelist(self._date, self._course_name, self._duration)
        ret = self._db.remove_donelist(self._date, self._course_name)
        self.assertIsNone(ret)

        with self.assertRaises(RuntimeError):
            self._db.remove_donelist(self._date, self._course_name)
