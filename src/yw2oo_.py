"""yW2OO - Export ywriter7 scenes to odt. 

Depends on the PyWriter library v1.5

Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/yW2OO
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os

from pywriter.odt.odt_file import OdtFile
from pywriter.yw7.yw7_file import Yw7File


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

    if sourcePath is None:
        return 'ERROR: No yWriter 7 project found.'

    print('Export yWriter7 scenes content to odt')
    print('Project: "' + sourcePath + '"')
    yw7File = Yw7File(sourcePath)

    if yw7File.is_locked():
        return 'ERROR: yWriter 7 seems to be open. Please close first.'

    message = yw7File.read()

    if message.startswith('ERROR'):
        return message

    document = OdtFile(sourcePath.split('.yw7')[0] + SUFFIX + '.odt')
    document.comments = True
    message = document.write(yw7File)
    return message


if __name__ == '__main__':
    message = main()
    print(message)
