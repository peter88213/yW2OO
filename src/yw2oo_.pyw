"""Convert yWriter project to odt or ods. 

Version @release

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import sys
from urllib.parse import unquote

from yw2oolib.exporter import Exporter

YW_EXTENSIONS = ['.yw7', '.yw6', '.yw5']


def run(sourcePath, suffix=None):
    converter = Exporter()
    kwargs = {'suffix': suffix}
    converter.run(sourcePath, **kwargs)
    converter.ui.start()


if __name__ == '__main__':

    try:
        sourcePath = unquote(sys.argv[1].replace('file:///', ''))

    except:
        sourcePath = ''

    fileName, FileExtension = os.path.splitext(sourcePath)

    if not FileExtension in YW_EXTENSIONS:
        # Source file is not a yWriter project.
        suffix = None

    else:
        # Source file is a yWriter project; suffix matters.

        try:
            suffix = sys.argv[2]

        except:
            suffix = ''

    run(sourcePath, suffix)
