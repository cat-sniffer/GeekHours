# Specification

**Table of Contents**

- [Specification](#specification)
    - [Files and directories](#files-and-directories)
    - [Database schema](#database-schema)
    - [Database access methods](#database-access-methods)

## Overview

![UML class diagram](http://www.plantuml.com/plantuml/png/JP3DQiCm48JlVWf1BoqqVO1WJ4hhb5nA2JxqPjRMueZe9qYhvb3oxfMsiP1E-iQZdLdl0e6dQ7GpQmX1l0F1105_6o5cPotEDChfyIbXW1yizvExZicfaL7PW9v6xwwCyIA1iA14ZGLlpJtfpHa3LkQW1LC84CzYEBdeGw4v4p9wN5GWz5LC5V4__WBp6HPCJ_7CWrxa9DfstQphU3VkK2pf-_3yiD-_fiE6T9JSYiFdq7_qHz5-7GyTgpboAuR-Us0aPMhaghKWemTIpjOIbowl-NhBnTU6OhDP_qvJBv7rrTFiqCfez1y0)

## Files and directories

The sqlite database file is saved as `$HOME/.geekhours.db` with 664 permission.

## Database schema

GeekHours saves data to `sqlite` using `sqlite3` of the Python 3. The following is the database schema.

Field      | Type    | Null | Key | Default | Note
-----      | ----    | ---- | --- | ------- | -----
`id`       | INTEGER | NO   | PRI |         | A primary key
`date`     | TEXT    | NO   |     | date()  | Studied date
`course`   | TEXT    | NO   |     | 'Error' | Course which user studied
`duration` | TEXT    | NO   |     | time()  | Studied time duration

## Database access methods

GeekHours have 2 modules. One is `command` module defined `Command` class to handle inputs from stdin,
and the other is `database` module defined `Database` class to connect/close database and /insert/update/delete
records.

The `command` module defines the following functions:

get_date()
get_hours()
get_course()
register()
update()
delete()

The `database` module defines the following functions:

connect_db()
save_db()
show_table()
insert_row()
update_row()
delete_row()
