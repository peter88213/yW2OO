#!/usr/bin/python3
"""Install the yW2OO script and set up the registry files
for extending the yWriter context menu. 

Version @release

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/yW2OO
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys
import os
import stat
from shutil import copyfile
from shutil import copytree
from shutil import rmtree
from pathlib import Path
from string import Template
import gettext
import locale
import platform
try:
    from tkinter import *
except ModuleNotFoundError:
    print('The tkinter module is missing. Please install the tk support package for your python3 version.')
    sys.exit(1)

# Initialize localization.
LOCALE_PATH = f'{os.path.dirname(sys.argv[0])}/locale/'
try:
    CURRENT_LANGUAGE = locale.getlocale()[0][:2]
except:
    # Fallback for old Windows versions.
    CURRENT_LANGUAGE = locale.getdefaultlocale()[0][:2]
try:
    t = gettext.translation('reg', LOCALE_PATH, languages=[CURRENT_LANGUAGE])
    _ = t.gettext
except:

    def _(message):
        return message

APPNAME = 'yw2oo'
VERSION = ' @release'
APP = f'{APPNAME}.py'
START_UP_SCRIPT = 'run.pyw'
INI_FILE = f'{APPNAME}.ini'
INI_PATH = '/config/'
SAMPLE_PATH = 'sample/'
SUCCESS_MESSAGE = '''

$Appname is installed here:

$Apppath'''

SHORTCUT_MESSAGE = '''
Now you might want to create a shortcut on your desktop.  

On Windows, open the installation folder, hold down the Alt key on your keyboard, 
and then drag and drop run.pyw to your desktop.

On Linux, create a launcher on your desktop. With xfce for instance, the launcher's command may look like this:
python3 '$Apppath' %F
'''

APP = 'yw2oo.py'

START_UP_CODE = f'''import {APPNAME}
{APPNAME}.main()
'''

SET_CONTEXT_MENU = f'''Windows Registry Editor Version 5.00

[-HKEY_CURRENT_USER\Software\Classes\yWriter7\shell\yw2oo]
[-HKEY_CURRENT_USER\Software\Classes\yWriter6\shell\yw2oo]
[-HKEY_CURRENT_USER\Software\Classes\yWriter5\shell\yw2oo]

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo]
"MUIVerb"="{_('Export to OpenOffice')}"
"subcommands"=""

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell]

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\000export]
@="{_('Manuscript without tags (export only)')}"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\000export\\command]
@="\\"$PYTHON\\" \\"$SCRIPT\\" \\"%1\\" x"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\010proof]
@="{_('Manuscript with visible tags for proof reading')}"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\010proof\\command]
@="\\"$PYTHON\\" \\"$SCRIPT\\" \\"%1\\" _proof"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\020manuscript]
@="{_('Manuscript for editing')}"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\020manuscript\\command]
@="\\"$PYTHON\\" \\"$SCRIPT\\" \\"%1\\" _manuscript"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\040scenedesc]
@="{_('Scene descriptions for editing')}"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\040scenedesc\\command]
@="\\"$PYTHON\\" \\"$SCRIPT\\" \\"%1\\" _scenes"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\050chapterdesc]
@="{_('Chapter descriptions for editing')}"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\050chapterdesc\\command]
@="\\"$PYTHON\\" \\"$SCRIPT\\" \\"%1\\" _chapters"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\060partdesc]
@="{_('Part descriptions for editing')}"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\060partdesc\\command]
@="\\"$PYTHON\\" \\"$SCRIPT\\" \\"%1\\" _parts"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\200more]
@="{_('More')}..."

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\200more\\command]
@="\\"$PYTHON\\" \\"$SCRIPT\\" \\"%1\\""

'''

'''
[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\030brfsynopsis]
@="{_('Brief synopsis (export only)')}"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\030brfsynopsis\\command]
@="\\"$PYTHON\\" \\"$SCRIPT\\" \\"%1\\" _brf_synopsis"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\070chardesc]
@="{_('Character descriptions for editing')}"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\070chardesc\\command]
@="\\"$PYTHON\\" \\"$SCRIPT\\" \\"%1\\" _characters"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\080locdesc]
@="{_('Location descriptions for editing')}"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\080locdesc\\command]
@="\\"$PYTHON\\" \\"$SCRIPT\\" \\"%1\\" _locations"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\090itemdesc]
@="{_('Item descriptions for editing')}"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\090itemdesc\\command]
@="\\"$PYTHON\\" \\"$SCRIPT\\" \\"%1\\" _items"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\100scenelist]
@="{_('Scene list (spreadsheet)')}"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\100scenelist\\command]
@="\\"$PYTHON\\" \\"$SCRIPT\\" \\"%1\\" _scenelist"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\110charlist]
@="{_('Character list (spreadsheet)')}"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\110charlist\\command]
@="\\"$PYTHON\\" \\"$SCRIPT\\" \\"%1\\" _charlist"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\120loclist]
@="{_('Location list (spreadsheet)')}"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\120loclist\\command]
@="\\"$PYTHON\\" \\"$SCRIPT\\" \\"%1\\" _loclist"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\130itemlist]
@="{_('Item list (spreadsheet)')}"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\130itemlist\\command]
@="\\"$PYTHON\\" \\"$SCRIPT\\" \\"%1\\" _itemlist"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\150notes]
@="{_('Notes chapters for editing')}"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\150notes\\command]
@="\\"$PYTHON\\" \\"$SCRIPT\\" \\"%1\\" _notes"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\160todo]
@="{_('Todo chapters for editing')}"

[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\yw2oo\\shell\\160todo\\command]
@="\\"$PYTHON\\" \\"$SCRIPT\\" \\"%1\\" _todo"

'''

RESET_CONTEXT_MENU = '''Windows Registry Editor Version 5.00

[-HKEY_CURRENT_USER\Software\Classes\yWriter7\shell\yw2oo]
[-HKEY_CURRENT_USER\Software\Classes\yWriter6\shell\yw2oo]
[-HKEY_CURRENT_USER\Software\Classes\yWriter5\shell\yw2oo]
'''

root = Tk()
processInfo = Label(root, text='')
message = []


def output(text):
    message.append(text)
    processInfo.config(text=('\n').join(message))


def make_context_menu(installPath):
    """Generate ".reg" files to extend the yWriter context menu."""

    def save_reg_file(filePath, template, mapping):
        """Save a registry file."""
        with open(filePath, 'w') as f:
            f.write(template.safe_substitute(mapping))
        output(f'Creating "{os.path.normpath(filePath)}"')

    python = sys.executable.replace('\\', '\\\\')
    instPath = installPath.replace('/', '\\\\')
    script = f'{instPath}\\\\{START_UP_SCRIPT}'
    mapping = dict(PYTHON=python, SCRIPT=script)
    save_reg_file(f'{installPath}/add_context_menu.reg', Template(SET_CONTEXT_MENU), mapping)
    save_reg_file(f'{installPath}/rem_context_menu.reg', Template(RESET_CONTEXT_MENU), {})


def open_folder(installDir):
    """Open an installation folder window in the file manager.
    """
    try:
        os.startfile(os.path.normpath(installDir))
        # Windows
    except:
        try:
            os.system('xdg-open "%s"' % os.path.normpath(installDir))
            # Linux
        except:
            try:
                os.system('open "%s"' % os.path.normpath(installDir))
                # Mac
            except:
                pass


def install(pywriterPath):
    """Install the script."""

    # Create a general PyWriter installation directory, if necessary.
    os.makedirs(pywriterPath, exist_ok=True)
    installDir = f'{pywriterPath}{APPNAME}'
    cnfDir = f'{installDir}{INI_PATH}'
    if os.path.isfile(f'{installDir}/{APP}'):
        simpleUpdate = True
    else:
        simpleUpdate = False
    try:
        # Move an existing installation to the new place, if necessary.
        oldHome = os.getenv('APPDATA').replace('\\', '/')
        oldInstDir = f'{oldHome}/pyWriter/{APPNAME}'
        os.replace(oldInstDir, installDir)
        output(f'Moving "{oldInstDir}" to "{installDir}"')
    except:
        pass
    os.makedirs(cnfDir, exist_ok=True)

    # Delete the old version, but retain configuration, if any.
    rmtree(f'{installDir}/locale', ignore_errors=True)
    rmtree(f'{installDir}/icons', ignore_errors=True)
    rmtree(f'{installDir}/help', ignore_errors=True)
    with os.scandir(installDir) as files:
        for file in files:
            if not 'config' in file.name:
                try:
                    os.remove(file)
                    output(f'Removing "{file.name}"')
                except:
                    pass

    # Install the new version.
    copyfile(APP, f'{installDir}/{APP}')
    output(f'Copying "{APP}"')

    # Install the help files.
    copytree('help', f'{installDir}', dirs_exist_ok=True)
    output(f'Copying "help"')

    # Install the localization files.
    copytree('locale', f'{installDir}/locale', dirs_exist_ok=True)
    output(f'Copying "locale"')

    # Install the icon files.
    copytree('icons', f'{installDir}/icons', dirs_exist_ok=True)
    output(f'Copying "icons"')

    # Make the script executable under Linux.
    st = os.stat(f'{installDir}/{APP}')
    os.chmod(f'{installDir}/{APP}', st.st_mode | stat.S_IEXEC)

    # Install configuration files, if needed.
    try:
        with os.scandir(SAMPLE_PATH) as files:
            for file in files:
                if not os.path.isfile(f'{cnfDir}{file.name}'):
                    copyfile(f'{SAMPLE_PATH}{file.name}', f'{cnfDir}{file.name}')
                    output(f'Copying "{file.name}"')
                else:
                    output(f'Keeping "{file.name}"')
    except:
        pass

    # Generate registry entries for the context menu (Windows only).
    if os.name == 'nt':
        make_context_menu(installDir)

    # Display a success message.
    mapping = {'Appname': APPNAME, 'Apppath': f'{installDir}/{APP}'}
    output(Template(SUCCESS_MESSAGE).safe_substitute(mapping))

    #--- Create a start-up script.
    if platform.system() == 'Windows':
        shebang = ''
    else:
        shebang = '#!/usr/bin/python3\n'
    with open(f'{installDir}/{START_UP_SCRIPT}', 'w', encoding='utf-8') as f:
        f.write(f'{shebang}{START_UP_CODE}')

    # Ask for shortcut creation.
    if not simpleUpdate:
        output(Template(SHORTCUT_MESSAGE).safe_substitute(mapping))


if __name__ == '__main__':
    scriptPath = os.path.abspath(sys.argv[0])
    scriptDir = os.path.dirname(scriptPath)
    os.chdir(scriptDir)

    # Open a tk window.
    root.geometry("800x600")
    root.title(f'Install {APPNAME}{VERSION}')
    header = Label(root, text='')
    header.pack(padx=5, pady=5)

    # Prepare the messaging area.
    processInfo.pack(padx=5, pady=5)

    # Run the installation.
    homePath = str(Path.home()).replace('\\', '/')
    pywriterPath = f'{homePath}/.pywriter/'
    try:
        install(pywriterPath)
    except Exception as ex:
        output(str(ex))

    # Show options: open installation folders or quit.
    root.openButton = Button(text="Open installation folder", command=lambda: open_folder(f'{homePath}/.pywriter/{APPNAME}'))
    root.openButton.config(height=1, width=30)
    root.openButton.pack(padx=5, pady=5)
    root.quitButton = Button(text="Quit", command=quit)
    root.quitButton.config(height=1, width=30)
    root.quitButton.pack(padx=5, pady=5)
    root.mainloop()
