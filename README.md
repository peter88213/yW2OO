# yW2OO - yWriter to LibreOffice converter

Export a novel from [yWriter 7](http://www.spacejock.com/yWriter7.html) to an OpenDocument 
text file.

![Screenshot: Generated ODT in Writer](https://raw.githubusercontent.com/peter88213/yW2OO/master/docs/Screenshots/Writer.png)

For more information see [Wiki (english)](https://github.com/peter88213/yW2OO/wiki)



## Requirements

* Windows.

* yWriter 7.

* A LibreOffice 5 or 6 standard installation (not a "portable" version).



## Download

The yW2OO Software comes as a zipfile `yW2OO_<version number>.zip`. 

[Download page](https://github.com/peter88213/yW2OO/releases/latest)



## How to install

1. If you have already installed an older version of yW2OO, please run the uninstaller for it. 

2. Unzip `yW2OO_<version number>.zip` within your user profile.

3. Move into the `yW2OO_<version number>` folder and run `Install.bat` (double click).
   This will copy all needed files to the right places. 
   You may be asked for approval to modify  the Windows registry. Please accept in order to
   install an Explorer context menu entry "Export to LibreOffice" for yWriter7 files.

4. __Optional:__  Download and install the [Courier Prime](https://quoteunquoteapps.com/courierprime).



## How to use

1. Write your novel with yWriter7. Please consider the following conventions:
   * Text markup: Bold and italics are supported. Other highlighting such as underline and strikethrough are lost.
   * Chapters and scenes marked as "Unused" (U) will not be exported.
   * Chapters marked as "Other" (I) will not be exported.
   * If `This chapter begins a new section` is selected in _Chapter/Details_, the heading will be on the first level. Otherwise, it will be on the second level.
   * If `Suppress chapter title when exporting` is selected in _Chapter/Details_, yW2OO will remove "Chapter" from auto-numbered chapter titles. The numbers will remain.
   * If `Append to previous scene` is selected in _Scene/Exporting_, neither a blank line nor a scene divider will be inserted between the scenes. Otherwise three asterisks will be inserted (style: Heading 4). 

   Backup entire project and close yWriter.

2.  Move into your yWriter project folder, and right-click your .yw7 project file. 
   In the context menu, choose `Export to LibreOffice`. 
   
![Screenshot: Windows Explorer context menu](https://raw.githubusercontent.com/peter88213/yW2OO/master/docs/Screenshots/yw2oo_cm.png)

3. If everything goes well, you find an OpenDocument file named `<your yWriter project>.odt`.
   Double click to open.

4. Fine tune your manuscript typographically with [OOTyW](https://github.com/peter88213/OOTyW/wiki).



## How to uninstall

Move into the `yW2OO_<version number>` folder and run `Uninstall.bat` (double click). 
You may be asked for approval to modify the registry. Please accept to remove the Explorer context
menu entry. 

