# yW2OO

![screenshot](Screenshots/yw2oo_cm.png)


[yWriter](http://spacejock.com/yWriter7.html) is a free word processor written by Australian author and programmer Simon Haynes. yWriter's strengths are structuring novels and controlling the progress during the writing process. With this Python script, you can combine the advantages of yWriter 7 with the advantages of OpenOffice/LibreOffice.


## Features (a Python 3 installation is required)

- Launch via Windows Explorer context menu. Optionally, use the graphical user interface to select the yWriter project and the export    document type. 
- Generate a "standard manuscript" formatted **ODF text document (ODT)** from a yWriter 7 project.
- Load yWriter 7 chapters and scenes into an OpenDocument file with chapter and scene markers for **proof reading** and writing back.
- Generate a **brief synopsis** with chapter and scene titles from a yWriter 7 project.
- Generate a **character list** that can be edited in Office Calc and written back to yWriter format.
- Generate a **location list** that can be edited in Office Calc and written back to yWriter format.
- Generate an **item list** that can be edited in Office Calc and written back to yWriter format.
- Generate an OpenDocument text file containing navigable **cross references** , such as scenes per character, characters per tag, etc.
- Generate a new yWriter 7 project from a **work in progress** or an **outline**.
- Update an existing yWriter 7 project with an edited text or spreadsheet document.
- The application is ready for internationalization with GNU gettext. A German localization is provided. 

With the [pywoo extension for OpenOffice](https://peter88213.github.io/pywoo) and the [yw-cnv extension for LibreOffice](https://peter88213.github.io/yw-cnv), you can write your edited Office documents back to the yWriter project.

    
## Requirements

- [Python](https://www.python.org/) from version 3.6.

## Please note: 

yW2OO was fundamentally revised. 

- If you want to update it from a version less than v3, 
first uninstall your current yW2OO installation with its included **Uninstall.bat** script.
- If you want to update it from version 3.x or 4.x, make sure to create a new shortcut, and re-run the registry files for the explorer context menu after installation.

## Download and install

[Download the latest release (version 5.3.0)](https://raw.githubusercontent.com/peter88213/yW2OO/main/dist/yw2oo_v5.3.0.zip)

- Extract the "yW2OO_v5.3.0" folder from the downloaded zipfile "yW2OO_v5.3.0.zip"
- Move into this new folder and open "README.md" for further instructions.

### Note for Linux users

Please make sure that your Python3 installation has the *tkinter* module. On Ubuntu, for example, it is not available out of the box and must be installed via a separate package. 

---

[Changelog](changelog)

## Usage

See the [instructions for use](usage)


## Credits

The icons are made using the free *Pusab* font by Ryoichi Tsunekawa, [Flat-it](http://flat-it.com/).

## License

yW2OO is distributed under the [MIT License](http://www.opensource.org/licenses/mit-license.php).


 




