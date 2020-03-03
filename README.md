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

[Download page](https://github.com/peter88213/yW2OO/releases)



## How to install

1. If you have already installed an older version of yW2OO, please run the uninstaller for it. 

2. Unzip `yW2OO_<version number>.zip` within your user profile.

3. Move into the `yW2OO_<version number>` folder and run `Install.bat` (double click).
   This will copy all needed files to the right places. 
   You may be asked for approval to modify  the Windows registry. Please accept in order to
   install an Explorer context menu entry "Export to LibreOffice" for yWriter7 files.

4. __Optional:__  Download and install the [Courier Prime](https://quoteunquoteapps.com/courierprime).



## How to use

1. Write your novel with yWriter7. Backup entire project and close yWriter.

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

