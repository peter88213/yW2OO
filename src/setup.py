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

APP = 'yw2oo.pyw'

YW7_CONTEXT_MENU = '''Windows Registry Editor Version 5.00

[HKEY_CLASSES_ROOT\\yWriter7\\shell\\yw2oo]
"MUIVerb"="Export to OpenOffice"
"subcommands"=""

[HKEY_CLASSES_ROOT\\yWriter7\\shell\\yw2oo\\shell]

[HKEY_CLASSES_ROOT\\yWriter7\\shell\\yw2oo\\shell\\00proof]
@="Proof reading"

[HKEY_CLASSES_ROOT\\yWriter7\\shell\\yw2oo\\shell\\00proof\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _proof"

[HKEY_CLASSES_ROOT\\yWriter7\\shell\\yw2oo\\shell\\01manuscript]
@="Manuscript"

[HKEY_CLASSES_ROOT\\yWriter7\\shell\\yw2oo\\shell\\01manuscript\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _manuscript"

[HKEY_CLASSES_ROOT\\yWriter7\\shell\\yw2oo\\shell\\02scenedesc]
@="Scene Descriptions"

[HKEY_CLASSES_ROOT\\yWriter7\\shell\\yw2oo\\shell\\02scenedesc\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _scenes"

[HKEY_CLASSES_ROOT\\yWriter7\\shell\\yw2oo\\shell\\03chapterdesc]
@="Chapter Descriptions"

[HKEY_CLASSES_ROOT\\yWriter7\\shell\\yw2oo\\shell\\03chapterdesc\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _chapters"

[HKEY_CLASSES_ROOT\\yWriter7\\shell\\yw2oo\\shell\\04partdesc]
@="Part Descriptions"

[HKEY_CLASSES_ROOT\\yWriter7\\shell\\yw2oo\\shell\\04partdesc\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _parts"

[HKEY_CLASSES_ROOT\\yWriter7\\shell\\yw2oo\\shell\\05scenelist]
@="Scene List"

[HKEY_CLASSES_ROOT\\yWriter7\\shell\\yw2oo\\shell\\05scenelist\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _scenelist"

[HKEY_CLASSES_ROOT\\yWriter7\\shell\\yw2oo\\shell\\06plotlist]
@="Plot List"

[HKEY_CLASSES_ROOT\\yWriter7\\shell\\yw2oo\\shell\\06plotlist\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _plotlist"

[HKEY_CLASSES_ROOT\\yWriter7\\shell\\yw2oo\\shell\\07chardesc]
@="Character Descriptions"

[HKEY_CLASSES_ROOT\\yWriter7\\shell\\yw2oo\\shell\\07chardesc\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _characters"

[HKEY_CLASSES_ROOT\\yWriter7\\shell\\yw2oo\\shell\\08locdesc]
@="Location Descriptions"

[HKEY_CLASSES_ROOT\\yWriter7\\shell\\yw2oo\\shell\\08locdesc\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _locations"

[HKEY_CLASSES_ROOT\\yWriter7\\shell\\yw2oo\\shell\\09itemdesc]
@="Item Descriptions"

[HKEY_CLASSES_ROOT\\yWriter7\\shell\\yw2oo\\shell\\09itemdesc\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _items"

[HKEY_CLASSES_ROOT\\yWriter7\\shell\\yw2oo\\shell\\10charlist]
@="Character List"

[HKEY_CLASSES_ROOT\\yWriter7\\shell\\yw2oo\\shell\\10charlist\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _charlist"

[HKEY_CLASSES_ROOT\\yWriter7\\shell\\yw2oo\\shell\\11loclist]
@="Location List"

[HKEY_CLASSES_ROOT\\yWriter7\\shell\\yw2oo\\shell\\11loclist\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _loclist"

[HKEY_CLASSES_ROOT\\yWriter7\\shell\\yw2oo\\shell\\12itemlist]
@="Item List"

[HKEY_CLASSES_ROOT\\yWriter7\\shell\\yw2oo\\shell\\12itemlist\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _itemlist"

[HKEY_CLASSES_ROOT\\yWriter7\\shell\\yw2oo\\shell\\13crossreference]
@="Cross references"

[HKEY_CLASSES_ROOT\\yWriter7\\shell\\yw2oo\\shell\\13crossreference\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _xref"

[HKEY_CLASSES_ROOT\\yWriter7\\shell\\yw2oo\\shell\\14export]
@="Export to odt"

[HKEY_CLASSES_ROOT\\yWriter7\\shell\\yw2oo\\shell\\14export\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\""
'''

