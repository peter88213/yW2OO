"""Provide a converter class for universal export from a yWriter project. 

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/yw2oo
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.converter.universal_exporter import UniversalExporter
from pywriter.ui.ui_tk import UiTk


class Exporter(UniversalExporter):
    """Extend the Super class. 
    Show 'Open' button after conversion from yw.
    """

    def __init__(self):
        """Extend the super class method."""
        UniversalExporter.__init__(self)
        self.ui = UiTk('Export from yWriter')

    def export_from_yw(self, sourceFile, targetFile):
        """Extend the super class method."""
        UniversalExporter.export_from_yw(self, sourceFile, targetFile)

        if self.newFile:
            self.ui.show_open_button(self.open_newFile)
