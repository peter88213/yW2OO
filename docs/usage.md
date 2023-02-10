[Project homepage](https://peter88213.github.io/yW2OO)

------------------------------------------------------------------

yWriter to OpenOffice/LibreOffice converter - yWriter export to odt/ods documents. 

# Instructions for use

## How to install yW2OO

1. If you have already installed an older version of yW2OO, please run the uninstaller for it. 

2. Unzip `yW2OO_<version number>.zip` within your user profile.

3. Move into the `yW2OO_<version number>` folder and run `setup.pyw` (double click).
   This will copy all needed files to the right places. 
   
4. Open the installation folder. You may wish to create a shortcut to *run.pyw* on your Desktop.

5. Under Windows, you can add am Explorer context menu by double-clicking  `add_context_menu.reg`. 
   You may be asked for approval to modify  the Windows registry. Please accept.

You can remove the context menu entries by double-clicking  `rem_context_menu.reg`.

Please note that these context menus depend on the currently installed Python version. 
After a major Python update you may need to run the setup program again and renew the registry entries.

## How to use yW2OO

#### Drag and drop

You can drag a document or yWriter project and drop it on the shortcut icon to instantly convert the file.
After the conversion, the craphical user interface pops up, showing a message, and providing a button
to open the converted file.


#### Using the graphical user interface

The included installation script prompts you to create a shortcut on the desktop. 

1. Start the program via the desktop shortcut icon. On startup, the last opened yWriter project 
   is loaded, if any. Otherwise, a "file open" dialog is displayed. Optionally, you can drag your yWriter 
   project and drop it on the shortcut icon. 
   
2. If the loaded file is not the project you want to export from, open another project via the 
   **File > Open** command (or *Ctrl-O* shortcut). 
   
3. Via the main menu, choose the export document type (see command reference below). This will start the export.

4. If everything goes well, a success message pops up. The newly created file is located 
   in the same folder as your yWriter project. If you want to edit your new document immediately, 
   just click on the **open converted file** button. 

#### Using the Explorer context menu

For the time being, this works only with *.yw7* files.

1. Move into your yWriter project folder, and right-click your .yw7 project file. 
   In the context menu, choose **Export to OpenOffice**. 
   
2. A sub menu with export document types will open. Select the desired one.

3. If everything goes well, a success message pops up. The newly created file is located 
   in the same folder as your yWriter project. If you want to edit your new document immediately, 
   just click on the **open converted file** button. 


--- 

# Online help

You can open this page with **Help > Online help**.

## Command reference

- **[File menu](https://peter88213.github.io/yW2OO/help/file_menu)**
- **[Swap](https://peter88213.github.io/yW2OO/help/swap_menu)**
- **[Export menu](https://peter88213.github.io/yW2OO/help/export_menu)**
- **[Import](https://peter88213.github.io/yW2OO/help/import_menu)**
- **[Descriptions menu](https://peter88213.github.io/yW2OO/help/descriptions_menu)**
- **[Lists menu](https://peter88213.github.io/yW2OO/help/Lists_menu)**

--- 

# Basic concepts

## Formatting text

It is assumed that very few types of text markup are needed for a novel text:

- *Emphasized* (usually shown as italics).
- *Strongly emphasized* (usually shown as capitalized).
- *Citation* (paragraph visually distinguished from body text).

When exporting to ODT format, *yW2OO* replaces these formattings as follows: 

- Text with `[i]Italic markup[/i]` is formatted as *Emphasized*.
- Text with `[b]Bold markup[/b]` is formatted as *Strongly emphasized*. 
- Paragraphs starting with `> ` are formatted as *Quote*.

---

## How to uninstall yW2OO

1. Move into the installation folder `~\.yw2oo` (see below) and double click on `rem_context_menu.reg`. 
You may be asked for approval to modify the registry. Please accept to remove the Explorer context
menu entry.
2. Move one folder up, and delete the `yw2oo` folder. 



## Installation path

The setup script installs *yw2oo.pyw* in the user profile. This is the installation path on Windows: 

`c:\Users\<user name>\.pywriter\yw2oo`