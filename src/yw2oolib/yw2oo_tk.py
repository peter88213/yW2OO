""""Provide a tkinter GUI framework for yWriter odf export.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yw-viewer
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import tkinter as tk

from pywriter.pywriter_globals import *
from pywriter.file.doc_open import open_document
from pywriter.ui.main_tk import MainTk
from yw2oolib.yw2oo_exporter import Yw2ooExporter


class Yw2ooTk(MainTk):
    """A tkinter GUI class for yWriter odf export.
    
    Public methods:
        disable_menu() -- disable menu entries when no project is open.
        enable_menu() -- enable menu entries when a project is open.
        open_project(fileName) -- create a yWriter project instance and read the file. 
        close_project() -- close the yWriter project without saving and reset the user interface.

    Public instance variables:
        treeWindow -- tk window for the project tree.

    Show titles, descriptions, and contents in a text box.
    """

    def __init__(self, title, **kwargs):
        """Organize the GUI main window.
        
        Positional arguments:
            title -- application title to be displayed at the window frame.
         
        Required keyword arguments:
            yw_last_open -- str: initial file.
        
        Extends the superclass constructor.
        """
        self.kwargs = kwargs
        super().__init__(title, **kwargs)
        self._exporter = Yw2ooExporter()
        self._exporter.ui = self

    def _build_main_menu(self):
        """Add main menu entries.
        
        Extends the superclass template method. 
        """
        super()._build_main_menu()
        self._exportMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Export'), menu=self._exportMenu)
        self.mainMenu.entryconfig(_('Export'), state='disabled')
        self._exportMenu.add_command(label=_('Export to odt'),
                                        command=lambda: self._export_document(''))
        self._exportMenu.add_command(label=_('Brief synopsis'),
                                        command=lambda: self._export_document('_brf_synopsis'))
        self._exportMenu.add_command(label=_('Scene descriptions'),
                                       command=lambda: self._export_document('_scenes'))
        self._exportMenu.add_command(label=_('Chapter descriptions'),
                                        command=lambda: self._export_document('_chapters'))
        self._exportMenu.add_command(label=_('Part descriptions'),
                                       command=lambda: self._export_document('_parts'))
        self._exportMenu.add_command(label=_('Character descriptions'),
                                        command=lambda: self._export_document('_characters'))
        self._exportMenu.add_command(label=_('Location descriptions'),
                                        command=lambda: self._export_document('_locations'))
        self._exportMenu.add_command(label=_('Item descriptions'),
                                        command=lambda: self._export_document('_items'))
        self.root._openButton = tk.Button(text=_('Open exported document'), state=tk.DISABLED, command=self._open_newFile)
        self.root._openButton.config(height=1)
        self.root._openButton.pack(pady=10)
        self.root.quitButton = tk.Button(text=_("Quit"), command=self.on_quit)
        self.root.quitButton.config(height=1, width=10)
        self.root.quitButton.pack(pady=10)

    def disable_menu(self):
        """Disable menu entries when no project is open.
        
        Extends the superclass method.      
        """
        super().disable_menu()
        self.mainMenu.entryconfig(_('Export'), state='disabled')
        self.hide_open_button()

    def enable_menu(self):
        """Enable menu entries when a project is open.
        
        Extends the superclass method.
        """
        super().enable_menu()
        self.mainMenu.entryconfig(_('Export'), state='normal')

    def _export_document(self, suffix):
        self.kwargs['suffix'] = suffix
        self._exporter.run(self.ywPrj.filePath, **self.kwargs)

    def show_open_button(self, open_cmd=None):
        self.root._openButton['state'] = tk.NORMAL

    def hide_open_button(self):
        self.root._openButton['state'] = tk.DISABLED

    def _open_newFile(self):
        """Open the converted file for editing and exit the converter script."""
        open_document(self._exporter.newFile)
