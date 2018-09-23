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
        cls._connection = cls._db.connect_db(cls._db_path)
        cls._tables = cls._db.create_table()
        cls._donelist = 'donelist'
        cls._course = 'course'
        cls._course_name = 'python'
        cls._date = '0801'
        cls._duration = '5'
        cls._donelist_fields = (cls._date, cls._course_name, cls._duration)
        cls._course_fields = [('python'), ('art'), ('math')]

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

    def test_create_table(self):
        """
        Test create_table() creates a table.
        Verify that the table schema and the table schema created by SetUpClass() are equal.
        """
        # Prepare the table schemas
        donelist_clm = ("CREATE TABLE donelist ("
                        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                        "date TEXT NOT NULL, "
                        "course TEXT NOT NULL, "
                        "duration TEXT NOT NULL)")

        course_clm = ("CREATE TABLE course ("
                      "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                      "name TEXT NOT NULL)")

        ##### donelist
        donelist = self._db.cur.execute("SELECT sql from sqlite_master \
                                             WHERE type = 'table' AND name = 'donelist'")
        # Cast string to tuple to assertEqual() table schemas
        donelist_clm = tuple([donelist_clm])
        self.assertEqual(donelist.fetchone(), donelist_clm)

        ##### course
        course = self._db.cur.execute("SELECT sql from sqlite_master \
                                           WHERE type = 'table' AND name = 'course'")
        course_clm = tuple([course_clm])
        self.assertEqual(course.fetchone(), course_clm)

    def test_show(self):
        """
        Test show() shows the records.
        Verify that the inserted record and retrieved record are equal.
        """
        ##### course
        self._db.insert(self._course, self._course_fields)
        course = self._db.cur.execute('SELECT * FROM course').fetchall()
        # course: [(1, 'python'), (2, 'art'), (3, 'math')]
        # self._course_fields: ['python', 'art', 'math']
        self.assertEqual(course[0][1], self._course_fields[0])
        self.assertEqual(course[1][1], self._course_fields[1])
        self.assertEqual(course[2][1], self._course_fields[2])

        ###### donelist
        self._db.insert(self._donelist, self._donelist_fields)
        donelist = self._db.cur.execute('SELECT * FROM donelist').fetchall()
        # donelist: [(1, '0801', 'python', '5')]
        self.assertEqual(donelist[0][1:], self._donelist_fields)

    def test_update(self):
        """ Test that update() replace a record and update it appropriately. """
        self._db.insert(self._course, self._course_fields)
        self._db.insert(self._donelist, self._donelist_fields)
        update_donelist = ('0802', 'art', '3')
        update_course = ('history')
        self._db.cur.execute('UPDATE donelist SET date=?, course=?, duration=? WHERE course=?\
                                  AND date=?', (update_donelist[0], update_donelist[1],
                                                update_donelist[2], self._course_name,
                                                self._date,))
        self._db.cur.execute('UPDATE course SET name=? WHERE name=?',
                             (update_course, self._course_name,))
        self._db.con.commit()

        ##### course
        check_course = self._db.cur.execute('SELECT * FROM course').fetchall()
        self.assertNotIn(self._course_name, check_course)
        # Get the index number of a field to be replaced
        index = self._course_fields.index(self._course_name)
        # Replace the field with new corse name
        self._course_fields[index] = update_course
        # Create a list of updated fields of course
        lst = []
        for elem in check_course:
            lst.append(elem[1])
        self.assertIn(update_course, lst)

        ##### donelist
        check_donelist = self._db.cur.execute('SELECT * FROM donelist').fetchall()
        # Assert that "original fields" are not in "updated fileds"
        self.assertNotIn(self._course_name and self._date and self._duration, check_donelist)
        # 'check_donelist[0][1:]' for the ID elimination
        self.assertEqual(update_donelist, check_donelist[0][1:])

    def test_remove(self):
        """
        Test remove() removes a record.
        Record of table 'donelist' should be deleted by matching date and course name.
        Record of table 'course' should be deleted by matching course name.
        """
        #self._db.insert_record(self._course, self._courses)
        self._db.insert(self._course, self._course_fields)
        #self._db.insert_record(self._donelist, self._record)
        self._db.insert(self._donelist, self._donelist_fields)
        self._db.cur.execute('DELETE FROM donelist WHERE course=? AND date=?',
                             (self._course_name, self._date,))
        self._db.cur.execute('DELETE FROM course WHERE name=?', (self._course_name,))
        self._db.con.commit()

        ##### course
        #check_course = self._db.show(self._course)
        check_course = self._db.cur.execute('SELECT * FROM course').fetchall()
        self.assertNotIn(self._course_name, check_course)

        ##### donelist
        #check_donelist = self._db.show(self._donelist)
        check_donelist = self._db.cur.execute('SELECT * FROM donelist').fetchall()
        self.assertNotIn(self._course_name and self._date, check_donelist)


        # Restore records to the original record for next tests.
        self._db.cur.execute('INSERT INTO course(id, name) VALUES (?, ?)',
                             (1, self._course_name,))
        self._db.con.commit()
