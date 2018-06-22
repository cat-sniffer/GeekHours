# Specification

**Table of Contents**

- [Specification](#specification)
    - [Overview](#overview)
    - [Files and directories](#files-and-directories)
    - [Database schema](#database-schema)
    - [Database access methods](#database-access-methods)

## Overview

![uml class diagram](http://www.plantuml.com/plantuml/png/bP71QeD048RlFiL2BoqqVO0WafAQaaifmKDlChg3IjRTi3lR74hUlHDr5_MM1G_pxJYV_xXp19Pyhv9QWNFY0mWgSFYN23wrqHfhAcNr_3801xyugrfpBRbVuGGwxT1IQSrr0luYWN0692gCu9PCrhtfUz1ob3R8GY2U6SlMUEjcTNslGuF5fdE4Tg5Sw4RL1UepDCW3y3mCV9ELIDEGECj6_RG7er7nM6ueNfyEXtS-eMD8AhVY-5Nad_b9fD-dOnPlxlQjAFAV8YBg-ZKQ4woWz1QeCtgDGvuuBPGtVXwEjX_KZmVJi4WHt44YDhPhMWh_SiOtY-zAuchZ2to1oGwrzBtw1m00)

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

GeekHours have 2 modules. One is `command` module defined `Command` class to handle inputs from stdin.
And the other is `database` module defined `Database` class to communicate with a database such as
connect/close and insert/update/delete records.
