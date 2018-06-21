# Specification

**Table of Contents**

- [Specification](#specification)
    - [Overview](#overview)
    - [Files and directories](#files-and-directories)
    - [Database schema](#database-schema)
    - [Database access methods](#database-access-methods)

## Overview

![UML class diagram](http://www.plantuml.com/plantuml/png/LP3BIiGm58RtVOg06mN71nXA6T6Ek14Pkd1NJfj36oQN8Jbn5ZBlRYusnAxo_UVo_wS7Hs39AzdC4fnZhq0mWSEVXh7PQ8qpZNowVmZeu1lBUpNNCNHAJ2YqGqkZDTU4_iA1i217YGLlpP_JYr4AD8z62mOJeBmhmcgyTONcIBbeSH6Eq5OsbKLUVu7v30k6KJodHKzyOcsxNTPrqJ9dA2sXFZpU7O_FuSiDuIY-P-yVG__MdrZxUUgI61ttREY_XeGaL8qvQILmRu64qPMqPSxJ-NcBkRU0R6V5ijBsWofzz--cve2QUoL_0G00)

## Files and directories

The sqlite database file is saved as `$HOME/.geekhours.db` with 664 permission.

## Database schema

GeekHours saves data to `sqlite` using `sqlite3` of the Python 3. The following is the database schema.

**Donelist:**

Field      | Type Affinity | Null | Key | Default | Note
-----      | ------------- | ---- | --- | ------- | -----
`id`       | INTEGER       | NO   | PRI | `id`+1  | A primary key
`date`     | TEXT          | NO   |     | date()  | Studied date
`course`   | TEXT          | NO   |     | Unknown | Course which user studied
`duration` | TEXT          | NO   |     | time()  | Studied time duration

**Course:**

Field      | Type Affinity | Null | Key | Default | Note
-----      | ------------- | ---- | --- | ------- | -----
`id`       | INTEGER       | NO   | PRI | `id`+1  | A primary key
`name`     | TEXT          | NO   |     | Unknown | Course name

## Database access methods

GeekHours have 2 modules. One is `command` module defined `Command` class to handle inputs from stdin,
and the other is `database` module defined `Database` class to connect/close database and /insert/update/delete
records.
