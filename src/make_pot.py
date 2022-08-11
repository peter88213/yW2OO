"""Generate a template file (pot) for message translation.

For further information see https://github.com/peter88213/yW2OO
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import sys
from build_yw2oo import main
from build_yw2oo import TARGET_FILE
import pgettext

APP = 'yW2OO'
POT_FILE = '../i18n/messages.pot'


def make_pot():
    # Generate a complete script.
    main()

    # Generate a pot file from the script.
    if os.path.isfile(POT_FILE):
        os.replace(POT_FILE, f'{POT_FILE}.bak')
        backedUp = True
    else:
        backedUp = False
    try:
        pot = pgettext.PotFile(POT_FILE, app=APP)
        pot.scan_file(TARGET_FILE)
        print(f'Writing "{pot.filePath}"...\n')
        pot.write_pot()
        return True

    except:
        if backedUp:
            os.replace(f'{POT_FILE}.bak', POT_FILE)
        print('WARNING: Cannot write pot file.')
        return False


if __name__ == '__main__':
    if not make_pot():
        sys.exit(1)
