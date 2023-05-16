[Project home page](index) > Changelog

------------------------------------------------------------------------

## Changelog

### v5.1.0

- Provide translations for scene related comments in the exported documents. 

Based on PyWriter v12.7.1

### v5.0.9

- When creating a new scene on ODT import, localize the default title.
- Change the German wording according to novelyst: "Szene" --> "Abschnitt". 

Based on PyWriter v12.4.1

### v5.0.8

- Show a message when scenes are split during conversion.

Based on PyWriter v12.4.0

### v5.0.7

- Make it work on virtual file systems.

Based on PyWriter v12.3.2

### v5.0.6

- Also convert .odt and .ods on start if specified by cmdline argument.

Based on PyWriter v12.3.0

### v5.0.5

- When a document is loaded, disable "Descriptions" and "Lists" menus.

Based on PyWriter v12.3.0

### v5.0.4

- Make sure that no conversion is run on start if an invalid source path is set as commandline argument.

Based on PyWriter v12.3.0

### v5.0.3

- Fix a bug where the "Open converted file" button is deactivated after conversion on start.

Based on PyWriter v12.3.0

### v5.0.2

- Reduce the memory use by discarding the docstrings on building.

Based on PyWriter v12.1.2

### v5.0.1

- Improve error handling.

Based on PyWriter v12.1.1

### v5.0.0 Major feature update

IMPORTANT: 
- If you have a desktop shortcut to start yW2OO, please change the target from "yw2oo.pyw" to "run.pyw".
- If you use the Windows Explorer context menu entry, please re-run the registry scripts after setup.

Changes
- Provide reverse conversion of ODT/ODS to yWriter.
- Use a start up script ( *run.pyw* ) to speed up execution.
- Replace the built in help with online help.

Based on PyWriter v12.1.0

### v4.4.3

- Make it run on old Windows versions.

Based on PyWriter v10.0.1

### v4.4.2

- Modify "shebang" lines to make the scripts run with Python 3.11 under Windows.

Based on PyWriter v9.0.5

### v4.4.1 Bugfix

- Fix a regression from v4.3.1 where wrong language markers are imported
from the "proofread" document.

Based on PyWriter v9.0.5

### v4.4.0

- Code optimization and library update. 

Based on PyWriter v9.0.4

### v4.3.3

- Fix a bug where no error message is not displayed, if no help text is available.

Based on PyWriter v8.0.9

### v4.3.2

- Library upgrade.
- Assign "no language" to the chapter/scene markers for the  proof reading document.
- When converting to ODT format, apply all XML predefined entities.
- Fix a bug where attempting to save a write-protected file raises an
uncaught exception.

Based on PyWriter v8.0.8

### v4.2.4

- Fix a bug in odt manuscript export, where the "Quotation" style is not applied at scene start.

Based on PyWriter v7.14.1

### v4.2.3

- Undo the change from v4.1.3: Change the German wording (Abschnitt --> Szene).

Based on PyWriter v7.12.2

### v4.2.2

- Read the document language and country codes from project variables, if any.

Based on PyWriter v7.12.2

### v4.2.1

Introduce a notation for assigning text passages to another language/country. This is mainly for spell checking in Office Writer.

Based on PyWriter v7.11.2

### v4.1.4 

- When importing from yWriter, paragraphs that start with "> " are formatted as "Quotations".

Based on PyWriter v7.10.3

### v4.1.3 

- Change the German wording: Szene --> Abschnitt.
- Process the document's language and country (if any) when exporting ODF.
- Support "no document language" settings.

Based on PyWriter v7.10.2

### v4.0.2 

- Fix help file.
- Show a pop-up message if the helpfile is missing.

Based on PyWriter v7.4.1

### v4.0.1 

- Exit program after opening the exported document.

Based on PyWriter v7.4.1

### v4.0.0 

- New user interface.
- New document type for "ToDo" chapters.
- Add internationalization according to GNU coding standards.
- Provide German localization.
- Consider project names containing a reserved suffix.

Based on PyWriter v7.4.1

### v3.16.3 Update setup script

- Change the working dir to the script dir on startup in order to avoid "file not found" error.

