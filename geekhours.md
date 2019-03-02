# Geek Hours Command Examples

## Usage
```
$ geekhours -h
usage: geekhours [-h] {course,done} ...

geekhours is a simple study time management tool.

optional arguments:
  -h, --help     show this help message

Synopsis:
  geekhours course list
  geekhours course add course_name [course_name ...]
  geekhours course rm course_name
  geekhours done list
  geekhours done add [--date [date]] [--duration [duration]] course_name
  geekhours done rm date course_name

  {course,done}  Sub commands.
    course       Manipulate course.
    done         Manipulate done.
```

## Add courses

```
$ geekhours course add Python English Math
Add 'Python' in course.
Add 'English' in course.
Add 'Math' in course.
```

## List courses

```
$ geekhours course list
[
    "Python",
    "English",
    "Math"
]
```

## Add a record of study time

```
$ geekhours done add Python -d 20190223 -D 5
Add '20190223 Python 5h' in donelist.

$ geekhours done add English -d 20190223
Add '20190223 English 1h' in donelist.

$ geekhours done add Math
Add '20190302 Math 1h' in donelist.
```

## List records of study time

```
$ geekhours done list
[
    {
        "id": 1,
        "date": "20190223",
        "course": "Python",
        "duration": "5h"
    },{
        "id": 2,
        "date": "20190223",
        "course": "English",
        "duration": "1h"
    },{
        "id': 3,
        "date": "20190302",
        "course": "Math",
        "duration": "1h"
    }
]
```

## Delete a record of study time

```
$ geekhours done rm 20190302 Math
Removed record.
```

## Delete a course

```
$ geekhours course rm English
Removed 'English' from course.
```