YW6_CONTEXT_MENU = '''Windows Registry Editor Version 5.00

[HKEY_CLASSES_ROOT\\yWriter6\\shell\\yw2oo]
"MUIVerb"="Export to OpenOffice"
"subcommands"=""

[HKEY_CLASSES_ROOT\\yWriter6\\shell\\yw2oo\\shell]

[HKEY_CLASSES_ROOT\\yWriter6\\shell\\yw2oo\\shell\\00proof]
@="Proof reading"

[HKEY_CLASSES_ROOT\\yWriter6\\shell\\yw2oo\\shell\\00proof\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _proof"

[HKEY_CLASSES_ROOT\\yWriter6\\shell\\yw2oo\\shell\\01manuscript]
@="Manuscript"

[HKEY_CLASSES_ROOT\\yWriter6\\shell\\yw2oo\\shell\\01manuscript\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _manuscript"

[HKEY_CLASSES_ROOT\\yWriter6\\shell\\yw2oo\\shell\\02scenedesc]
@="Scene Descriptions"

[HKEY_CLASSES_ROOT\\yWriter6\\shell\\yw2oo\\shell\\02scenedesc\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _scenes"

[HKEY_CLASSES_ROOT\\yWriter6\\shell\\yw2oo\\shell\\03chapterdesc]
@="Chapter Descriptions"

[HKEY_CLASSES_ROOT\\yWriter6\\shell\\yw2oo\\shell\\03chapterdesc\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _chapters"

[HKEY_CLASSES_ROOT\\yWriter6\\shell\\yw2oo\\shell\\04partdesc]
@="Part Descriptions"

[HKEY_CLASSES_ROOT\\yWriter6\\shell\\yw2oo\\shell\\04partdesc\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _parts"

[HKEY_CLASSES_ROOT\\yWriter6\\shell\\yw2oo\\shell\\05scenelist]
@="Scene List"

[HKEY_CLASSES_ROOT\\yWriter6\\shell\\yw2oo\\shell\\05scenelist\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _scenelist"

[HKEY_CLASSES_ROOT\\yWriter6\\shell\\yw2oo\\shell\\06plotlist]
@="Plot List"

[HKEY_CLASSES_ROOT\\yWriter6\\shell\\yw2oo\\shell\\06plotlist\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _plotlist"

[HKEY_CLASSES_ROOT\\yWriter6\\shell\\yw2oo\\shell\\07chardesc]
@="Character Descriptions"

[HKEY_CLASSES_ROOT\\yWriter6\\shell\\yw2oo\\shell\\07chardesc\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _characters"

[HKEY_CLASSES_ROOT\\yWriter6\\shell\\yw2oo\\shell\\08locdesc]
@="Location Descriptions"

[HKEY_CLASSES_ROOT\\yWriter6\\shell\\yw2oo\\shell\\08locdesc\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _locations"

[HKEY_CLASSES_ROOT\\yWriter6\\shell\\yw2oo\\shell\\09itemdesc]
@="Item Descriptions"

[HKEY_CLASSES_ROOT\\yWriter6\\shell\\yw2oo\\shell\\09itemdesc\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _items"

[HKEY_CLASSES_ROOT\\yWriter6\\shell\\yw2oo\\shell\\10charlist]
@="Character List"

[HKEY_CLASSES_ROOT\\yWriter6\\shell\\yw2oo\\shell\\10charlist\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _charlist"

[HKEY_CLASSES_ROOT\\yWriter6\\shell\\yw2oo\\shell\\11loclist]
@="Location List"

[HKEY_CLASSES_ROOT\\yWriter6\\shell\\yw2oo\\shell\\11loclist\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _loclist"

[HKEY_CLASSES_ROOT\\yWriter6\\shell\\yw2oo\\shell\\13crossreference]
@="Cross references"

[HKEY_CLASSES_ROOT\\yWriter6\\shell\\yw2oo\\shell\\13crossreference\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _xref"

[HKEY_CLASSES_ROOT\\yWriter6\\shell\\yw2oo\\shell\\14export]
@="Export to odt"

[HKEY_CLASSES_ROOT\\yWriter6\\shell\\yw2oo\\shell\\14export\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\""
'''

