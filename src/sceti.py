"""Add scene titles to yWriter's html export.

@summary: Adds scene titles as comments to yWriter's html export file.
    OpenOffice shall convert these html comments into navigable items.
@author: Peter Triesberger
@see: https://github.com/peter88213/yW2OO
@license: The MIT License 
    (https://opensource.org/licenses/mit-license.php)
@copyright: (c) 2019, Peter Triesberger
@return: Exitcode
    0 if no error occurred; 
    1 if "Auto_Descriptions.txt" cannot be read; 
    2 if "Exported Project.html" cannot be read; 
    3 if "Exported Project.html" is not pre-processed 
      or contains no scene; 
    4 if "Exported Project.html" and "Auto_Descriptions.txt" 
      contain different numbers of scenes; 
    5 if "Exported Project.html" cannot be written. 
@precondition: The file "Exported Project.html" must exist 
    with r/w access in the working directory.
    It must be pre-processed by yW2OO.py. 
@precondition: The File "Auto_Descriptions.txt" must exist 
    in the directory just above the working directory. 
    It must match to "Exported Project.html", 
    i.e the number of sceneTitles must be the same.
@postcondition: The file "Exported Project.html" is overwritten 
    by a new version containing scene titles as html comments. 
@since: 2019-10-05
@change: 2019-10-06 v1.1.0 
    Scene titles are taken from "Auto_Descriptions.txt" 
    instead of "auto_outline.txt". Each scene gets a number.
@change: 2019-10-21 v1.1.1 
    Refactoring for unit test support.
@change: 2019-10-21 v1.1.2 
    Further refactoring: Renamed "main" function to "main".
@change: 2019-10-21 v1.2.0 
    Further refactoring and code documentation. New exit codes.
@change: 2019-10-21 v1.3.0 
    "collect_scene_titles" gets filename as parameter 
    and returns simple list of scenes. 
    "main" uses this data to create html comments.
@change: 2019-10-23 v1.3.1
    Further refactoring according to PEP 8 style guide
    (see https://www.python.org/dev/peps/pep-0008/)
"""

import re
import sys

VERSION = "v1.3.1"

START_MESSAGE = '\nSceTi adding yWriter scene titles to html export ' + VERSION

# (yWriter command: "Project>Export Project>Scene descriptions").
DESC_FILE = "../Auto_Descriptions.txt"

# (yWriter command: "Project>Export Project>to html").
HTML_FILE = "Exported Project.html"

# The scene numbering in yWriter's scene descriptions begins with '0.1'
# in each chapter, so scene titles can be identified by a leading ' 0'
DESC_SCENE_MARKER = "^ 0"

# The yW2OO preprocessor formats each scene's first paragraph as a
# (temporary) 6th level heading. Here's the right place to insert
# scene title annotations.
HTML_SCENE_MARKER = "<H6>"


def collect_scene_titles():
    """Generate a list of numbered scene titles. 

    @summary: Browse the scene descriptions exported by yWriter. 
        Identify chapters and scenes. Put the scene titles in a list,
        adding the correct chapter number to each scene number.  
    @precondition: The File "Auto_Descriptions.txt" must exist 
        in the directory just above the working directory. 
    @return: Sorted list of numbered scene titles.
    """
    try:
        descFile = open(DESC_FILE, 'r')
        descData = descFile.readlines()
        descFile.close()
    except:
        print('ERROR: Cannot open "' + DESC_FILE +
              '".\nPlease export outline first!\n')
        sys.exit(1)
    else:
        # Declare a List for numbered scene titles.
        sceneTitles = []
        # Declare a Counter for non-empty lines generally containing
        # chapter titles. The first non-empty line contains the project
        # title; this is compensated by a negative counter preset.
        chapterCount = -1
        for line in descData:
            # Count chapter entries and generate annotations
            # with numbered scene titles.
            if re.search(".+", line.rstrip()) is not None:
                # The line is not empty. Is it a scene title?
                if re.search(DESC_SCENE_MARKER, line) is None:
                    # The line is not a scene title,
                    # so it must be the next chapter title.
                    chapterCount = chapterCount + 1
                else:
                    # The line contains a scene title.
                    # Replace the first characters by the chapter number
                    # and add the line to the scene list.
                    sceneTitles.append(
                        re.sub(DESC_SCENE_MARKER, str(chapterCount), line))
        return(sceneTitles)


def insert_scene_titles(sceneTitles):
    """ Put html comments with numbered scene titles to scene beginnings.

    @summary: Browse the html project file exported by yWriter and 
        preprocessed by yw2oo.py. 
    @param: sceneTitles Sorted list of numbered scene titles.
    @precondition: The file "Exported Project.html" must exist with r/w access
        in the working directory. It must be pre-processed by yW2OO.py. 
    @postcondition: The html project file is overwritten by a new version
        containing scene titles as html comments. 
    """
    try:
        # Open yWriter's html export file
        # (hopefully pre-processed by yW2OO.py).
        htmlFile = open(HTML_FILE, 'r')
        htmlData = htmlFile.readlines()
        htmlFile.close()
    except:
        print('ERROR: Cannot open "' + HTML_FILE +
              '".\nPlease export yWriter project as html first!\n')
        sys.exit(2)
    else:
        # Declare a REFERENCE number of scenes.
        # If the html project file contains the same number of scenes,
        # the scene descriptions file is considered matching.
        outlineSceneCount = len(sceneTitles)
        # Now browse the html project file for scene beginnings.
        # First declare a counter for paragraphs formatted by yW2OO.py
        # as scene beginnings.
        htmlSceneCount = 0
        # Declare a list for the new html document including annotations.
        htmlWithAnnotations = []
        for line in htmlData:
            if line.count(HTML_SCENE_MARKER) > 0:
                # Found a new scene in the project.
                # Does it fit to yWriter's scene descriptions?
                if htmlSceneCount < outlineSceneCount:
                    # Maybe ... so let's insert an one-line html annotation
                    # containing the title.
                    htmlWithAnnotations.append(
                        "<!-- " + sceneTitles[htmlSceneCount].rstrip() + " -->\n")
                # Increase the ACTUAL number of scenes.
                htmlSceneCount = htmlSceneCount + 1
            htmlWithAnnotations.append(line)        # Copy original html line.
        if htmlSceneCount == 0:
            # Not a single html scene marker was found:
            # The html file seems to be not preprocessed.
            print('ERROR: "' + HTML_FILE +
                  '" is not pre-processed or contains no scene.\nPlease run yW2OO.py first!\n')
            sys.exit(3)
        elif htmlSceneCount != outlineSceneCount:
            # html export and scene descriptions seem not to fit together.
            print('ERROR: "' + HTML_FILE + '" and "' + DESC_FILE +
                  '" do not match.\nPlease re-export outline first!\n')
            sys.exit(4)
        else:
            # html export and scene descriptions have
            # the same number of scenes.
            try:
                # Overwrite yWriter's html export file.
                htmlFile = open(HTML_FILE, 'w')
                htmlFile.writelines(htmlWithAnnotations)
                htmlFile.close()
                print('Added ' + str(outlineSceneCount) +
                      ' scene titles as comments to "' + HTML_FILE + '".\n')
            except:
                print('ERROR: Cannot write "' + HTML_FILE + '".\n')
                sys.exit(5)
            else:
                return(0)


def main():
    print(START_MESSAGE)     # Must contain the correct version number!
    insert_scene_titles(collect_scene_titles())


if __name__ == '__main__':
    main()
