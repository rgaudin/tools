#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

"""  Ethiopian Calendar tool for Python 2.6

Copyright (c) 2010 Renaud Gaudin <rgaudin@gmail.com>

This tool is a python port of Java Code from Ealet 2.0 by Senamirmir Project.

This code is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This code is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA """

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
import datetime
from six.moves import range


class EthiopianDateConverter(object):

    """ Class methods for converting between Ethiopian and Gregorian """

    @classmethod
    def _start_day_of_ethiopian(cls, year):
        """ returns first day of that Ethiopian year

        Params:
        * year: an int """

        # magic formula gives start of year
        new_year_day = (year // 100) - (year // 400) - 4

        # if the prev ethiopian year is a leap year, new-year occrus on 12th
        if (year - 1) % 4 == 3:
            new_year_day += 1

        return new_year_day

    @classmethod
    def date_to_gregorian(cls, adate):
        """ Gregorian date object representation of provided Ethiopian date

        Shortcut to to_gregorian() classmethod using a date parameter

        Params:
        * adate: date object """

        return cls.to_gregorian(adate.year, adate.month, adate.day)

    @classmethod
    def date_to_ethiopian(cls, adate):
        """ Ethiopian date object representation of provided Gregorian date

        Shortcut to to_ethiopian() classmethod using a date parameter

        Params:
        * adate: date object """

        return cls.to_ethiopian(adate.year, adate.month, adate.day)

    @classmethod
    def to_gregorian(cls, year, month, date):
        """ Gregorian date object representation of provided Ethiopian date

        Params:
        * year: an int
        * month: an int
        * date: an int """

        # prevent incorect input
        inputs = (year, month, date)
        if 0 in inputs or [data.__class__ for data in inputs].count(int) != 3:
            raise ValueError("Malformed input can't be converted.")

        # Ethiopian new year in Gregorian calendar
        new_year_day = cls._start_day_of_ethiopian(year)

        # September (Ethiopian) sees 7y difference
        gregorian_year = year + 7

        # Number of days in gregorian months
        # starting with September (index 1)
        # Index 0 is reserved for leap years switches.
        gregorian_months = [0, 30, 31, 30, 31, 31, 28, \
                            31, 30, 31, 30, 31, 31, 30]

        # if next gregorian year is leap year, February has 29 days.
        next_year = gregorian_year + 1
        if (next_year % 4 == 0 and next_year % 100 != 0) \
           or next_year % 400 == 0:
            gregorian_months[6] = 29

        # calculate number of days up to that date
        until = ((month - 1) * 30) + date
        if until <= 37 and year <= 1575:  # mysterious rule
            until += 28
            gregorian_months[0] = 31
        else:
            until += new_year_day - 1

        # if ethiopian year is leap year, paguemain has six days
        if year - 1 % 4 == 3:
            until += 1

        # calculate month and date incremently
        m = 0
        for i in range(0, gregorian_months.__len__()):
            if until <= gregorian_months[i]:
                m = i
                gregorian_date = until
                break
            else:
                m = i
                until -= gregorian_months[i]

        # if m > 4, we're already on next Gregorian year
        if m > 4:
            gregorian_year += 1

        # Gregorian months ordered according to Ethiopian
        order = [8, 9, 10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        gregorian_month = order[m]

        return datetime.date(gregorian_year, gregorian_month, gregorian_date)

    @classmethod
    def to_ethiopian(cls, year, month, date):
        """ Ethiopian date string representation of provided Gregorian date

        Params:
        * year: an int
        * month: an int
        * date: an int """

        # prevent incorect input
        inputs = (year, month, date)
        if 0 in inputs or [data.__class__ for data in inputs].count(int) != 3:
            raise ValueError("Malformed input can't be converted.")

        # date between 5 and 14 of May 1582 are invalid
        if month == 10 and date >= 5 and date <= 14 and year == 1582:
            raise ValueError("Invalid Date between 5-14 May 1582.")

        # Number of days in gregorian months
        # starting with January (index 1)
        # Index 0 is reserved for leap years switches.
        gregorian_months = [0, 31, 28, 31, 30, 31, 30, \
                            31, 31, 30, 31, 30, 31]

        # Number of days in ethiopian months
        # starting with January (index 1)
        # Index 0 is reserved for leap years switches.
        ethiopian_months = [0, 30, 30, 30, 30, 30, 30, 30, \
                            30, 30, 5, 30, 30, 30, 30]

        # if gregorian leap year, February has 29 days.
        if  (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
            gregorian_months[2] = 29

        # September sees 8y difference
        ethiopian_year = year - 8

        # if ethiopian leap year pagumain has 6 days
        if ethiopian_year % 4 == 3:
            ethiopian_months[10] = 6
        else:
            ethiopian_months[10] = 5

        # Ethiopian new year in Gregorian calendar
        new_year_day = cls._start_day_of_ethiopian(year - 8)

        # calculate number of days up to that date
        until = 0
        for i in range(1, month):
            until += gregorian_months[i]
        until += date

        # update tahissas (december) to match january 1st
        if ethiopian_year % 4 == 0:
            tahissas = 26
        else:
            tahissas = 25

        # take into account the 1582 change
        if year < 1582:
            ethiopian_months[1] = 0
            ethiopian_months[2] = tahissas
        elif until <= 277 and year == 1582:
            ethiopian_months[1] = 0
            ethiopian_months[2] = tahissas
        else:
            tahissas = new_year_day - 3
            ethiopian_months[1] = tahissas

        # calculate month and date incremently
        m = 0
        for m in range(1, ethiopian_months.__len__()):
            if until <= ethiopian_months[m]:
                if m == 1 or ethiopian_months[m] == 0:
                    ethiopian_date = until + (30 - tahissas)
                else:
                    ethiopian_date = until
                break
            else:
                until -= ethiopian_months[m]

        # if m > 4, we're already on next Ethiopian year
        if m > 10:
            ethiopian_year += 1

        # Ethiopian months ordered according to Gregorian
        order = [0, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 1, 2, 3, 4]
        ethiopian_month = order[m]

        return ethiopian_year, ethiopian_month, ethiopian_date
