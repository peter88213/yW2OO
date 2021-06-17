"""Install the yW2OO script and set up the registry files
for extending the yWriter context menu. 

Version 3.4.2

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/yW2OO
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import sys
from string import Template

APP = 'yw2oo.pyw'

YW_CONTEXT_MENU = '''Windows Registry Editor Version 5.00

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo]
"MUIVerb"="Export to OpenOffice"
"subcommands"=""

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell]

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\00export]
@="Export to odt"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\00export\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\""

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\01proof]
@="Proof reading"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\01proof\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _proof"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\02manuscript]
@="Manuscript"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\02manuscript\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _manuscript"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\03scenedesc]
@="Scene Descriptions"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\03scenedesc\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _scenes"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\04chapterdesc]
@="Chapter Descriptions"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\04chapterdesc\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _chapters"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\05partdesc]
@="Part Descriptions"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\05partdesc\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _parts"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\06charlist]
@="Character List"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\06charlist\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _charlist"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\07loclist]
@="Location List"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\07loclist\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _loclist"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\08itemlist]
@="Item List"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\08itemlist\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _itemlist"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\10crossreference]
@="Cross references"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\10crossreference\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _xref"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\11chardesc]
@="Character Descriptions"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\11chardesc\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _characters"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\12locdesc]
@="Location Descriptions"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\12locdesc\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _locations"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\13itemdesc]
@="Item Descriptions"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\13itemdesc\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _items"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\14scenelist]
@="Scene List"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\14scenelist\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _scenelist"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\15plotlist]
@="Plot List"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\15plotlist\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _plotlist"

[-HKEY_CURRENT_USER\Software\Classes\yWriter6\shell\yw2oo]
[-HKEY_CURRENT_USER\Software\Classes\yWriter5\shell\yw2oo]
'''

RESET_CONTEXT_MENU = '''Windows Registry Editor Version 5.00

[-HKEY_CURRENT_USER\Software\Classes\yWriter7\shell\yw2oo]
[-HKEY_CURRENT_USER\Software\Classes\yWriter6\shell\yw2oo]
[-HKEY_CURRENT_USER\Software\Classes\yWriter5\shell\yw2oo]
'''


def copy_file(inputFile, outputFile):
    with open(inputFile, 'rb') as f:
        myData = f.read()
    with open(outputFile, 'wb') as f:
        f.write(myData)
    return()


def update_reg(installPath):

    def make_reg(filePath, template, mapping):
        """Create a registry file to extend the yWriter context menu."""

        with open(filePath, 'w', encoding='utf-8') as f:
            f.write(template.safe_substitute(mapping))

        print(os.path.normpath(filePath) + ' written.')

    python = sys.executable.replace('\\', '\\\\')
    script = installPath.replace('/', '\\\\') + '\\\\' + APP
    mapping = dict(PYTHON=python, SCRIPT=script)
    make_reg(installPath + '/add_context_menu.reg',
             Template(YW_CONTEXT_MENU), mapping)
    make_reg(installPath + '/rem_context_menu.reg',
             Template(RESET_CONTEXT_MENU), {})


def run():
    """Install the yW2OO script and extend the yWriter context menu."""
    installPath = os.getenv('APPDATA').replace('\\', '/') + '/yw2oo'

    try:
        with os.scandir(installPath) as files:

            for file in files:
                os.remove(file)

    except:

        try:
            os.mkdir(installPath)
            print(os.path.normpath(installPath) + ' created.')

        except:
            pass

    update_reg(installPath)

    copy_file(APP, installPath + '/' + APP)
    print(os.path.normpath(installPath + '/' + APP) + ' copied.')

    os.startfile(os.path.normpath(installPath))


if __name__ == '__main__':
    run()
