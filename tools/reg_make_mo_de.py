"""Generate a German translation file for GNU gettext.

This script is for the Windows Explorer context menu
as specified by the ".reg" file to generate. 

- Generate the language specific 'reg.mo' dictionary.

Usage: 
reg_make_mo_de.py

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import sys
sys.path.insert(0, f'{os.getcwd()}/../../PyWriter/src')
import msgfmt

PO_PATH = '../i18n/reg_de.po'
MO_PATH = '../i18n/locale/de/LC_MESSAGES/reg.mo'


def main():
    msgfmt.make(PO_PATH, MO_PATH)


if __name__ == '__main__':
    main()
