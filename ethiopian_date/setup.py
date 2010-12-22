#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import setuptools

setuptools.setup(
    name='ethiopian_date',
    version=__import__('ethiopian_date').__version__,
    license='GNU General Public License (GPL), Version 3',

    provides=['ethiopian_date'],

    description='Ethiopian date converter.',
    long_description=open('README.rst').read(),

    url='http://github.com/rgaudin/tools',

    packages=['ethiopian_date'],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or '
        'Lesser General Public License (LGPL)',
        'Programming Language :: Python',
    ],
)
