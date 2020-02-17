"""PyWriter v1.2 - Import and export ywriter7 scenes for editing. 

Proof reading file format: html (with invisible chapter and scene tags)

Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import subprocess


import re
import zipfile
import locale
from shutil import rmtree
from datetime import datetime

from abc import abstractmethod

startWriter = False


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

        self.summary = None
        # str

        self.author = None
        # str

        self.fieldTitle1 = None
        # str

        self.fieldTitle2 = None
        # str

        self.fieldTitle3 = None
        # str

        self.fieldTitle4 = None
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

    @abstractmethod
    def read(self):
        """Parse the file and store selected properties.
        To be overwritten by file format specific subclasses.
        """

    @abstractmethod
    def write(self, novel):
        """Write selected novel properties to the file.
        To be overwritten by file format specific subclasses.
        """

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


class OdtFile(Novel):
    """OpenDocument xml project file representation."""

    _FILE_EXTENSION = '.odt'
    _TEMPDIR = 'temp_odt'
    _ODT_COMPONENTS = ['Configurations2', 'manifest.rdf', 'META-INF', 'content.xml', 'meta.xml', 'mimetype', 'settings.xml', 'styles.xml', 'Configurations2/accelerator', 'Configurations2/floater', 'Configurations2/images', 'Configurations2/menubar',
                       'Configurations2/popupmenu', 'Configurations2/progressbar', 'Configurations2/statusbar', 'Configurations2/toolbar', 'Configurations2/toolpanel', 'Configurations2/accelerator/current.xml', 'Configurations2/images/Bitmaps', 'META-INF/manifest.xml']

    _SCENE_DIVIDER = '* * *'
    # To be placed between scene ending and beginning tags.

    _ODT_HEADER = '''<?xml version="1.0" encoding="UTF-8"?>

<office:document-content xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" xmlns:ooo="http://openoffice.org/2004/office" xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" xmlns:dr3d="urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0" xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0" xmlns:chart="urn:oasis:names:tc:opendocument:xmlns:chart:1.0" xmlns:rpt="http://openoffice.org/2005/report" xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0" xmlns:number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0" xmlns:ooow="http://openoffice.org/2004/writer" xmlns:oooc="http://openoffice.org/2004/calc" xmlns:of="urn:oasis:names:tc:opendocument:xmlns:of:1.2" xmlns:css3t="http://www.w3.org/TR/css3-text/" xmlns:tableooo="http://openoffice.org/2009/table" xmlns:calcext="urn:org:documentfoundation:names:experimental:calc:xmlns:calcext:1.0" xmlns:drawooo="http://openoffice.org/2010/draw" xmlns:loext="urn:org:documentfoundation:names:experimental:office:xmlns:loext:1.0" xmlns:grddl="http://www.w3.org/2003/g/data-view#" xmlns:field="urn:openoffice:names:experimental:ooo-ms-interop:xmlns:field:1.0" xmlns:math="http://www.w3.org/1998/Math/MathML" xmlns:form="urn:oasis:names:tc:opendocument:xmlns:form:1.0" xmlns:script="urn:oasis:names:tc:opendocument:xmlns:script:1.0" xmlns:dom="http://www.w3.org/2001/xml-events" xmlns:xforms="http://www.w3.org/2002/xforms" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:formx="urn:openoffice:names:experimental:ooxml-odf-interop:xmlns:form:1.0" xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns:officeooo="http://openoffice.org/2009/office" office:version="1.2">
 <office:scripts/>
 <office:font-face-decls>
  <style:font-face style:name="StarSymbol" svg:font-family="StarSymbol" style:font-charset="x-symbol"/>
 </office:font-face-decls>
 <office:automatic-styles>
  <style:style style:name="Sect1" style:family="section">
   <style:section-properties style:editable="false">
    <style:columns fo:column-count="1" fo:column-gap="0cm"/>
   </style:section-properties>
  </style:style>
 </office:automatic-styles>
 <office:body>
  <office:text text:use-soft-page-breaks="true">
'''

    _ODT_FOOTER = '''  </office:text>
 </office:body>
</office:document-content>
'''

    _ODT_HEADING_MARKERS = ['<text:h text:style-name="Heading_20_2" text:outline-level="2">',
                            '<text:h text:style-name="Heading_20_1" text:outline-level="1">']

    _ODT_META = '''<?xml version="1.0" encoding="utf-8"?>
<office:document-meta xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" xmlns:ooo="http://openoffice.org/2004/office" xmlns:grddl="http://www.w3.org/2003/g/data-view#" office:version="1.2">
  <office:meta>
    <meta:generator>PyWriter</meta:generator>
    <dc:title>%title%</dc:title>
    <dc:description>%summary%</dc:description>
    <dc:subject></dc:subject>
    <meta:keyword></meta:keyword>
    <meta:initial-creator>%author%</meta:initial-creator>
    <dc:creator></dc:creator>
    <meta:creation-date>%date%T%time%Z</meta:creation-date>
    <dc:date></dc:date>
  </office:meta>
</office:document-meta>
'''

    def __init__(self, filePath, templatePath):
        Novel.__init__(self, filePath)

        self.sections = False
        self.proofread = False
        self.bookmarks = False
        self.comments = False

        self._templatePath = templatePath

    def tear_down(self):
        try:
            rmtree(self._TEMPDIR)

        except:
            pass

    def write(self, novel):
        """Generate an odt file from a template.
        Return a message beginning with SUCCESS or ERROR.
        """

        def set_up():
            self.tear_down()
            os.mkdir(self._TEMPDIR)

            with zipfile.ZipFile(self._templatePath, 'r') as odtTemplate:
                odtTemplate.extractall(self._TEMPDIR)

        def format_chapter_title(text):
            """Fix auto-chapter titles for non-English """
            text = text.replace('Chapter ', '')
            return text

        def to_odt(text):
            """Convert yw7 raw markup to html. Return a html string."""
            try:
                text = text.replace(
                    '\n', '</text:p>\n<text:p text:style-name="First_20_line_20_indent">')
                text = text.replace(
                    '[i]', '<text:span text:style-name="Emphasis">')
                text = text.replace('[/i]', '</text:span>')
                text = text.replace(
                    '[b]', '<text:span text:style-name="Strong_20_Emphasis">')
                text = text.replace('[/b]', '</text:span>')

            except:
                pass

            return text

        def set_locale():
            localeCodes = locale.getdefaultlocale()[0].split('_')
            languageCode = localeCodes[0]
            countryCode = localeCodes[1]
            try:
                with open(self._TEMPDIR + '/styles.xml', 'r', encoding='utf-8') as f:
                    text = f.read()

            except:
                return 'ERROR: cannot read "styles.xml"'

            text = re.sub('fo\:language\=\"..',
                          'fo:language="' + languageCode, text)
            text = re.sub('fo\:country\=\"..',
                          'fo:country="' + countryCode, text)
            try:
                with open(self._TEMPDIR + '/styles.xml', 'w', encoding='utf-8') as f:
                    f.write(text)

            except:
                return 'ERROR: Cannot write "styles.xml"'

            return 'SUCCESS: Locale set to "' + locale.getdefaultlocale()[0] + '".'

        def write_metadata():
            dt = datetime.today()
            date = str(dt.year) + '-' + str(dt.month).rjust(2, '0') + '-' + \
                str(dt.day).rjust(2, '0')
            time = str(dt.hour).rjust(2, '0') + ':' + \
                str(dt.minute).rjust(2, '0') + ':' + \
                str(dt.second).rjust(2, '0')
            text = self._ODT_META.replace('%author%', self.author).replace('%title%', self.title).replace(
                '%summary%', '<![CDATA[' + self.summary + ']]>').replace('%date%', date).replace('%time%', time)

            try:
                with open(self._TEMPDIR + '/meta.xml', 'w', encoding='utf-8') as f:
                    f.write(text)

            except:
                return 'ERROR: Cannot write "meta.xml".'

            return 'SUCCESS: Metadata written to "meta.xml"'

        def write_content():
            lines = [self._ODT_HEADER]

            for chId in self.srtChapters:

                if self.sections and self.chapters[chId].chType == 0 and not self.chapters[chId].isUnused:
                    lines.append(
                        '<text:section text:style-name="Sect1" text:name="ChID:' + chId + '">')

                if self.proofread:
                    if self.chapters[chId].isUnused:
                        lines.append(
                            '<text:p text:style-name="yWriter_20_mark_20_unused">[ChID:' + chId + ' (Unused)]</text:p>')

                    elif self.chapters[chId].chType != 0:
                        lines.append(
                            '<text:p text:style-name="yWriter_20_mark_20_info">[ChID:' + chId + ' (Info)]</text:p>')

                    else:
                        lines.append(
                            '<text:p text:style-name="yWriter_20_mark">[ChID:' + chId + ']</text:p>')

                if self.proofread or ((not self.chapters[chId].isUnused) and self.chapters[chId].chType == 0):
                    headingMarker = self._ODT_HEADING_MARKERS[self.chapters[chId].chLevel]
                    lines.append(headingMarker + format_chapter_title(
                        self.chapters[chId].title) + '</text:h>')

                    firstSceneInChapter = True

                    for scId in self.chapters[chId].srtScenes:

                        if self.proofread or not self.scenes[scId].isUnused:

                            if not firstSceneInChapter:
                                lines.append(
                                    '<text:p text:style-name="Heading_20_4">' + self._SCENE_DIVIDER + '</text:p>')

                            if self.sections:
                                lines.append(
                                    '<text:section text:style-name="Sect1" text:name="ScID:' + scId + '">')

                            if self.proofread:

                                if self.scenes[scId].isUnused or self.chapters[chId].isUnused:
                                    lines.append(
                                        '<text:p text:style-name="yWriter_20_mark_20_unused">[ScID:' + scId + ' (Unused)]</text:p>')

                                elif self.chapters[chId].chType != 0:
                                    lines.append(
                                        '<text:p text:style-name="yWriter_20_mark_20_info">[ScID:' + scId + ' (Info)]</text:p>')

                                else:
                                    lines.append(
                                        '<text:p text:style-name="yWriter_20_mark">[ScID:' + scId + ']</text:p>')

                            scenePrefix = '<text:p text:style-name="Text_20_body">'

                            if self.bookmarks:
                                scenePrefix += '<text:bookmark text:name="ScID:' + scId + '"/>'

                            if self.comments:
                                scenePrefix += ('<office:annotation>\n' +
                                                '<dc:creator>scene title</dc:creator>\n' +
                                                '<text:p>' + self.scenes[scId].title + '</text:p>\n' +
                                                '</office:annotation>')

                            if self.scenes[scId].sceneContent is not None:
                                lines.append(scenePrefix +
                                             to_odt(self.scenes[scId].sceneContent) + '</text:p>')

                            else:
                                lines.append(scenePrefix + '</text:p>')

                            firstSceneInChapter = False

                            if self.proofread:

                                if self.scenes[scId].isUnused or self.chapters[chId].isUnused:
                                    lines.append(
                                        '<text:p text:style-name="yWriter_20_mark_20_unused">[/ScID (Unused)]</text:p>')

                                elif self.chapters[chId].chType != 0:
                                    lines.append(
                                        '<text:p text:style-name="yWriter_20_mark_20_info">[/ScID (Info)]</text:p>')

                                else:
                                    lines.append(
                                        '<text:p text:style-name="yWriter_20_mark">[/ScID]</text:p>')

                            if self.sections:
                                lines.append('</text:section>')

                if self.proofread:

                    if self.chapters[chId].isUnused:
                        lines.append(
                            '<text:p text:style-name="yWriter_20_mark_20_unused">[/ChID (Unused)]</text:p>')

                    elif self.chapters[chId].chType != 0:
                        lines.append(
                            '<text:p text:style-name="yWriter_20_mark_20_info">[/ChID (Info)]</text:p>')

                    else:
                        lines.append(
                            '<text:p text:style-name="yWriter_20_mark">[/ChID]</text:p>')

                if self.sections and self.chapters[chId].chType == 0 and not self.chapters[chId].isUnused:
                    lines.append('</text:section>')

            lines.append(self._ODT_FOOTER)
            text = '\n'.join(lines)

            try:
                with open(self._TEMPDIR + '/content.xml', 'w', encoding='utf-8') as f:
                    f.write(text)

            except:
                return 'ERROR: Cannot write "content.xml".'

            return 'SUCCESS: Content written to "content.xml"'

        # Copy the novel's attributes to write

        if novel.title is None:
            self.title = ''

        else:
            self.title = novel.title

        if novel.summary is None:
            self.summary = ''

        else:
            self.summary = novel.summary

        if novel.author is None:
            self.author = ''

        else:
            self.author = novel.author

        if novel.srtChapters != []:
            self.srtChapters = novel.srtChapters

        if novel.scenes is not None:
            self.scenes = novel.scenes

        if novel.chapters is not None:
            self.chapters = novel.chapters

        set_up()

        message = write_content()

        if message.startswith('ERROR'):
            return message

        message = write_metadata()

        if message.startswith('ERROR'):
            return message

        message = set_locale()

        if message.startswith('ERROR'):
            return message

        try:
            with zipfile.ZipFile(self.filePath, 'w') as odtTarget:
                workdir = os.getcwd()
                os.chdir(self._TEMPDIR)
                for file in self._ODT_COMPONENTS:
                    odtTarget.write(file)
        except:
            os.chdir(workdir)
            return 'ERROR: Cannot generate "' + self._filePath + '".'

        os.chdir(workdir)
        self.tear_down()
        return 'SUCCESS: "' + self._filePath + '" saved.'


import xml.etree.ElementTree as ET


class Chapter():
    """yWriter chapter representation."""

    def __init__(self):
        self.title = None
        # str

        self.summary = None
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

        self.summary = None
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

        self.tags = None
        # list of str

        self.sceneNotes = None
        # str

        self.field1 = None
        # str

        self.field2 = None
        # str

        self.field3 = None
        # str

        self.field4 = None
        # str

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


def indent(elem, level=0):
    """xml pretty printer

    Kudos to to Fredrik Lundh. 
    Source: http://effbot.org/zone/element-lib.htm#prettyprint
    """
    i = "\n" + level * "  "

    if len(elem):

        if not elem.text or not elem.text.strip():
            elem.text = i + "  "

        if not elem.tail or not elem.tail.strip():
            elem.tail = i

        for elem in elem:
            indent(elem, level + 1)

        if not elem.tail or not elem.tail.strip():
            elem.tail = i

    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def cdata(filePath, cdataTags: list):
    '''Postprocess the xml file created by ElementTree:
       Put a header on top and insert the missing CDATA tags.
    '''
    with open(filePath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    newlines = ['<?xml version="1.0" encoding="utf-8"?>\n']

    for line in lines:

        for tag in cdataTags:
            line = re.sub('\<' + tag + '\>', '<' +
                          tag + '><![CDATA[', line)
            line = re.sub('\<\/' + tag + '\>',
                          ']]></' + tag + '>', line)

        newlines.append(line)

    newXml = ''.join(newlines)
    newXml = newXml.replace('[CDATA[ \n', '[CDATA[')
    newXml = newXml.replace('\n]]', ']]')

    try:
        with open(filePath, 'w', encoding='utf-8') as f:
            f.write(newXml)

    except:
        return 'ERROR: Can not write"' + filePath + '".'

    return 'SUCCESS: "' + filePath + '" written.'


class Yw7File(Novel):
    """yWriter 7 xml project file representation."""

    _FILE_EXTENSION = '.yw7'
    # overwrites PywFile._FILE_EXTENSION

    def __init__(self, filePath):
        Novel.__init__(self, filePath)
        self._cdataTags = ['Title', 'AuthorName', 'Bio', 'Desc', 'FieldTitle1', 'FieldTitle2', 'FieldTitle3', 'FieldTitle4',
                           'LaTeXHeaderFile', 'Tags', 'AKA', 'ImageFile', 'FullName', 'Goals', 'Notes', 'RTFFile', 'SceneContent']
        # Names of yw7 xml elements containing CDATA.
        # ElementTree.write omits CDATA tags, so they have to be inserted
        # afterwards.

    def read(self):
        """Parse the yw7 xml file located at filePath, fetching the Novel attributes.
        Return a message beginning with SUCCESS or ERROR.
        """

        # Complete list of tags requiring CDATA (if incomplete).

        try:
            with open(self._filePath, 'r', encoding='utf-8') as f:
                xmlData = f.read()

        except(FileNotFoundError):
            return 'ERROR: "' + self._filePath + '" not found.'

        lines = xmlData.split('\n')

        for line in lines:
            tag = re.search('\<(.+?)\>\<\!\[CDATA', line)

            if tag is not None:

                if not (tag.group(1) in self._cdataTags):
                    self._cdataTags.append(tag.group(1))

        # Open the file again and let ElementTree parse its xml structure.

        try:
            self._tree = ET.parse(self._filePath)
            root = self._tree.getroot()

        except:
            return 'ERROR: Can not process "' + self._filePath + '".'

        prj = root.find('PROJECT')
        self.title = prj.find('Title').text

        if prj.find('AuthorName') is not None:
            self.author = prj.find('AuthorName').text

        if prj.find('Desc') is not None:
            self.summary = prj.find('Desc').text

        self.fieldTitle1 = prj.find('FieldTitle1').text
        self.fieldTitle2 = prj.find('FieldTitle2').text
        self.fieldTitle3 = prj.find('FieldTitle3').text
        self.fieldTitle4 = prj.find('FieldTitle4').text

        for chp in root.iter('CHAPTER'):
            chId = chp.find('ID').text
            self.chapters[chId] = Chapter()
            self.chapters[chId].title = chp.find('Title').text
            self.srtChapters.append(chId)

            if chp.find('Desc') is not None:
                self.chapters[chId].summary = chp.find('Desc').text

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

            if scn.find('Desc') is not None:
                self.scenes[scId].summary = scn.find('Desc').text

            if scn.find('Notes') is not None:
                self.scenes[scId].sceneNotes = scn.find('Notes').text

            if scn.find('Field1') is not None:
                self.scenes[scId].field1 = scn.find('Field1').text

            if scn.find('Field2') is not None:
                self.scenes[scId].field2 = scn.find('Field2').text

            if scn.find('Field3') is not None:
                self.scenes[scId].field3 = scn.find('Field3').text

            if scn.find('Field4') is not None:
                self.scenes[scId].field4 = scn.find('Field4').text

            if scn.find('Tags') is not None:

                if scn.find('Tags').text is not None:
                    self.scenes[scId].tags = scn.find('Tags').text.split(';')

            if scn.find('Unused') is not None:
                self.scenes[scId].isUnused = True

            sceneContent = scn.find('SceneContent').text

            if sceneContent is not None:
                self.scenes[scId].sceneContent = sceneContent

        return 'SUCCESS: ' + str(len(self.scenes)) + ' Scenes read from "' + self._filePath + '".'

    def is_locked(self):
        """Test whether a .lock file placed by yWriter exists.
        """
        if os.path.isfile(self._filePath + '.lock'):
            return True

        else:
            return False


TITLE = 'yW2OO v2.1'

LIBREOFFICE = ['c:/Program Files/LibreOffice/program/swriter.exe',
               'c:/Program Files (x86)/LibreOffice/program/swriter.exe',
               'c:/Program Files/LibreOffice 5/program/swriter.exe',
               'c:/Program Files (x86)/LibreOffice 5/program/swriter.exe']


SUFFIX = '_exp'
# File name suffix for the exported html file.
# Example:
# foo.yw7 --> foo_exp.html


def main():
    sourcePath = None

    templatePath = os.environ['USERPROFILE'] + \
        '/AppData/Roaming/LibreOffice/4/user/yW2OO/template.zip'

    if not os.path.isfile(templatePath):
        return 'ERROR: "' + templatePath + '" not found.'

    files = os.listdir('.')

    for file in files:

        if '.yw7' in file:
            sourcePath = file
            break

    if sourcePath is None:
        return 'ERROR: No yWriter 7 project found.'

    print('Export yWriter7 scenes content to odt')
    print('Project: "' + sourcePath + '"')
    yw7File = Yw7File(sourcePath)

    if yw7File.is_locked():
        return 'ERROR: yWriter 7 seems to be open. Please close first.'

    message = yw7File.read()

    if message.startswith('ERROR'):
        return (message)

    document = OdtFile(sourcePath.split('.yw7')[
                       0] + SUFFIX + '.odt', templatePath)
    document.comments = True
    message = document.write(yw7File)

    if message.startswith('ERROR'):
        return (message)

    if startWriter:

        for lo in LIBREOFFICE:

            if os.path.isfile(lo):
                cmd = [os.path.normpath(lo)]
                cmd.append(document.filePath)
                subprocess.call(cmd)
                break

    return (message)


if __name__ == '__main__':
    startWriter = True
    print(main())
