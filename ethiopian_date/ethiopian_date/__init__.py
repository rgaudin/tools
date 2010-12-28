#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

""" Ethiopian Date Converter

Convert from Ethiopian date to Gregorian date (and vice-versa)

Examples:

greg_date = EthiopianDateConverter.to_gregorian(2003, 4, 11)
ethi_date = EthiopianDateConverter.date_to_ethiopian(datetime.date.today())

"""

VERSION = (0, 1, 1)


def get_version():
    version = "%s.%s" % (VERSION[0], VERSION[1])
    if VERSION[2] != 0:
        version = "%s.%s" % (version, VERSION[2])
    return version

__version__ = get_version()

from ethiopian_date import EthiopianDateConverter
