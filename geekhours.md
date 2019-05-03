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
  geekhours sum
  geekhours sum course
  geekhours sum week [-c|--course [course_name]]
  geekhours sum month [-c|--course [course_name]]

  {course,done,sum}  Sub commands.
    course           Manipulate course.
    done             Manipulate done.
    sum              Display the total hours studied.
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

## Format records to comma separated CSV or JSON

The '-f' and '--format' options can be used to write records to comma separated CSV or JSON.

### `geekhours course list` command:

`courses.csv` or `courses.json` will be created depending on the format type.

```
$ geekhours course list -f|--format csv|json
```

### `geekhours done list` command:

`records.csv` or `records.json` will be created depending on the format type.

```
$ geekhours done list -f|--format csv|json
```

### Specify the file name

File name can be specified by giving it to `-o` or `--output` options.

```
$ geekhours course list -f csv -o [FILE-PATH]
$ geekhours done list --format json --output [FILE-PATH]
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

## Display the total hours

```
$ geekhours sum
{
    "total_hours": {
        "Total: ": 311.5
    },
    "total_hours_per_course": {
        "art": 31,
        "eng": 74,
        "math": 100,
        "python": 106.5
    },
    "total_hours_per_week": {
        "Sun": 36,
        "Mon": 55.5,
        "Tue": 45,
        "Wed": 22,
        "Thu": 56,
        "Fri": 39,
        "Sat": 58
    },
    "total_hours_per_month": {
        "Apr": 233,
        "May": 78.5
    }
}
```

## Total hours per course

```
$ geekhours sum course
{
    "total_hours_per_course": {
        "art": 31,
        "eng": 74,
        "math": 100,
        "python": 106.5
    }
}
```

### Total hours per week

```
$ geekhours sum week
{
    "total_hours_per_week": {
        "Sun": 36,
        "Mon": 55.5,
        "Tue": 45,
        "Wed": 22,
        "Thu": 56,
        "Fri": 39,
        "Sat": 58
    }
}
```

#### Total hours per week by course

To get the total number of hours per week for each course,
specify a course name to `-c` or `--course` options.

```
$ geekhours sum week -c art
{
    "total_hours_per_week": {
        "Mon": 5,
        "Tue": 2,
        "Wed": 3,
        "Thu": 17,
        "Fri": 1,
        "Sat": 3
    }
}
```

### Total hours per month

```
$ geekhours sum month
{
    "total_hours_per_month": {
        "Apr": 233,
        "May": 78.5
    }
}
```

#### Total hours per month by course

To get the total number of hours per month for each course,
specify a course name to `-c` or `--course` options.

```
$ geekhours sum month --course art
{
    "total_hours_per_month": {
        "Apr": 23,
        "May": 8
    }
}
```
