[Project homepage](https://peter88213.github.io/yW2OO)

------------------------------------------------------------------

yWriter to OpenOffice/LibreOffice converter - yWriter export to odt/ods documents. 

# Instructions for use

## How to install yW2OO

1. If you have already installed an older version of yW2OO, please run the uninstaller for it. 

2. Unzip `yW2OO_<version number>.zip` within your user profile.

3. Move into the `yW2OO_<version number>` folder and run `setup.pyw` (double click).
   This will copy all needed files to the right places. 
   
4. Open the installation folder. You may wish to create a shortcut to *yw2oo.pyw* on your Desktop.

5. Under Windows, you can add am Explorer context menu by double-clicking  `add_context_menu.reg`. 
   You may be asked for approval to modify  the Windows registry. Please accept.

You can remove the context menu entries by double-clicking  `rem_context_menu.reg`.

Please note that these context menus depend on the currently installed Python version. 
After a major Python update you may need to run the setup program again and renew the registry entries.

## How to use yW2OO

#### Using the graphical user interface

The included installation script prompts you to create a shortcut on the desktop. 

1. Start the program via the desktop shortcut icon. On startup, the last opened yWriter project 
   is loaded, if any. Otherwise, a "file open" dialog is displayed. Optionally, you can drag your yWriter 
   project and drop it on the shortcut icon. 
   
2. If the loaded file is not the project you want to export from, open another project via the 
   **File > Open** command (or *Ctrl-O* shortcut). 
   
3. Via the main menu, choose the export document type. This will start the export.

4. If everything goes well, a success message pops up. The newly created file is located 
   in the same folder as your yWriter project. If you want to edit your new document immediately, 
   just click on the `open` button. 

#### Using the Explorer context menu

1. Move into your yWriter project folder, and right-click your .yw7 project file. 
   In the context menu, choose `Export to OpenOffice`. 
   
2. A sub menu with export document types will open. Select the desired one.

3. If everything goes well, a success message pops up. The newly created file is located 
   in the same folder as your yWriter project. If you want to edit your new document immediately, 
   just click on the `open` button. 


## How to uninstall yW2OO

Move into the installation folder `~\.yw2oo` and double click on `rem_context_menu.reg`. 
You may be asked for approval to modify the registry. Please accept to remove the Explorer context
menu entry. 


------------------------------------------------------------------------


## Command reference

See the [command reference page](help.md)


------------------------------------------------------------------------


## Installation path

The setup script installs *yw2oo.pyw* in the user profile. This is the installation path on Windows: 

`c:\Users\<user name>\.pywriter\yw2oo`