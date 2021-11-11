"""Install the yW2OO script and set up the registry files
for extending the yWriter context menu. 

Version @release

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/yW2OO
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import sys
from string import Template
from shutil import copyfile

APP = 'yw2oo.pyw'

YW_CONTEXT_MENU = '''Windows Registry Editor Version 5.00

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo]
"MUIVerb"="Export to OpenOffice"
"subcommands"=""

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell]

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\000export]
@="Export to odt"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\000export\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\""

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\010brfsynopsis]
@="Brief Synopsis"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\010brfsynopsis\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _brf_synopsis"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\020proof]
@="Proof reading"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\020proof\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _proof"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\030manuscript]
@="Manuscript"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\030manuscript\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _manuscript"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\040scenedesc]
@="Scene Descriptions"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\040scenedesc\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _scenes"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\050chapterdesc]
@="Chapter Descriptions"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\050chapterdesc\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _chapters"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\060partdesc]
@="Part Descriptions"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\060partdesc\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _parts"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\070charlist]
@="Character List"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\070charlist\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _charlist"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\080loclist]
@="Location List"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\080loclist\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _loclist"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\090itemlist]
@="Item List"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\090itemlist\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _itemlist"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\100crossreference]
@="Cross references"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\100crossreference\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _xref"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\110chardesc]
@="Character Descriptions"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\110chardesc\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _characters"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\120locdesc]
@="Location Descriptions"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\120locdesc\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _locations"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\130itemdesc]
@="Item Descriptions"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\130itemdesc\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _items"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\140scenelist]
@="Scene List"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\140scenelist\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _scenelist"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\150plotlist]
@="Plot List"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\150plotlist\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _plotlist"

[-HKEY_CURRENT_USER\Software\Classes\yWriter6\shell\yw2oo]
[-HKEY_CURRENT_USER\Software\Classes\yWriter5\shell\yw2oo]
'''

RESET_CONTEXT_MENU = '''Windows Registry Editor Version 5.00

[-HKEY_CURRENT_USER\Software\Classes\yWriter7\shell\yw2oo]
[-HKEY_CURRENT_USER\Software\Classes\yWriter6\shell\yw2oo]
[-HKEY_CURRENT_USER\Software\Classes\yWriter5\shell\yw2oo]
'''


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
    installPath = os.getenv('APPDATA').replace('\\', '/') + '/PyWriter/yw2oo'

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

    copyfile(APP, installPath + '/' + APP)
    print(os.path.normpath(installPath + '/' + APP) + ' copied.')

    os.startfile(os.path.normpath(installPath))


if __name__ == '__main__':
    run()
