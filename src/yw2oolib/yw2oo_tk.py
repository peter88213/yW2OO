""""Provide a tkinter GUI framework for yWriter odf export.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yW2OO
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import tkinter as tk
from tkinter import messagebox
import webbrowser

from pywriter.pywriter_globals import *
from pywriter.file.doc_open import open_document
from pywriter.ui.main_tk import MainTk
from pywriter.ui.set_icon_tk import *
from yw2oolib.yw2oo_exporter import Yw2ooExporter

HELPFILE = f'{os.path.dirname(sys.argv[0])}/help.html'


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
    _KEY_HELP = ('<F1>', 'F1')

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
        set_icon(self.root, icon='yLogo32')
        self.exporter = Yw2ooExporter()
        self.exporter.ui = self

        self._openButton = tk.Button(self.mainWindow, text=_('Open exported document'), state=tk.DISABLED, command=self._open_newFile)
        self._openButton.config(height=1)
        self._openButton.pack(pady=10)
        self.quitButton = tk.Button(self.mainWindow, text=_("Quit"), command=self.on_quit)
        self.quitButton.config(height=1, width=10)
        self.quitButton.pack(pady=10)
        self.disable_menu()
        self.root.bind(self._KEY_HELP[0], self.show_help)

    def _build_main_menu(self):
        """Add main menu entries.
        
        Extends the superclass template method. 
        """
        super()._build_main_menu()

        # Export
        self.exportMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Export'), menu=self.exportMenu)
        self.exportMenu.add_command(label=_('Manuscript without tags (export only)'), command=lambda: self._export_document(''))
        self.exportMenu.add_command(label=_('Brief synopsis (export only)'), command=lambda: self._export_document('_brf_synopsis'))
        self.exportMenu.add_command(label=_('Cross references (export only)'), command=lambda: self._export_document('_xref'))
        self.exportMenu.add_separator()
        self.exportMenu.add_command(label=_('Manuscript for editing'), command=lambda: self._export_document('_manuscript'))
        self.exportMenu.add_command(label=_('Notes chapters for editing'), command=lambda: self._export_document('_notes'))
        self.exportMenu.add_command(label=_('Todo chapters for editing'), command=lambda: self._export_document('_todo'))
        self.exportMenu.add_separator()
        self.exportMenu.add_command(label=_('Manuscript with visible tags for proof reading'), command=lambda: self._export_document('_proof'))

        # Descriptions
        self.descMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Descriptions'), menu=self.descMenu)
        self.descMenu.add_command(label=_('Part descriptions for editing'), command=lambda: self._export_document('_parts'))
        self.descMenu.add_command(label=_('Chapter descriptions for editing'), command=lambda: self._export_document('_chapters'))
        self.descMenu.add_command(label=_('Scene descriptions for editing'), command=lambda: self._export_document('_scenes'))
        self.descMenu.add_command(label=_('Character descriptions for editing'), command=lambda: self._export_document('_characters'))
        self.descMenu.add_command(label=_('Location descriptions for editing'), command=lambda: self._export_document('_locations'))
        self.descMenu.add_command(label=_('Item descriptions for editing'), command=lambda: self._export_document('_items'))

        # Lists
        self.listMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Lists'), menu=self.listMenu)
        self.listMenu.add_command(label=_('Scene list (spreadsheet)'), command=lambda: self._export_document('_scenelist'))
        self.listMenu.add_command(label=_('Character list (spreadsheet)'), command=lambda: self._export_document('_charlist'))
        self.listMenu.add_command(label=_('Location list (spreadsheet)'), command=lambda: self._export_document('_loclist'))
        self.listMenu.add_command(label=_('Item list (spreadsheet)'), command=lambda: self._export_document('_itemlist'))

        # Help
        self.mainMenu.add_command(label=_('Help'), command=self.show_help)

    def disable_menu(self):
        """Disable menu entries when no project is open.
        
        Extends the superclass method.      
        """
        super().disable_menu()
        self.mainMenu.entryconfig(_('Export'), state='disabled')
        self.mainMenu.entryconfig(_('Descriptions'), state='disabled')
        self.mainMenu.entryconfig(_('Lists'), state='disabled')
        self.hide_open_button()

    def enable_menu(self):
        """Enable menu entries when a project is open.
        
        Extends the superclass method.
        """
        super().enable_menu()
        self.mainMenu.entryconfig(_('Export'), state='normal')
        self.mainMenu.entryconfig(_('Descriptions'), state='normal')
        self.mainMenu.entryconfig(_('Lists'), state='normal')

    def _export_document(self, suffix):
        self.kwargs['suffix'] = suffix
        self.exporter.run(self.prjFile.filePath, **self.kwargs)

    def show_open_button(self, open_cmd=None):
        self._openButton['state'] = tk.NORMAL

    def hide_open_button(self):
        self._openButton['state'] = tk.DISABLED

    def _open_newFile(self):
        """Open the converted file for editing and exit the program."""
        open_document(self.exporter.newFile)
        self.on_quit()

    def show_help(self, event=None):
        if os.path.isfile(HELPFILE):
            webbrowser.open(HELPFILE)
        else:
            messagebox.showerror(self.title, _('Help file not found. Please check the installation'))
