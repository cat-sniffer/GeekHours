# Specification

**Table of Contents**

- [Specification](#specification)
    - [Files and directories](#files-and-directories)
    - [Database schema](#database-schema)
    - [Database access methods](#database-access-methods)

## Files and directories

TODO: Where to save sqlite database file? How is a permission?

## Database schema

GeekHours saves data to `sqlite` using `sqlite3` of the Python 3. The following is the database schema.

TODO: Exact type will be defined.

Field    | Type   | Null | Key | Default | Note
-----    | ----   | ---- | --- | ------- | -----
`id`     | int    | NO   | PRI | NULL    | A primary key
`date`   | date   | NO   |     | NULL    | Studied date
`course` | string | NO   |     | NULL    | Course which user studied
`time`   | time   | NO   |     | NULL    | Studied time duration

## Database access methods

TODO: How to insert, update and delete using python? Define class and method here.