Based on PyWriter v5.18.0

### v3.16.2 Improved setup

- Catch exceptions in the setup script.

Based on PyWriter v5.18.0

### v3.16.1 Bugfix release

OdtExport:
- Fix quotations at scene start.
- Fix and refactor inline code removal.

Based on PyWriter v5.16.1

### v3.16.0 

- OdtExport: When exporting chapters and scenes to odt, set style of paragraphs that start with "> " to "Quotations".

Based on PyWriter v5.16.0

### v3.14.0 

When exporting chapters and scenes to odt,
- ignore scenes beginning with `<HTML>` or `<TEX>`,
- remove inline raw code.

Based on PyWriter v5.14.0

### v3.12.5 Improved word counting

- Fix word counting considering ellipses.

Based on PyWriter v5.12.4

### v3.12.4 Improved word counting

- Fix word counting considering comments, hyphens, and dashes.

Based on PyWriter v5.12.3

### v3.12.3 Optional update

PyWriter library update.

Based on PyWriter v5.12.2

### v3.12.2 Optional update

Provide the "Quotations" paragraph style.

Based on PyWriter v5.4.2

### v3.12.1 Optional update

Improve non-Windows compatibility.

Based on PyWriter v5.2.2

### v3.12.0

- Add document type: Notes scenes.
- Remove document type: Plot list.

When installing this version, please update the Explorer context menu.

Based on PyWriter v5.2.0

### v3.10.2 Optional update

- Clean up ODF templates to make the code and generated documents more compact.

Based on PyWriter v5.0.3

### v3.10.1 Optional update

- Improve code and documentation quality.

Based on PyWriter v5.0.2

### v3.10.0

- Fix a bug where "To do" chapters cause an exception.
- Rework the user interface. 
- Refactor the code.

Based on PyWriter v5.0.0

### v3.8.6 Update text formatting

When creating odt files, make paragraphs after blank lines "Text body" without indent.

Based on PyWriter v3.32.2

### v3.8.5 Create backup when overwriting

- Create registry files on setup only under Windows.
- Create backups when overwriting files.

Based on PyWriter v3.30.0

### v3.8.4 Bugfix release

- Fix a bug in the PyWriter library where brief synopses cannot be opened with LibreOffice 7.

Based on PyWriter v3.28.2

### v3.8.3 Change the order in the context menu

- Move "Brief Synopsis" below "Proof reading".

Based on PyWriter v3.28.1

### v3.8.2 Optional update for Linux compatibility

- Add shebang and change the line endings for Linux.
- Change the installation path to make it compatible with non-Windows OS.

After update, please remove the old version at `~\AppData\Roaming\yw2oo` manually.

Based on PyWriter v3.28.1

### v3.8.1 Bugfix update

- Fix a bug in the setup script where setup is aborted when the "PyWriter" directory does not exist in the user profile.

Based on PyWriter v3.28.1

### v3.8.0 Feature update

- Add a brief synopsis with chapter and scene titles.

Based on PyWriter v3.28.0

### v3.6.0 Feature update

- Add notes to the character descriptions.

Based on PyWriter v3.22.0

### v3.4.6 Bugfix release

This release is strongly recommended.
Fix a regression from PyWriter v3.12.5. causing a crash if a scene has an 
hour, but no minute set.

Based on PyWriter v3.16.4

### v3.4.5 Standardize the installation path

- Move the installation path to the AppData\Roaming\PyWriter subfolder, 
where all PyWriter-based applications are to be located.

Based on PyWriter v3.12.7

### v3.4.4 Optional update

Refactor: 
- Remove overhead from the main function.
- Move the Exporter class to the main script. 

Based on PyWriter v3.12.5

### v3.4.3 Optional update

- Major refactoring of the template based export.

Based on PyWriter v3.12.5

### v3.4.2 Optional update

- Major refactoring of the yw7 file processing.

Based on PyWriter v3.8.0

### v3.4.1 Bugfix update

- Fix the "proofread tags" paragraph styles.

Based on PyWriter v3.6.6

### v3.4.0 New document formatting, general program improvement

