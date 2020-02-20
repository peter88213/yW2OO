# yW2OO (yWriter to LibreOffice converter)

Export a novel from [yWriter 7](http://www.spacejock.com/yWriter7.html) to an OpenDocument text file.

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

3. Move into the `yW2OO_<version number>` folder and run `Install.bat` (double click). This will copy all needed files to the right places.

4. __Optional:__ Open the `yW2OO_<version number>\fonts>` folder, and unzip `CourierPrime.zip`. Install the `.ttf` files (right click -> Install).


## How to use

1. Write your novel in yWriter 7. Make sure, the `<your yWriter project>.yw` folder contains a file named `writer.bat`. If not, copy it from `yW2OO_<version number>\setup>` folder.

2. Close yWriter, move into the `<your yWriter project>.yw` folder, and run `writer.bat` (double click). If everything goes well, LibreOffice Writer will start automatically and show your document as a OpenDocument file named `<your yWriter project>.odt` with a hierarchical structure and with the right styles applied.

3. Fine tune your manuscript typographically with [OOTyW](https://github.com/peter88213/OOTyW/wiki).

## How to uninstall

Move into the `yW2OO_<version number>` folder and run `Uninstall.bat` (double click). 

