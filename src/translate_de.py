"""Generate German translation files for GNU gettext.

- Update the project's 'de.po' translation file.
- Generate the language specific 'pywriter.mo' dictionary.

Usage: 
translate_de.py

File structure:

├── PyWriter/
│   ├── i18n/
│   │   └── de.json
│   └── src/
│       ├── translations.py
│       └── msgfmt.py
└── <project>/
    ├── src/ 
    │   └── translate_de.py
    └── i18n/
        ├── messages.pot
        ├── de.po
        └── locale/
            └─ de/
               └─ LC_MESSAGES/
                  └─ pywriter.mo
    
Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yW2OO
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import translations
import msgfmt

APP = 'yW2OO'
PO_PATH = '../i18n/de.po'
MO_PATH = '../i18n/locale/de/LC_MESSAGES/pywriter.mo'

if translations.main('de', app=APP):
    print(f'Writing "{MO_PATH}" ...')
    msgfmt.make(PO_PATH, MO_PATH)
