#!/usr/bin/env python3

"""

Python program to print out CoVid 19 data for the United States

"""

import inspy_logger as logger

from lib import PROG_NAME
from argparse import ArgumentParser
import os
from pathlib import Path
from configparser import ConfigParser
from conf import run

from lib.api import fetch_data

parser = ArgumentParser('covid_info',
                        prefix_chars='+-',
                        add_help=True,
                        allow_abbrev=True, )

parser.add_argument('+v', '--verbose',
                    action='store_true',
                    required=False,
                    help='The program will output verbosely.',
                    dest='verbose')

parser.add_argument('+gui', action='store_true', required=False,
                    help='Starts covid_tracker in graphical user interface mode',
                    dest='gui')

parser = parser.parse_args()

conf_path = Path(os.path.abspath('conf/'))

conf_file = Path(os.path.abspath('conf/settings.ini'))

log = logger.start(PROG_NAME, parser.verbose)

if conf_path.exists():
    if conf_file.exists():
        if parser.gui:
            config = ConfigParser()
            config.read('conf/settings.ini')
            run.config = config
            if 'GUI' in config:
                print(config['GUI']['theme'])
                app_theme = config['GUI']['theme']

        loaded_settings = True
    else:
        loaded_settings = False
else:
    print('false')

if parser.gui:
    print('')
    from lib.gui.models.windows.main import MainWindow
    MainWindow()
else:
    fetch_data()

