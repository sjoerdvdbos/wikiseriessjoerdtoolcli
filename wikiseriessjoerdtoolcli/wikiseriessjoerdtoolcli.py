#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: wikiseriessjoerdtoolcli.py
#
# Copyright 2023 Sjoerd van den Bos
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
#

"""
Main code for wikiseriessjoerdtoolcli.

.. _Google Python Style Guide:
   https://google.github.io/styleguide/pyguide.html

"""

import logging
import logging.config
import json
import argparse
import coloredlogs
from pathlib import Path
import wikiseriessjoerdlib


__author__ = '''Sjoerd van den Bos <test@example.com>'''
__docformat__ = '''google'''
__date__ = '''01-05-2023'''
__copyright__ = '''Copyright 2023, Sjoerd van den Bos'''
__credits__ = ["Sjoerd van den Bos"]
__license__ = '''MIT'''
__maintainer__ = '''Sjoerd van den Bos'''
__email__ = '''<test@example.com>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".


# This is the main prefix used for logging
LOGGER_BASENAME = '''wikiseriessjoerdtoolcli'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())


def get_arguments():
    """
    Gets us the cli arguments.

    Returns the args as parsed from the argsparser.
    """
    # https://docs.python.org/3/library/argparse.html
    parser = argparse.ArgumentParser(description='''A cli tool to use wikipedia to retrieve tv series information''')
    parser.add_argument('--log-config',
                        '-l',
                        action='store',
                        dest='logger_config',
                        help='The location of the logging config json file',
                        default='')
    parser.add_argument('--log-level',
                        '-L',
                        help='Provide the log level. Defaults to info.',
                        dest='log_level',
                        action='store',
                        default='info',
                        choices=['debug',
                                 'info',
                                 'warning',
                                 'error',
                                 'critical'])

    # examples: /Users/sjoerd.van.den.bos/tmp/wikiseriessjoerd
    parser.add_argument('--name', '-n',
                        help='Name of the series to retrieve.',
                        type=str,
                        required=True)
    parser.add_argument('--path', '-p',
                        help='Path to save the series data. This can be relative.',
                        default='.',
                        type=str,
                        required=False)
    args = parser.parse_args()
    return args


def setup_logging(level, config_file=None):
    """
    Sets up the logging.

    Needs the args to get the log level supplied

    Args:
        level: At which level do we log
        config_file: Configuration to use

    """
    # This will configure the logging, if the user has set a config file.
    # If there's no config file, logging will default to stdout.
    if config_file:
        # Get the config for the logger. Of course this needs exception
        # catching in case the file is not there and everything. Proper IO
        # handling is not shown here.
        try:
            with open(config_file, encoding="utf-8") as conf_file:
                configuration = json.loads(conf_file.read())
                # Configure the logger
                logging.config.dictConfig(configuration)
        except ValueError:
            print(f'File "{config_file}" is not valid json, cannot continue.')
            raise SystemExit(1) from None
    else:
        coloredlogs.install(level=level.upper())


def main():
    """
    Main method.

    This method holds what you want to execute when
    the script is run on command line.
    """
    args = get_arguments()
    setup_logging(args.log_level, args.logger_config)
    # Main code goes here
    series = wikiseriessjoerdlib.search_series(args.name)
    path = f'{args.path}/{args.name}'
    Path(f'{path}').mkdir(exist_ok=True)
    for season in series:
        Path(f'{path}/{season}').mkdir(exist_ok=True)
        for number, episode in enumerate(series[season], 1):
            Path(f'{path}/{season}/Episode {number}.txt').write_text(f'Title: "{episode}"', encoding="utf-8")


if __name__ == '__main__':
    main()
