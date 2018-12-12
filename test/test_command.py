""" Unit test for Command module. """

import unittest
from lib.command import Command
from lib.util import create_db, remove_db


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
        cls._date = '20181101'
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

    def test_show(self):
        """ Test for show()

        Assert show() calls the Database.show().
        """
        self.assertIsNone(self._command.show('course'))
        self.assertIsNone(self._command.show('donelist'))

    def test_insert_course(self):
        """ Test for insert_course()

        Assert insert_course() calls the Database.insert_course().
        """
        self._command.remove_course(self._course_name_python)
        self._command.remove_course(self._course_name_math)
        self._command.remove_course(self._course_name_eng)
        self.assertIsNone(self._command.insert_course(self._courses))

    def test_insert_donelist(self):
        """ Test for insert_donelist()

        Assert insert_donelist() calls the Database.insert_donelist().
        """
        self._command.remove_donelist(self._date, self._course_name_python)
        self.assertIsNone(
            self._command.insert_donelist(self._date, self._course_name_python,
                                              self._duration))

    def test_remove_course(self):
        """ Test for insert_course()

        Assert insert_course() calls the Database.remove_course().
        """
        self.assertIsNone(self._command.remove_course(self._course_name_python))
        self.assertIsNone(self._command.remove_course(self._course_name_math))
        self.assertIsNone(self._command.remove_course(self._course_name_eng))

        # Insertion for tearDown()
        self._command.insert_course(self._courses)

    def test_remove_donelist(self):
        """ Test for remove_donelist()

        Assert remove_donelist() calls the Database.remove_donelist().
        """
        self.assertIsNone(self._command.remove_donelist(self._date, self._course_name_python))

        # Insertion for tearDown()
        self._command.insert_donelist(self._date, self._course_name_python, self._duration)
