""" Common Utilities """

from os import remove, rmdir
from tempfile import mkstemp, mkdtemp


def create_db():
    """ Create temporary database. """
    db_path = mkdtemp()
    db_name = mkstemp(suffix='.db', dir=db_path)
    db_name = str(db_name[1])
    return db_path, db_name


def remove_db(db_path: str, db_name: str):
    """ Remove temporary database. """
    remove(db_name)
    rmdir(db_path)
