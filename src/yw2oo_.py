#!/usr/bin/python3
"""Convert yWriter project to or from odt or ods. 

Version @release
Requires Python 3.6+
Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/yW2OO
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import sys
from pathlib import Path
from pywriter.pywriter_globals import *
from pywriter.ui.set_icon_tk import *
from pywriter.config.configuration import Configuration
from yw2oolib.yw2oo_tk import Yw2ooTk

APPNAME = 'yw2oo'
SETTINGS = dict(
    yw_last_open='',
    root_geometry='600x140',
)
OPTIONS = {}
FILE_TYPES = [
    (_('Convertible file'), '.yw7'),
    (_('Convertible file'), '.odt'),
    (_('Convertible file'), '.ods'),
]


def main():
    #--- Set up the directories for configuration and temporary files.
    try:
        homeDir = str(Path.home()).replace('\\', '/')
        installDir = f'{homeDir}/.pywriter/{APPNAME}/config'
    except:
        installDir = '.'
    os.makedirs(installDir, exist_ok=True)
    try:
        sourcePath = sys.argv[1]
    except:
        sourcePath = ''
    try:
        suffix = sys.argv[2]
    except:
        suffix = None

    #--- Load configuration.
    iniFile = f'{installDir}/{APPNAME}.ini'
    configuration = Configuration(SETTINGS, OPTIONS)
    configuration.read(iniFile)
    kwargs = dict(file_types=FILE_TYPES,)
    kwargs.update(configuration.settings)
    kwargs.update(configuration.options)

    #--- Instantiate the converter object.
    ui = Yw2ooTk(f'{APPNAME} @release', **kwargs)

    #--- Get initial project path.
    __, extension = os.path.splitext(sourcePath)
    if not sourcePath:
        sourcePath = kwargs['yw_last_open']
        suffix = None
    ui.open_project(sourcePath)
    if suffix:
        if suffix == 'x':
            # Cmdline argument "x" is a placeholder for "plain" export.
            suffix = ''
        kwargs['suffix'] = suffix
        ui.converter.run(sourcePath, **kwargs)
        # Exits if converted document is opened.
    else:
        if extension in ('.odt', '.ods'):
            ui.converter.run(sourcePath, **kwargs)
            # Exits if converted document is opened.
    ui.start()

    #--- Save project specific configuration
    for keyword in ui.kwargs:
        if keyword in configuration.options:
            configuration.options[keyword] = ui.kwargs[keyword]
        elif keyword in configuration.settings:
            configuration.settings[keyword] = ui.kwargs[keyword]
    configuration.write(iniFile)


if __name__ == '__main__':
    main()
