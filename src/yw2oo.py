"""yW2OO v2.0 -Export ywriter7 scenes as html. 

Syntax: yw2oo.py
An .yw7 project file must exist within the working directory. 

Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/yW2OO
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import sys
import os
import subprocess
import re
import xml.etree.ElementTree as ET

TITLE = 'yW2OO v2.0'

LIBREOFFICE = ['c:/Program Files/LibreOffice/program/swriter.exe',
               'c:/Program Files (x86)/LibreOffice/program/swriter.exe',
               'c:/Program Files/LibreOffice 5/program/swriter.exe',
               'c:/Program Files (x86)/LibreOffice 5/program/swriter.exe']


SUFFIX = '_exp'
# File name suffix for the exported html file.
# Example:
# foo.yw7 --> foo_exp.html

HTML_SCENE_DIVIDER = '* * *'
# To be placed between scene ending and beginning tags.

# Make the generated html file look good in a web browser:

STYLESHEET = '<style type="text/css">\n' + \
    'h1, h2, h3, h4, p {font: 1em monospace; margin: 3em; line-height: 1.5em}\n' + \
    'h1, h2, h3, h4 {text-align: center}\n' +\
    'h1 {letter-spacing: 0.2em; font-style: italic}' + \
    'h1, h2 {font-weight: bold}\n' + \
    'h3 {font-style: italic}\n' + \
    'p.textbody {margin-top:0; margin-bottom:0}\n' + \
    'p.firstlineindent {margin-top:0; margin-bottom:0; text-indent: 1em}\n' + \
    'strong {font-weight:normal; text-transform: uppercase}\n' + \
    '</style>\n'

HTML_HEADER = '<html>\n' + '<head>\n' + \
    '<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>\n' + STYLESHEET + \
    '<title>$bookTitle$</title>\n' + \
    '</head>\n' + '<body>\n'

HTML_FOOTER = '\n</body>\n</html>\n'

HTML_HEADING_MARKERS = ("h2", "h1")
# Index is yWriter's chapter chLevel:
# 0 is for an ordinary chapter
# 1 is for a chapter beginning a section


def to_html(text):
    """Convert yw7 raw markup to html. Return a html string."""
    try:
        text = text.replace('\n', '</p>\n<p class="firstlineindent">')
        text = text.replace('[i]', '<em>')
        text = text.replace('[/i]', '</em>')
        text = text.replace('[b]', '<strong>')
        text = text.replace('[/b]', '</strong>')
        text = re.sub('\<p(.+?)\>\<\/p\>', '<p\g<1>><br></p>', text)

    except:
        pass

    return text


class Novel():
    """Abstract yWriter project file representation.

    This class represents a file containing a novel with additional 
    attributes and structural information (a full set or a subset
    of the information included in an yWriter project file).
    """

    _FILE_EXTENSION = ''
    # To be extended by file format specific subclasses.

    def __init__(self, filePath):
        self.title = None
        # str

        self.chapters = {}
        # key = chapter ID, value = Chapter object.
        # The order of the elements does not matter (the novel's
        # order of the chapters is defined by srtChapters)

        self.scenes = {}
        # key = scene ID, value = Scene object.
        # The order of the elements does not matter (the novel's
        # order of the scenes is defined by the order of the chapters
        # and the order of the scenes within the chapters)

        self.srtChapters = []
        # list of str
        # The novel's chapter IDs. The order of its elements
        # corresponds to the novel's order of the chapters.

        self._filePath = None
        # str
        # Path to the file. The setter only accepts files of a
        # supported type as specified by _FILE_EXTENSION.

        self.filePath = filePath

    @property
    def filePath(self):
        return self._filePath

    @filePath.setter
    def filePath(self, filePath):
        """Accept only filenames with the right extension. """
        if filePath.lower().endswith(self._FILE_EXTENSION):
            self._filePath = filePath

    def file_exists(self):
        """Check whether the file specified by _filePath exists. """
        if os.path.isfile(self._filePath):
            return True

        else:
            return False

    def get_structure(self):
        """returns a string showing the order of chapters and scenes 
        as a tree. The result can be used to compare two Novel objects 
        by their structure.
        """
        lines = []

        for chId in self.srtChapters:
            lines.append('ChID:' + str(chId) + '\n')

            for scId in self.chapters[chId].srtScenes:
                lines.append('  ScID:' + str(scId) + '\n')

        return ''.join(lines)


class Chapter():
    """yWriter chapter representation."""

    def __init__(self):
        self.title = None
        # str

        self.chLevel = None
        # int
        # 0 = chapter level
        # 1 = section level ("this chapter begins a section")

        self.chType = None
        # int
        # 0 = chapter type (marked "Chpter")
        # 1 = other type (marked "Other")

        self.isUnused = None
        # bool

        self.srtScenes = []
        # list of str
        # The chapter's scene IDs. The order of its elements
        # corresponds to the chapter's order of the scenes.


class Scene():
    """yWriter scene representation."""

    def __init__(self):
        self.title = None
        # str

        self._sceneContent = None
        # str
        # Scene text with yW7 raw markup.

        self.wordCount = None
        # int
        # To be updated by the sceneContent setter

        self.letterCount = None
        # int
        # To be updated by the sceneContent setter

        self.isUnused = None
        # bool

    @property
    def sceneContent(self):
        return self._sceneContent

    @sceneContent.setter
    def sceneContent(self, text):
        """Set sceneContent updating word count and letter count."""
        self._sceneContent = text
        text = re.sub('\[.+?\]|\.|\,| -', '', self._sceneContent)
        # Remove yw7 raw markup for word count

        wordList = text.split()
        self.wordCount = len(wordList)

        text = re.sub('\[.+?\]', '', self._sceneContent)
        # Remove yw7 raw markup for letter count

        text = text.replace('\n', '')
        text = text.replace('\r', '')
        self.letterCount = len(text)


class Manuscript(Novel):
    """HTML file representation of an yWriter project's manuscript part.

    Represents a html file with chapter and scene sections 
    containing scene contents to be read and written by 
    OpenOffice/LibreOffice Writer.
    """

    _FILE_EXTENSION = 'html'
    # overwrites Novel._FILE_EXTENSION

    def __init__(self, filePath):
        Novel.__init__(self, filePath)
        self._lines = []
        self._scId = None
        self._chId = None

    def write(self, novel):
        """Generate a html file containing:
        - chapter sections containing:
            - chapter headings,
            - scene sections containing:
                - scene ID as anchor, 
                - scene title as comment,
                - scene content.
        Return a message beginning with SUCCESS or ERROR.
        """

        def format_chapter_title(text):
            """Fix auto-chapter titles for non-English """
            text = text.replace('Chapter ', '')
            return text

        # Copy the novel's attributes to write

        if novel.title is not None:
            if novel.title != '':
                self.title = novel.title

        if novel.srtChapters != []:
            self.srtChapters = novel.srtChapters

        if novel.scenes is not None:
            self.scenes = novel.scenes

        if novel.chapters is not None:
            self.chapters = novel.chapters

        lines = [HTML_HEADER.replace('$bookTitle$', self.title)]

        for chId in self.srtChapters:

            if (not self.chapters[chId].isUnused) and self.chapters[chId].chType == 0:
                headingMarker = HTML_HEADING_MARKERS[self.chapters[chId].chLevel]
                lines.append('<' + headingMarker + '>' + format_chapter_title(
                    self.chapters[chId].title) + '</' + headingMarker + '>')

                for scId in self.chapters[chId].srtScenes:

                    if not self.scenes[scId].isUnused:
                        lines.append('<h4>' + HTML_SCENE_DIVIDER + '</h4>')
                        lines.append('<p class="textbody">')

                        # Insert scene title as comment.

                        lines.append(
                            '<!-- ' + self.scenes[scId].title + ' -->')

                        if self.scenes[scId].sceneContent is not None:
                            lines.append(
                                to_html(self.scenes[scId].sceneContent))

                        lines.append('</p>')

        lines.append(HTML_FOOTER)
        text = '\n'.join(lines)

        # Remove scene dividers from chapter's beginning

        text = text.replace('</h1>\n<h4>' + HTML_SCENE_DIVIDER + '</h4>',
                            '</h1>')
        text = text.replace('</h2>\n<h4>' + HTML_SCENE_DIVIDER + '</h4>',
                            '</h2>')

        try:
            with open(self._filePath, 'w', encoding='utf-8') as f:
                f.write(text)

        except(PermissionError):
            return 'ERROR: ' + self._filePath + '" is write protected.'

        return 'SUCCESS: "' + self._filePath + '" saved.'


class Yw7File(Novel):
    """yWriter 7 xml project file representation."""

    _FILE_EXTENSION = '.yw7'
    # overwrites PywFile._FILE_EXTENSION

    def __init__(self, filePath):
        Novel.__init__(self, filePath)

    def read(self):
        """Parse the yw7 xml file located at filePath, fetching the Novel attributes.
        Return a message beginning with SUCCESS or ERROR.
        """
        try:
            self._tree = ET.parse(self._filePath)
            root = self._tree.getroot()

        except:
            return 'ERROR: Can not process "' + self._filePath + '".'

        prj = root.find('PROJECT')
        self.title = prj.find('Title').text

        for chp in root.iter('CHAPTER'):
            chId = chp.find('ID').text
            self.chapters[chId] = Chapter()
            self.chapters[chId].title = chp.find('Title').text
            self.srtChapters.append(chId)

            if chp.find('SectionStart') is not None:
                self.chapters[chId].chLevel = 1

            else:
                self.chapters[chId].chLevel = 0

            if chp.find('Unused') is not None:
                self.chapters[chId].isUnused = True

            else:
                self.chapters[chId].isUnused = False

            self.chapters[chId].chType = int(chp.find('Type').text)

            self.chapters[chId].srtScenes = []

            if chp.find('Scenes') is not None:

                for scn in chp.find('Scenes').findall('ScID'):
                    scId = scn.text
                    self.chapters[chId].srtScenes.append(scId)

        for scn in root.iter('SCENE'):
            scId = scn.find('ID').text

            self.scenes[scId] = Scene()
            self.scenes[scId].title = scn.find('Title').text

            if scn.find('Unused') is not None:
                self.scenes[scId].isUnused = True

            sceneContent = scn.find('SceneContent').text

            if sceneContent is not None:
                self.scenes[scId].sceneContent = sceneContent

        return 'SUCCESS: ' + str(len(self.scenes)) + ' Scenes read from "' + self._filePath + '".'

    def is_locked(self):
        """Test whether a .lock file placed by yWriter exists."""
        if os.path.isfile(self._filePath + '.lock'):
            return True

        else:
            return False


def main():
    sourcePath = None
    files = os.listdir('.')

    for file in files:

        if '.yw7' in file:
            sourcePath = file
            break

    if sourcePath is None:
        print('ERROR: No yWriter 7 project found.')
        exit(1)

    print('Export yWriter7 scenes content to html')
    print('Project: "' + sourcePath + '"')
    yw7File = Yw7File(sourcePath)

    if yw7File.is_locked():
        print('ERROR: yWriter 7 seems to be open. Please close first.')
        sys.exit(1)

    message = yw7File.read()
    print(message)

    if message.startswith('ERROR'):
        sys.exit(1)

    document = Manuscript(sourcePath.split('.yw7')[0] + SUFFIX + '.html')
    message = document.write(yw7File)
    print(message)

    if message.startswith('ERROR'):
        sys.exit(1)

    for lo in LIBREOFFICE:

        if os.path.isfile(lo):
            cmd = [os.path.normpath(lo)]
            cmd.append('macro:///yW2OO.Convert.main')
            cmd.append(document.filePath)
            subprocess.call(cmd)
            break


if __name__ == '__main__':
    main()
