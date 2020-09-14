# Please note: 

This project will not be continued. Users are advised to uninstall yW2OO and switch to one of the following projects: 

## For LibreOffice users: 

The yw-cnv extension for LibreOffice: Import and export yWriter 6/7 projects. 

https://github.com/peter88213/yw-cnv

## For OpenOffice users: 

The pywoo tools for OpenOffice: Import and export yWriter 6/7 projects with Python. 

https://github.com/peter88213/pywoo


# yW2OO (yWriter to OpenOffice/LibreOffice converter)

Convert [yWriter](http://www.spacejock.com/yWriter5.html)'s HTML export file into a neat OpenDocument text file, ready to apply templates and styles.

![Screenshot: Generated ODT in OpenOffice Writer](https://raw.githubusercontent.com/peter88213/yW2OO/master/docs/Screenshots/Writer.png)


## Download

The yW2OO Software comes as a zipfile `yW2OO_<version number>.zip`. 

[Download page](https://github.com/peter88213/yW2OO/releases)

## How to install

1. Unzip `yW2OO_<version number>.zip` within your user profile.

2. Move into the `yW2OO_<version number>` folder and run `Install.bat` (double click). This will copy all needed files to the right place and install the Office extension.

3. __Optional:__ Open the `yW2OO_<version number>\template\StandardPages_<required paper size>` folder, and run `Install.bat` (double click) to install the provided Standard Manuscript Pages template. 

4. __Optional:__ Open the `yW2OO_<version number>\fonts>` folder, and unzip `CourierPrime.zip`. Install the `.ttf` files (right click -> Install).


## How to use

1. Write your novel in yWriter. Make sure, the `<your yWriter project>\Export` folder contains a file named `writer.bat`. If not, copy it from `yW2OO_<version number>\setup>` folder.

2. __Optional:__ Let yWriter export your scene descriptions to the default location, if you want the scene titles as navigable comments inserted. Command: __Project > Export Project > Scene descriptions__

3. Let yWriter export your project to `<your yWriter project>\Export\Exported Project.html`. Command: __Project > Export Project > to html__.

4. You may close the web browser window showing `Exported Project.html`.

5. Move into the `<your yWriter project>\Export` folder and run `writer.bat` (double click). If everything goes well, OpenOffice/LibreOffice Writer will start automatically and show your document as a OpenDocument file named `Exported Project.odt` with a hierarchical structure and with the right styles applied.

6. Fine tune your manuscript typographically with [OOTyW](https://github.com/peter88213/OOTyW/wiki).

## How to uninstall

Move into the `yW2OO_<version number>` folder and run `Uninstall.bat` (double click). 

