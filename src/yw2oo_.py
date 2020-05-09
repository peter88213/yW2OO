"""yW2OO - Export yWriter scenes to odt. 

Depends on the PyWriter library v1.6

Copyright (c) 2020, peter88213
For further information see https://github.com/peter88213/yW2OO
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os

from pywriter.odt.odt_file import OdtFile
from pywriter.yw.yw_file import YwFile


SUFFIX = ''
# File name suffix for the exported odt file.
# Example:
# foo.yw7 --> foo_exp.odt


def main():
    sourcePath = None

    files = os.listdir('.')

    for file in files:

        if file.endswith('.yw7'):
            sourcePath = file
            break

    if not sourcePath:

        for file in files:

            if file.endswith('.yw6'):
                sourcePath = file
                break

    if sourcePath is None:
        return 'ERROR: No yWriter project found.'

    print('Export yWriter scenes content to odt')
    print('Project: "' + sourcePath + '"')
    ywFile = YwFile(sourcePath)

    if ywFile.is_locked():
        return 'ERROR: yWriter seems to be open. Please close first.'

    message = ywFile.read()

    if message.startswith('ERROR'):
        return message

    fileName, FileExtension = os.path.splitext(sourcePath)
    document = OdtFile(fileName + SUFFIX + '.odt')
    document.comments = True
    message = document.write(ywFile)
    return message


if __name__ == '__main__':
    message = main()
    print(message)
