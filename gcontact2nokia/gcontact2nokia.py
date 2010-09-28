#!/usr/bin/env python
# encoding=utf-8

''' Generates Gammu-formatted backup file from Google Contact CSV file

    Takes a CSV file (Google CSV format) as input and generates a
    plain text file for use with gammu.

    Examples:
    gcontact2nokia.py google.csv gammu.bck && gammu restore gammu.bck -yes

    This script has _only_ been tested with my Nokia 1680 but should work
    with any gammu-compatible phone.

    LICENSE: WTF Public License. '''


import sys
import pprint
from datetime import datetime


class NokiaEntry(object):

    TEMPLATE = u"Entry%(num)sType = %(type)s\n" \
                "Entry%(num)sText = \"%(value)s\"\n"

    def __init__(self, key=None, value=None, position=None, *args, **kwargs):
        self.key = key
        self.value = value
        self.position = position

    def get_position(self):
        return str(self.position).zfill(2)

    def to_s(self, position=None):
        try:
            return self.TEMPLATE % {'num': self.get_position(), \
                                'type': self.key, \
                                'value': self.value}
        except:
            print self.key
            print self.value
            raise


class NokiaContact(object):

    _entries = []

    TEMPLATE = "[PhonePBK%(num)s]\n" \
               "Location = %(num)s\n" \
               "%(entries)s\n"

    def __init__(self, position=None, *args, **kwargs):

        self._entries = []
        self.position = position

        cptr = 0
        for key, value in kwargs.items():
            if value:
                entry = NokiaEntry(key=key, value=value, position=cptr)
                cptr = cptr + 1
                self._entries.append(entry)

    def get_position(self):
        return str(self.position).zfill(3)

    def to_s(self):
        return self.TEMPLATE % {'num': self.get_position(), \
                                'entries': self.entries()}

    def entries(self):
        out = u""
        for entry in self._entries:
            out += entry.to_s()
        return out


class NokiaBook(object):

    TEMPLATE = u"[Backup]\n" \
                "IMEI = \"%(imei)s\"\n" \
                "Phone = \"%(phone)s\"\n" \
                "Creator = \"%(creator)s\"\n" \
                "DateTime = %(date)s\n" \
                "Format = %(format)s\n\n" \
                "%(contacts)s"

    imei = '0000000000'
    phone = 'Nokia Unknown'
    creator = 'gcontact2nokia.py'
    date = datetime.now().strftime("%Y%m%dT%H%M%SZ")

    _contacts = []

    def __init__(self, *args, **kwargs):
        self._contacts = []

    def add(self, contact):
        self._contacts.append(contact)

    def to_s(self):
        return self.TEMPLATE % {'imei': self.imei, 'phone': self.phone, \
                  'creator': self.creator, 'date': self.date, \
                  'format': u"1.04", 'contacts': self.contacts()}

    def contacts(self):
        out = u""
        for contact in self._contacts:
            out += contact.to_s()
        return out


def str_decode(str_):
    encodings = ('utf-8', 'iso-8859-1')
    for enc in encodings:

        try:
            str_ = str_.decode(enc)
            return str_
        except UnicodeDecodeError:
            pass


def cleanup(str_):
    try:
        return str_.strip().title()
    except AttributeError:
        return str_


def usage():
    print "Usage: %s source.csv destination.bck\n" % sys.argv[0]


def main():

    # default settings
    GAMMU_IMEI = '356782027329625'
    GAMMU_PHONE = 'Nokia 1680 05.61'

    try:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    except IndexError:
        usage()
        exit(1)

    # create phone book
    book = NokiaBook()
    book.imei = GAMMU_IMEI
    book.phone = GAMMU_PHONE

    # open CSV file.
    print "Opening %s file as Google CSV data." % input_file
    inf = open(input_file, "r")

    # setup contact counter
    cptr = 0

    # loop on CSV file lines
    for line in inf:

        # skip first line (header)
        if cptr == 0:
            cptr = 1
            continue

        # entries holds the valueable data
        entries = {}

        # split CSV line
        data = line.replace('"', '').split(',')

        # retrieve, clean up and store each wanted field.
        for key, index in (('FirstName', 1), ('LastName', 3), \
                           ('NumberGeneral', 36), ('NumberWork', 38)):
            try:
                fdata = data[index]
            except IndexError:
                fdata = None

            if fdata:
                fdata = str_decode(fdata)

            fdata = cleanup(fdata)
            entries[key] = fdata

        # skype contacts without phone number
        if not entries['NumberGeneral'] \
           or entries['NumberGeneral'].__len__() <= 1:
            continue

        # pretty print retrieved infos
        # pprint.pprint(entries)

        # create the contact with a position number.
        contact = NokiaContact(position=cptr, **entries)

        # increment contact counter
        cptr = cptr + 1

        # add contact to phonebook
        book.add(contact)

    print "Book created: %d contacts" % book._contacts.__len__()

    # write phone book dump into destination file.
    outf = open(output_file, "w")
    outf.write(book.to_s().encode('utf-8'))

if __name__ == '__main__':
    main()
