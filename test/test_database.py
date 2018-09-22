""" Unit test for Database module. """

from os import path, remove
import unittest
from lib.database import Database

class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """ Prepare the test fixtures which is needed for this unittest. """
        # Prepare the fixtures
        db_name = '.geekhours.db'
        cls._db_path = path.join(path.dirname(__file__), db_name)
        cls._db = Database()

    @classmethod
    def tearDownClass(cls):
        """ Remove the database for this test after all the tests have run. """
        remove(cls._db_path)

    def setUp(self):
        """ Connect database before calling each test function. """
        self.connect = self._db.connect_db(self._db_path)

    def tearDown(self):
        """ Close database after each test function. """
        self._db.close_db()

    def test_connect_db(self):
        """ Test connect_db connects the database. """
        cls_name = self._db.con.__class__
        check_cls_name = "<class 'sqlite3.Connection'>"
        self.assertEqual(str(cls_name), check_cls_name)

    def test_close_db(self):
        """
        Test close_db() close the database.
        Verify it closes object-id of 'connenct()'.
        """
        self._db.connect_db(self._db_path)
        self._db.close_db()

        """
        '(hex(id(self._db.con)))' returns
        '<built-in method close of sqlite3.Connection object at CONNECTED_ID>'.
        Assert that the connected id is closed.
        """
        connected_id = (hex(id(self._db.con)))
        closed_id = self._db.con.close
        closed_id = str(closed_id)

        self.assertIn(connected_id, closed_id)
