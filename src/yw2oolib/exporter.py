"""Provide a converter class for universal export from a yWriter project. 

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/yw2oo
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.converter.yw7_exporter import Yw7Exporter
from pywriter.ui.ui_tk import UiTk


class Exporter(Yw7Exporter):
    """Extend the Super class. 
    Show 'Open' button after conversion from yw.
    """

    def __init__(self):
        """Extend the super class method, changing the ui strategy."""
        Yw7Exporter.__init__(self)
        self.ui = UiTk('Export from yWriter')

    def export_from_yw(self, sourceFile, targetFile):
        """Extend the super class method, showing an 'open' buton after conversion."""
        Yw7Exporter.export_from_yw(self, sourceFile, targetFile)

        if self.newFile:
            self.ui.show_open_button(self.open_newFile)