It is highly advised to update to this version.

- Imported *Scenes/chapters* and *manuscript* documents now have three-line 
"* * *" scene dividers instead of single blank lines.
- *Replace scene dividers with blank lines* is added to the **Format** menu.
- Scene titles as comments at the beginning of the scenes in the *manuscript* 
and *work in progress* documents are written back to yWriter.
- Chapter titles in the *manuscript*, *scene descriptions*, *part descriptions*,
and *chapter descriptions* documents are written back to yWriter.
- Generate temporary files in the user's temp folder.

Based on PyWriter v3.6.5

### v3.2.2 Optional update

- Modify plot list titles.

Based on PyWriter v3.4.2

### v3.2.1 Bugfix update

- Cope better with the chapter/scene type overdetermination since yWriter 7.0.7.2.

Based on PyWriter v3.4.1

### v3.2.0 Drop yWriter 6 support

Support only yWriter 7 projects for better maintainability and speed.

Based on PyWriter v3.4.0

### v3.0.2 Optional update

- Refactor for faster execution.

Based on Pywriter v3.2.1

### v3.0.1 Optional update
Refactor, based on PyWriter v3.2.0

### v3.0.0 Complete revision

Stand-alone universal exporter, based on PyWriter v3.0.0

### v1.16.0
- Add an AddOn menu to the extension for manual conversion.

### v1.15.1
- If `Auto_Descriptions.txt` exists, the project title is transferred to the ODT metadata.
- After preprocessing, the `Exported Project.html` code contains css attributes instead of improperly used heading tags.
- Exception handlers secure the OO/LO extension against improper use . 

### v1.14.0-b
- Update provided documentation.
- After preprocessing, the Exported Project.html code is well-formed and can be imported into any html processing application other than Open/LibreOffice. Previous versions of oo2yw just "hacked" Exported Project.html in an ugly way and relied on Open/LibreOffice's tolerance against bad html coding.

### v1.14.0
- Periods are no longer added to the chapter titles.
- StandardPages template is to be installed separately, so there is no more need for localized packages.
- Includes _Courier Prime_ font used by the template (optional).
- writer.bat is automatically copied to all yWriter projects on installation.
- writer.bat is automatically removed from all yWriter projects on de-installation.
- writer.bat supports yWriter7 behavior of scene descriptions export.
- New setup directory structure.

### v1.13.0
- Preprocessor _yW2OO.py_ v1.6.0 processes empty scene dividers generated by yWriter6.

### v1.12.0
- Optional scene title comments are marked _Scene descriptions_.
- _"Standard pages"_ template modified for nicer display of scene titles.

### v1.11.0
- Numbered scene titles can be added to the document as annotations. 

### v1.10.0
- Scene titles can be added to the document as comments. 

### v1.9.0
- Simplify and fix document conversion.

### v1.8.1
- Add LibreOffice 6.x support.
- Add README file for optional batch tool.
- Add german paperback model document to en-us zipfile.

### v1.8.0
- The _StandardPages_ styles are loaded without associating the template with the converted document. 

### v1.7.0
- Now, the OpenOffice extension (OXT) is language independent. 
- Only installation and de-installation scripts and document templates are language specific. 

### v1.6.0
- Add a description and a version number to OXT macro extension (important for future updates).
- Remove some unused macro subroutines. 
- Add a search/replace command for a LibreOffice (de) specific style name.

### v1.5.0
- The localized document template is now loaded automatically.
- The Templates included are optimized (Scenes will show up in navigator). 

### v1.4.1
- LibreOffice 5 support.

### v1.4.0
- Working for __yWriter6__ export as well. 
- Processing all types of HTML scene dividers.

### v1.3.0
- On install, localization is no longer auto-detected. Now there are separate downloads for each language. 

### v1.2.0
- Fully automated installation and de-installation,
- Localized (en-US and de-DE) OO document templates.

### v1.1.0

- Same function as the first release.
- Distribution now via zipfile (no binary executable).
- Add an uninstaller.
- Strip README files. There is a link to the GitHub Wiki for better maintainability.

### v1.0.0 
- First public release