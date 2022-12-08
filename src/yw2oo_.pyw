#!/usr/bin/python3
"""Convert yWriter project to odt or ods. 

Version @release
Requires Python 3.6+
Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yW2OO
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import sys
from pathlib import Path
from pywriter.pywriter_globals import *
from pywriter.ui.set_icon_tk import *
from pywriter.config.configuration import Configuration
from pywriter.ui.ui_tk import UiTk
from yw2oolib.yw2oo_exporter import Yw2ooExporter
from yw2oolib.yw2oo_tk import Yw2ooTk

APPNAME = 'yw2oo'
SETTINGS = dict(
    yw_last_open='',
    root_geometry='600x140',
)
OPTIONS = {}


def run(sourcePath='', suffix=None, installDir='.'):

    #--- Load configuration.
    iniFile = f'{installDir}/{APPNAME}.ini'
    configuration = Configuration(SETTINGS, OPTIONS)
    configuration.read(iniFile)
    kwargs = {}
    kwargs.update(configuration.settings)
    kwargs.update(configuration.options)

    #--- Get initial project path.
    if not sourcePath or not os.path.isfile(sourcePath):
        sourcePath = kwargs['yw_last_open']

    #--- Instantiate the exporter object.
    ui = Yw2ooTk(f'{APPNAME} @release', **kwargs)
    ui.open_project(sourcePath)

    if suffix:
        # Output document type is set, so run the converter immediately.
        if suffix == 'x':
            suffix = ''
        kwargs = {'suffix': suffix}
        ui.exporter.run(sourcePath, **kwargs)

    ui.start()

    #--- Save project specific configuration
    for keyword in ui.kwargs:
        if keyword in configuration.options:
            configuration.options[keyword] = ui.kwargs[keyword]
        elif keyword in configuration.settings:
            configuration.settings[keyword] = ui.kwargs[keyword]
    configuration.write(iniFile)


if __name__ == '__main__':

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
    run(sourcePath, suffix, installDir)
