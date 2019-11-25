""" Add scene titles to yWriter's html export.

Adds scene titles to yWriter's html export file as html comments.
OpenOffice shall convert these html comments into navigable items.

For further information see https://github.com/peter88213/yW2OO
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import re
import sys

VERSION = 'v1.15.3'
START_MESSAGE = "\nSceTi - Add yWriter's scene titles to its html export " + VERSION

# HTML_FILE is generated by yWriter.
# Invoking command: "Project > Export Project > to html").
# HTML_FILE is placed in the 'Export' subdirectory of the yWriter
# project directory. This should be the sceti working directory.
# Prior to running sceti, HTML_FILE must be preprocessed by yw200.py.
HTML_FILE = 'Exported Project.html'

# DSCR_FILE  is generated by yWriter.
# Invoking command: "Project > Export Project > Scene descriptions").
# DSCR_FILE must be placed in the 'Export' working directory (as done
# by yWriter7). yWriter5 and yWriter6 place this file in the project
# directory one level up. In this case, move DSCR_FILE to 'Export'
# before running sceti.py (generally done by the calling batch file).
DSCR_FILE = 'Auto_Descriptions.txt'

# The scene numbering in yWriter's scene descriptions begins with '0.1'
# in each chapter, so scene titles can be identified by a leading ' 0'
DSCR_SCENE_MARKER = '^ 0'

# Scene title comments are to be inserted here.
HTML_SCENE_MARKER = "<p class='textbody'>"


def figures(number):
    figures = 0
    dec = 1
    while((number) / dec) >= 1:
        dec = dec * 10
        figures = figures + 1
    return(figures)


def create_bookmarks(sceneTotal):
    """ Create a bookmark string for each scene """
    figuresST = figures(sceneTotal)
    bookmarks = []
    scene = 1
    while scene <= sceneTotal:
        bookmarks.append(((figuresST - figures(scene)) * '0') +
                         str(scene) + '00')
        scene = scene + 1
    return(bookmarks)


def collect_scene_titles(dscrData):
    """ Generate a list of numbered scene titles. """
    # Identify scene titles, replace their first characters
    # by the chapter number, and add them to the scene list.
    # Non-blank lines without a scene marker count as
    # chapter titles.
    sceneList = []
    # The first chapter title is preceded by the project title.
    # This is compensated by a negative chapter counter preset.
    chapterCount = -1
    for line in dscrData:
        if re.search(DSCR_SCENE_MARKER, line):
            sceneList.append(
                re.sub(DSCR_SCENE_MARKER, str(chapterCount), line))
        elif re.search('.+', line.rstrip()):
            chapterCount = chapterCount + 1
    return(sceneList)


def insert_scene_titles(bookTitle, htmlInput, sceneTitles):
    """ Put html comments with numbered scene titles to scene beginnings. """
    sceneTotalExpected = len(sceneTitles)
    bookmarks = create_bookmarks(sceneTotalExpected)
    # Identify scene beginnings and insert html comments before them.
    htmlOutput = []
    sceneCount = 0
    htmlHeader = True
    for line in htmlInput:
        if htmlHeader:
            if line.count('</head>'):
                # Put metadata at the bottom of the html <head>
                # section, if available.
                htmlOutput.append('<title>' + bookTitle + '</title>\n')
                # Exiting the html <head> section
                htmlHeader = False
        if line.count(HTML_SCENE_MARKER):
            try:
                htmlOutput.append(
                    '<a name = "' + bookmarks[sceneCount] + '" />\n')
                htmlOutput.append(
                    '<!-- ' + sceneTitles[sceneCount].rstrip() + ' -->\n')
            except IndexError:
                # Actual count exceeds reference count;
                # this error is considered later on.
                pass
            sceneCount = sceneCount + 1
        # Copy the original html line.
        htmlOutput.append(line)

    if sceneCount == 0:
        print('ERROR: "' + HTML_FILE +
              '" is not preprocessed or contains no scene.\nPlease run yW2OO.py first!\n')
        sys.exit(1)

    if sceneCount != sceneTotalExpected:
        print('ERROR: "' + HTML_FILE + '" and "' + DSCR_FILE +
              '" do not match.\nPlease re-export outline first!\n')
        sys.exit(1)

    try:
        with open(HTML_FILE, 'w') as f:
            f.writelines(htmlOutput)
        print('Added ' + str(sceneCount) +
              ' scene titles as comments to "' + HTML_FILE + '".\n')
    except IOError:
        print('ERROR: Cannot write "' + HTML_FILE + '".\n')
        sys.exit(1)


def main():
    print(START_MESSAGE)

    try:
        with open(HTML_FILE, 'r') as f:
            htmlInput = f.readlines()
    except IOError:
        print('ERROR: Cannot open "' + HTML_FILE +
              '".\nPlease export yWriter project as html first!\n')
        sys.exit(1)

    try:
        with open(DSCR_FILE, 'r') as f:
            dscrData = f.readlines()
    except:
        print('ERROR: Cannot open "' + DSCR_FILE +
              '".\nPlease export outline first!\n')
        sys.exit(1)

    bookTitle = dscrData[0].rstrip()
    insert_scene_titles(bookTitle, htmlInput, collect_scene_titles(dscrData))


if __name__ == '__main__':
    main()
