"""Convert yWriter project to odt or ods. 

Version @release
Requires Python 3.6+
Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/yW2OO
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys

from pywriter.ui.ui_tk import UiTk
from pywriter.converter.yw7_exporter import Yw7Exporter


class Exporter(Yw7Exporter):
    """Extend the Super class. 
    Show 'Open' button after conversion from yw.
    """

    def export_from_yw(self, source, target):
        """Extend the super class method, showing an 'open' button after conversion."""
        Yw7Exporter.export_from_yw(self, source, target)

        if self.newFile:
            self.ui._show_open_button(self._open_newFile)


def run(sourcePath, suffix=None):
    converter = Exporter()
    converter.ui = UiTk('Export from yWriter @release')
    kwargs = {'suffix': suffix}
    converter.run(sourcePath, **kwargs)
    converter.ui.start()


if __name__ == '__main__':

    try:
        sourcePath = sys.argv[1]

    except:
        sourcePath = ''

    try:
        suffix = sys.argv[2]

    except:
        suffix = ''

    run(sourcePath, suffix)
