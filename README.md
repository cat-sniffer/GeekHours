# Geek Hours
[![CircleCI](https://img.shields.io/circleci/project/github/YukieK/GeekHours.svg?style=flat-square)](https://circleci.com/gh/YukieK/GeekHours)
[![PyPI version](https://img.shields.io/pypi/v/GeekHours.svg?color=%2351A5DC&style=flat-square)](https://pypi.org/project/geekhours/)
[![GitHub license](https://img.shields.io/github/license/YukieK/geekhours.svg?color=%23e84566&style=flat-square)](https://github.com/YukieK/GeekHours/blob/master/LICENSE)

**Table of Contents**

- [Geek Hours](#geek-hours)
  - [Overview](#overview)
  - [Prerequisites](#prerequisites)
  - [Installing](#installing)
  - [Usage](#usage)
    - [Record](#record)
    - [List](#list)
    - [Delete](#delete)
  - [Command Examples](#command-examples)
  - [Specifications](#specifications)
  - [License](#license)

## Overview

**Geek Hours** is a simple study time management tool.

## Prerequisites

* Ubuntu **16.04** or later

* Python **3.5** or later

* SQLite **3.11.0** or later

## Installing

Install from PyPI via pip.

```
pip3 install geekhours
```

## Usage

### Record

Register course names you study.

```
geekhours course add course_name [course_name ...]
```

Record date, course and time you studied.

```
geekhours done add [-d [DATE]] [-D [DURATION]] course_name
```

### List

List courses:

```
geekhours course list
```

List study records:

```
geekhours done list
```

### Delete

Delete a course:

```
geekhours course rm course_name
```

Delete a study record:
```
geekhours done rm date course_name
```

## Command Examples

[geekhours.md](geekhours.md)

## Specifications

[SPEC.md](SPEC.md)

## License

This project is licensed under the MIT License.

[LICENSE](LICENSE)