YW5_CONTEXT_MENU = '''Windows Registry Editor Version 5.00

[HKEY_CLASSES_ROOT\\yWriter5\\shell\\yw2oo]
"MUIVerb"="Export to OpenOffice"
"subcommands"=""

[HKEY_CLASSES_ROOT\\yWriter5\\shell\\yw2oo\\shell]

[HKEY_CLASSES_ROOT\\yWriter5\\shell\\yw2oo\\shell\\02scenedesc]
@="Scene Descriptions"

[HKEY_CLASSES_ROOT\\yWriter5\\shell\\yw2oo\\shell\\02scenedesc\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _scenes"

[HKEY_CLASSES_ROOT\\yWriter5\\shell\\yw2oo\\shell\\03chapterdesc]
@="Chapter Descriptions"

[HKEY_CLASSES_ROOT\\yWriter5\\shell\\yw2oo\\shell\\03chapterdesc\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _chapters"

[HKEY_CLASSES_ROOT\\yWriter5\\shell\\yw2oo\\shell\\04partdesc]
@="Part Descriptions"

[HKEY_CLASSES_ROOT\\yWriter5\\shell\\yw2oo\\shell\\04partdesc\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _parts"

[HKEY_CLASSES_ROOT\\yWriter5\\shell\\yw2oo\\shell\\05scenelist]
@="Scene List"

[HKEY_CLASSES_ROOT\\yWriter5\\shell\\yw2oo\\shell\\05scenelist\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _scenelist"

[HKEY_CLASSES_ROOT\\yWriter5\\shell\\yw2oo\\shell\\06plotlist]
@="Plot List"

[HKEY_CLASSES_ROOT\\yWriter5\\shell\\yw2oo\\shell\\06plotlist\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _plotlist"

[HKEY_CLASSES_ROOT\\yWriter5\\shell\\yw2oo\\shell\\07charlist]
@="Character List"

[HKEY_CLASSES_ROOT\\yWriter5\\shell\\yw2oo\\shell\\07charlist\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _charlist"

[HKEY_CLASSES_ROOT\\yWriter5\\shell\\yw2oo\\shell\\08loclist]
@="Location List"

[HKEY_CLASSES_ROOT\\yWriter5\\shell\\yw2oo\\shell\\08loclist\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _loclist"

[HKEY_CLASSES_ROOT\\yWriter5\\shell\\yw2oo\\shell\\09itemlist]
@="Item List"

[HKEY_CLASSES_ROOT\\yWriter5\\shell\\yw2oo\\shell\\09itemlist\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _itemlist"

[HKEY_CLASSES_ROOT\\yWriter5\\shell\\yw2oo\\shell\\10crossreference]
@="Cross references"

[HKEY_CLASSES_ROOT\\yWriter5\\shell\\yw2oo\\shell\\10crossreference\\command]
@="\\"${PYTHON}\\" \\"${SCRIPT}\\" \\"%1\\" _xref"
'''

RESET_CONTEXT_MENU = '''Windows Registry Editor Version 5.00

[-HKEY_CLASSES_ROOT\yWriter7\shell\yw2oo]
[-HKEY_CLASSES_ROOT\yWriter6\shell\yw2oo]
[-HKEY_CLASSES_ROOT\yWriter5\shell\yw2oo]
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
    make_reg(installPath + '/add_cm7.reg', Template(YW7_CONTEXT_MENU), mapping)
    make_reg(installPath + '/add_cm6.reg', Template(YW6_CONTEXT_MENU), mapping)
    make_reg(installPath + '/add_cm5.reg', Template(YW5_CONTEXT_MENU), mapping)
    make_reg(installPath + '/del_cm.reg', Template(RESET_CONTEXT_MENU), {})


def run():
    """Install the yW2OO script and extend the yWriter context menu."""
    installPath = os.getenv('APPDATA').replace('\\', '/') + '/yw2oo'

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
