"""Provide a yWriter to ODF converter.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yW2OO
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.converter.yw7_exporter import Yw7Exporter


class Yw2ooExporter(Yw7Exporter):
    """A converter for universal export from a yWriter 7 project.

    Public methods:
        export_from_yw(sourceFile, targetFile) -- Convert from yWriter project to other file format.

    Shows the 'Open' button after conversion from yw.
    """

    def export_from_yw(self, source, target):
        """Convert from yWriter project to other file format.

        Positional arguments:
            source -- YwFile subclass instance.
            target -- Any Novel subclass instance.
        
        Extends the super class method, showing an 'open' button after conversion.
        """
        Yw7Exporter.export_from_yw(self, source, target)
        if self.newFile:
            self.ui._show_open_button(self._open_newFile)
