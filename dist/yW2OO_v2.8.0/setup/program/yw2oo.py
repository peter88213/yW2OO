"""yW2OO - Export yWriter scenes to odt. 

Depends on the PyWriter library v1.6

Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/yW2OO
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os


import zipfile

import re
import locale
from shutil import rmtree
from datetime import datetime


class OdtTemplate():

    _ODT_HEADING_STARTS = ['<text:h text:style-name="Heading_20_2" text:outline-level="2">',
                           '<text:h text:style-name="Heading_20_1" text:outline-level="1">',
                           '<text:h text:style-name="Heading_20_3" text:outline-level="3">']
    _ODT_HEADING_END = '</text:h>'

    _ODT_TITLE_START = '<text:p text:style-name="Title">'
    _ODT_SUBTITLE_START = '<text:p text:style-name="Subtitle">'

    _ODT_FIRST_PARA_START = '<text:p text:style-name="Text_20_body">'
    _ODT_PARA_START = '<text:p text:style-name="First_20_line_20_indent">'
    _ODT_SCENEDIV_START = '<text:p text:style-name="Heading_20_4">'
    _ODT_PARA_END = '</text:p>'

    _TEMPDIR = 'temp_odt'

    _ODT_COMPONENTS = ['manifest.rdf', 'META-INF', 'content.xml', 'meta.xml', 'mimetype',
                       'settings.xml', 'styles.xml', 'META-INF/manifest.xml']

    _CONTENT_XML_HEADER = '''<?xml version="1.0" encoding="UTF-8"?>

<office:document-content xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0" xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" xmlns:number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0" xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0" xmlns:chart="urn:oasis:names:tc:opendocument:xmlns:chart:1.0" xmlns:dr3d="urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0" xmlns:math="http://www.w3.org/1998/Math/MathML" xmlns:form="urn:oasis:names:tc:opendocument:xmlns:form:1.0" xmlns:script="urn:oasis:names:tc:opendocument:xmlns:script:1.0" xmlns:ooo="http://openoffice.org/2004/office" xmlns:ooow="http://openoffice.org/2004/writer" xmlns:oooc="http://openoffice.org/2004/calc" xmlns:dom="http://www.w3.org/2001/xml-events" xmlns:xforms="http://www.w3.org/2002/xforms" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:rpt="http://openoffice.org/2005/report" xmlns:of="urn:oasis:names:tc:opendocument:xmlns:of:1.2" xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns:grddl="http://www.w3.org/2003/g/data-view#" xmlns:tableooo="http://openoffice.org/2009/table" xmlns:field="urn:openoffice:names:experimental:ooo-ms-interop:xmlns:field:1.0" office:version="1.2">
 <office:scripts/>
 <office:font-face-decls>
  <style:font-face style:name="StarSymbol" svg:font-family="StarSymbol" style:font-charset="x-symbol"/>
  <style:font-face style:name="Courier New" svg:font-family="&apos;Courier New&apos;" style:font-adornments="Standard" style:font-family-generic="modern" style:font-pitch="fixed"/>
  <style:font-face style:name="Courier Prime" svg:font-family="&apos;Courier Prime&apos;, &apos;Courier New&apos;" style:font-adornments="Standard" style:font-family-generic="modern" style:font-pitch="fixed"/>
  <style:font-face style:name="Courier New1" svg:font-family="&apos;Courier New&apos;" style:font-family-generic="roman" style:font-pitch="fixed"/>
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
    _CONTENT_XML_FOOTER = '''  </office:text>
 </office:body>
</office:document-content>
'''
    _META_XML = '''<?xml version="1.0" encoding="utf-8"?>
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
    _MANIFEST_XML = '''<?xml version="1.0" encoding="utf-8"?>
<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0" manifest:version="1.2">
  <manifest:file-entry manifest:media-type="application/vnd.oasis.opendocument.text" manifest:full-path="/" />
  <manifest:file-entry manifest:media-type="application/xml" manifest:full-path="content.xml" manifest:version="1.2" />
  <manifest:file-entry manifest:media-type="application/rdf+xml" manifest:full-path="manifest.rdf" manifest:version="1.2" />
  <manifest:file-entry manifest:media-type="application/xml" manifest:full-path="styles.xml" manifest:version="1.2" />
  <manifest:file-entry manifest:media-type="application/xml" manifest:full-path="meta.xml" manifest:version="1.2" />
  <manifest:file-entry manifest:media-type="application/xml" manifest:full-path="settings.xml" manifest:version="1.2" />
</manifest:manifest>    
'''
    _MANIFEST_RDF = '''<?xml version="1.0" encoding="utf-8"?>
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="styles.xml">
    <rdf:type rdf:resource="http://docs.oasis-open.org/ns/office/1.2/meta/odf#StylesFile"/>
  </rdf:Description>
  <rdf:Description rdf:about="">
    <ns0:hasPart xmlns:ns0="http://docs.oasis-open.org/ns/office/1.2/meta/pkg#" rdf:resource="styles.xml"/>
  </rdf:Description>
  <rdf:Description rdf:about="content.xml">
    <rdf:type rdf:resource="http://docs.oasis-open.org/ns/office/1.2/meta/odf#ContentFile"/>
  </rdf:Description>
  <rdf:Description rdf:about="">
    <ns0:hasPart xmlns:ns0="http://docs.oasis-open.org/ns/office/1.2/meta/pkg#" rdf:resource="content.xml"/>
  </rdf:Description>
  <rdf:Description rdf:about="">
    <rdf:type rdf:resource="http://docs.oasis-open.org/ns/office/1.2/meta/pkg#Document"/>
  </rdf:Description>
</rdf:RDF>
'''
    _SETTINGS_XML = '''<?xml version="1.0" encoding="UTF-8"?>

<office:document-settings xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:config="urn:oasis:names:tc:opendocument:xmlns:config:1.0" xmlns:ooo="http://openoffice.org/2004/office" office:version="1.2">
 <office:settings>
  <config:config-item-set config:name="ooo:view-settings">
   <config:config-item config:name="ViewAreaTop" config:type="int">0</config:config-item>
   <config:config-item config:name="ViewAreaLeft" config:type="int">0</config:config-item>
   <config:config-item config:name="ViewAreaWidth" config:type="int">30508</config:config-item>
   <config:config-item config:name="ViewAreaHeight" config:type="int">27783</config:config-item>
   <config:config-item config:name="ShowRedlineChanges" config:type="boolean">true</config:config-item>
   <config:config-item config:name="InBrowseMode" config:type="boolean">false</config:config-item>
   <config:config-item-map-indexed config:name="Views">
    <config:config-item-map-entry>
     <config:config-item config:name="ViewId" config:type="string">view2</config:config-item>
     <config:config-item config:name="ViewLeft" config:type="int">8079</config:config-item>
     <config:config-item config:name="ViewTop" config:type="int">3501</config:config-item>
     <config:config-item config:name="VisibleLeft" config:type="int">0</config:config-item>
     <config:config-item config:name="VisibleTop" config:type="int">0</config:config-item>
     <config:config-item config:name="VisibleRight" config:type="int">30506</config:config-item>
     <config:config-item config:name="VisibleBottom" config:type="int">27781</config:config-item>
     <config:config-item config:name="ZoomType" config:type="short">0</config:config-item>
     <config:config-item config:name="ViewLayoutColumns" config:type="short">0</config:config-item>
     <config:config-item config:name="ViewLayoutBookMode" config:type="boolean">false</config:config-item>
     <config:config-item config:name="ZoomFactor" config:type="short">100</config:config-item>
     <config:config-item config:name="IsSelectedFrame" config:type="boolean">false</config:config-item>
    </config:config-item-map-entry>
   </config:config-item-map-indexed>
  </config:config-item-set>
  <config:config-item-set config:name="ooo:configuration-settings">
   <config:config-item config:name="AddParaSpacingToTableCells" config:type="boolean">true</config:config-item>
   <config:config-item config:name="PrintPaperFromSetup" config:type="boolean">false</config:config-item>
   <config:config-item config:name="IsKernAsianPunctuation" config:type="boolean">false</config:config-item>
   <config:config-item config:name="PrintReversed" config:type="boolean">false</config:config-item>
   <config:config-item config:name="LinkUpdateMode" config:type="short">1</config:config-item>
   <config:config-item config:name="DoNotCaptureDrawObjsOnPage" config:type="boolean">false</config:config-item>
   <config:config-item config:name="SaveVersionOnClose" config:type="boolean">false</config:config-item>
   <config:config-item config:name="PrintEmptyPages" config:type="boolean">true</config:config-item>
   <config:config-item config:name="PrintSingleJobs" config:type="boolean">false</config:config-item>
   <config:config-item config:name="AllowPrintJobCancel" config:type="boolean">true</config:config-item>
   <config:config-item config:name="AddFrameOffsets" config:type="boolean">false</config:config-item>
   <config:config-item config:name="PrintLeftPages" config:type="boolean">true</config:config-item>
   <config:config-item config:name="PrintTables" config:type="boolean">true</config:config-item>
   <config:config-item config:name="ProtectForm" config:type="boolean">false</config:config-item>
   <config:config-item config:name="ChartAutoUpdate" config:type="boolean">true</config:config-item>
   <config:config-item config:name="PrintControls" config:type="boolean">true</config:config-item>
   <config:config-item config:name="PrinterSetup" config:type="base64Binary">8gT+/0hQIExhc2VySmV0IFAyMDE0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAASFAgTGFzZXJKZXQgUDIwMTQAAAAAAAAAAAAAAAAAAAAWAAEAGAQAAAAAAAAEAAhSAAAEdAAAM1ROVwIACABIAFAAIABMAGEAcwBlAHIASgBlAHQAIABQADIAMAAxADQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQQDANwANAMPnwAAAQAJAJoLNAgAAAEABwBYAgEAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAU0RETQAGAAAABgAASFAgTGFzZXJKZXQgUDIwMTQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAEAAAAJAAAACQAAAAkAAAAJAAAACQAAAAkAAAAJAAAACQAAAAkAAAAJAAAACQAAAAkAAAAJAAAACQAAAAkAAAAJAAAACQAAAAAAAAABAAAAAQAAABoEAAAAAAAAAAAAAAAAAAAPAAAALQAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAgICAAP8AAAD//wAAAP8AAAD//wAAAP8A/wD/AAAAAAAAAAAAAAAAAAAAAAAoAAAAZAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADeAwAA3gMAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABrjvBgNAMAAAAAAAAAAAAABIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABIAQ09NUEFUX0RVUExFWF9NT0RFCgBEVVBMRVhfT0ZG</config:config-item>
   <config:config-item config:name="CurrentDatabaseDataSource" config:type="string"/>
   <config:config-item config:name="LoadReadonly" config:type="boolean">false</config:config-item>
   <config:config-item config:name="CurrentDatabaseCommand" config:type="string"/>
   <config:config-item config:name="ConsiderTextWrapOnObjPos" config:type="boolean">false</config:config-item>
   <config:config-item config:name="ApplyUserData" config:type="boolean">true</config:config-item>
   <config:config-item config:name="AddParaTableSpacing" config:type="boolean">true</config:config-item>
   <config:config-item config:name="FieldAutoUpdate" config:type="boolean">true</config:config-item>
   <config:config-item config:name="IgnoreFirstLineIndentInNumbering" config:type="boolean">false</config:config-item>
   <config:config-item config:name="TabsRelativeToIndent" config:type="boolean">true</config:config-item>
   <config:config-item config:name="IgnoreTabsAndBlanksForLineCalculation" config:type="boolean">false</config:config-item>
   <config:config-item config:name="PrintAnnotationMode" config:type="short">0</config:config-item>
   <config:config-item config:name="AddParaTableSpacingAtStart" config:type="boolean">true</config:config-item>
   <config:config-item config:name="UseOldPrinterMetrics" config:type="boolean">false</config:config-item>
   <config:config-item config:name="TableRowKeep" config:type="boolean">false</config:config-item>
   <config:config-item config:name="PrinterName" config:type="string">HP LaserJet P2014</config:config-item>
   <config:config-item config:name="PrintFaxName" config:type="string"/>
   <config:config-item config:name="UnxForceZeroExtLeading" config:type="boolean">false</config:config-item>
   <config:config-item config:name="PrintTextPlaceholder" config:type="boolean">false</config:config-item>
   <config:config-item config:name="DoNotJustifyLinesWithManualBreak" config:type="boolean">false</config:config-item>
   <config:config-item config:name="PrintRightPages" config:type="boolean">true</config:config-item>
   <config:config-item config:name="CharacterCompressionType" config:type="short">0</config:config-item>
   <config:config-item config:name="UseFormerTextWrapping" config:type="boolean">false</config:config-item>
   <config:config-item config:name="IsLabelDocument" config:type="boolean">false</config:config-item>
   <config:config-item config:name="AlignTabStopPosition" config:type="boolean">true</config:config-item>
   <config:config-item config:name="PrintHiddenText" config:type="boolean">false</config:config-item>
   <config:config-item config:name="DoNotResetParaAttrsForNumFont" config:type="boolean">false</config:config-item>
   <config:config-item config:name="PrintPageBackground" config:type="boolean">true</config:config-item>
   <config:config-item config:name="CurrentDatabaseCommandType" config:type="int">0</config:config-item>
   <config:config-item config:name="OutlineLevelYieldsNumbering" config:type="boolean">false</config:config-item>
   <config:config-item config:name="PrintProspect" config:type="boolean">false</config:config-item>
   <config:config-item config:name="PrintGraphics" config:type="boolean">true</config:config-item>
   <config:config-item config:name="SaveGlobalDocumentLinks" config:type="boolean">false</config:config-item>
   <config:config-item config:name="PrintProspectRTL" config:type="boolean">false</config:config-item>
   <config:config-item config:name="UseFormerLineSpacing" config:type="boolean">false</config:config-item>
   <config:config-item config:name="AddExternalLeading" config:type="boolean">true</config:config-item>
   <config:config-item config:name="UseFormerObjectPositioning" config:type="boolean">false</config:config-item>
   <config:config-item config:name="RedlineProtectionKey" config:type="base64Binary"/>
   <config:config-item config:name="MathBaselineAlignment" config:type="boolean">false</config:config-item>
   <config:config-item config:name="ClipAsCharacterAnchoredWriterFlyFrames" config:type="boolean">false</config:config-item>
   <config:config-item config:name="UseOldNumbering" config:type="boolean">false</config:config-item>
   <config:config-item config:name="PrintDrawings" config:type="boolean">true</config:config-item>
   <config:config-item config:name="PrinterIndependentLayout" config:type="string">disabled</config:config-item>
   <config:config-item config:name="TabAtLeftIndentForParagraphsInList" config:type="boolean">false</config:config-item>
   <config:config-item config:name="PrintBlackFonts" config:type="boolean">false</config:config-item>
   <config:config-item config:name="UpdateFromTemplate" config:type="boolean">true</config:config-item>
  </config:config-item-set>
 </office:settings>
</office:document-settings>
'''
    _STYLES_XML = '''<?xml version="1.0" encoding="UTF-8"?>

<office:document-styles xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0" xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" xmlns:number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0" xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0" xmlns:chart="urn:oasis:names:tc:opendocument:xmlns:chart:1.0" xmlns:dr3d="urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0" xmlns:math="http://www.w3.org/1998/Math/MathML" xmlns:form="urn:oasis:names:tc:opendocument:xmlns:form:1.0" xmlns:script="urn:oasis:names:tc:opendocument:xmlns:script:1.0" xmlns:ooo="http://openoffice.org/2004/office" xmlns:ooow="http://openoffice.org/2004/writer" xmlns:oooc="http://openoffice.org/2004/calc" xmlns:dom="http://www.w3.org/2001/xml-events" xmlns:rpt="http://openoffice.org/2005/report" xmlns:of="urn:oasis:names:tc:opendocument:xmlns:of:1.2" xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns:grddl="http://www.w3.org/2003/g/data-view#" xmlns:tableooo="http://openoffice.org/2009/table" office:version="1.2">
 <office:font-face-decls>
  <style:font-face style:name="StarSymbol" svg:font-family="StarSymbol" style:font-charset="x-symbol"/>
  <style:font-face style:name="Segoe UI1" svg:font-family="&apos;Segoe UI&apos;" style:font-family-generic="swiss"/>
  <style:font-face style:name="Courier New" svg:font-family="&apos;Courier New&apos;" style:font-adornments="Standard" style:font-family-generic="modern" style:font-pitch="fixed"/>
  <style:font-face style:name="Courier Prime" svg:font-family="&apos;Courier Prime&apos;, &apos;Courier New&apos;" style:font-adornments="Standard" style:font-family-generic="modern" style:font-pitch="fixed"/>
  <style:font-face style:name="Cumberland" svg:font-family="Cumberland" style:font-family-generic="modern" style:font-pitch="fixed"/>
  <style:font-face style:name="Courier New1" svg:font-family="&apos;Courier New&apos;" style:font-family-generic="roman" style:font-pitch="fixed"/>
  <style:font-face style:name="Segoe UI" svg:font-family="&apos;Segoe UI&apos;" style:font-family-generic="roman" style:font-pitch="variable"/>
  <style:font-face style:name="ITC Officina Sans Book" svg:font-family="&apos;ITC Officina Sans Book&apos;" style:font-family-generic="swiss" style:font-pitch="variable"/>
 </office:font-face-decls>
 <office:styles>
  <style:default-style style:family="graphic">
   <style:graphic-properties fo:wrap-option="no-wrap" draw:shadow-offset-x="0.3cm" draw:shadow-offset-y="0.3cm" draw:start-line-spacing-horizontal="0.283cm" draw:start-line-spacing-vertical="0.283cm" draw:end-line-spacing-horizontal="0.283cm" draw:end-line-spacing-vertical="0.283cm" style:flow-with-text="true"/>
   <style:paragraph-properties style:text-autospace="ideograph-alpha" style:line-break="strict" style:writing-mode="lr-tb" style:font-independent-line-spacing="false">
    <style:tab-stops/>
   </style:paragraph-properties>
   <style:text-properties fo:color="#000000" fo:font-size="10pt" fo:language="de" fo:country="DE" style:letter-kerning="true" style:font-size-asian="10pt" style:language-asian="zxx" style:country-asian="none" style:font-size-complex="1pt" style:language-complex="zxx" style:country-complex="none"/>
  </style:default-style>
  <style:default-style style:family="paragraph">
   <style:paragraph-properties fo:hyphenation-ladder-count="no-limit" style:text-autospace="ideograph-alpha" style:punctuation-wrap="hanging" style:line-break="strict" style:tab-stop-distance="1.251cm" style:writing-mode="lr-tb"/>
   <style:text-properties fo:color="#000000" style:font-name="Segoe UI" fo:font-size="10pt" fo:language="de" fo:country="DE" style:letter-kerning="true" style:font-name-asian="Segoe UI" style:font-size-asian="10pt" style:language-asian="zxx" style:country-asian="none" style:font-name-complex="Segoe UI" style:font-size-complex="1pt" style:language-complex="zxx" style:country-complex="none" fo:hyphenate="false" fo:hyphenation-remain-char-count="2" fo:hyphenation-push-char-count="2"/>
  </style:default-style>
  <style:default-style style:family="table">
   <style:table-properties table:border-model="separating"/>
  </style:default-style>
  <style:default-style style:family="table-row">
   <style:table-row-properties fo:keep-together="always"/>
  </style:default-style>
  <style:style style:name="Standard" style:family="paragraph" style:class="text" style:master-page-name="">
   <style:paragraph-properties fo:line-height="0.73cm" style:page-number="auto"/>
   <style:text-properties style:font-name="Courier Prime" fo:font-size="12pt" fo:font-weight="normal"/>
  </style:style>
  <style:style style:name="Heading" style:family="paragraph" style:parent-style-name="Standard" style:next-style-name="Text_20_body" style:class="text" style:master-page-name="">
   <style:paragraph-properties fo:line-height="0.73cm" fo:text-align="center" style:justify-single-word="false" style:page-number="auto" fo:keep-with-next="always">
    <style:tab-stops/>
   </style:paragraph-properties>
  </style:style>
  <style:style style:name="Text_20_body" style:display-name="Text body" style:family="paragraph" style:parent-style-name="Standard" style:next-style-name="First_20_line_20_indent" style:class="text" style:master-page-name="">
   <style:paragraph-properties style:page-number="auto">
    <style:tab-stops/>
   </style:paragraph-properties>
  </style:style>
  <style:style style:name="List" style:family="paragraph" style:parent-style-name="Text_20_body" style:class="list">
   <style:text-properties fo:font-weight="normal"/>
  </style:style>
  <style:style style:name="Caption" style:family="paragraph" style:parent-style-name="Standard" style:class="extra">
   <style:paragraph-properties fo:margin-top="0.212cm" fo:margin-bottom="0.212cm"/>
  </style:style>
  <style:style style:name="Table" style:family="paragraph" style:parent-style-name="Caption" style:class="extra"/>
  <style:style style:name="Index" style:family="paragraph" style:parent-style-name="Standard" style:class="index"/>
  <style:style style:name="Heading_20_1" style:display-name="Heading 1" style:family="paragraph" style:parent-style-name="Heading" style:next-style-name="Text_20_body" style:default-outline-level="1" style:list-style-name="" style:class="text" style:master-page-name="">
   <style:paragraph-properties fo:margin-top="0.73cm" fo:margin-bottom="0.73cm" style:page-number="auto">
    <style:tab-stops/>
   </style:paragraph-properties>
   <style:text-properties fo:text-transform="uppercase" fo:font-weight="bold"/>
  </style:style>
  <style:style style:name="Heading_20_2" style:display-name="Heading 2" style:family="paragraph" style:parent-style-name="Heading" style:next-style-name="Text_20_body" style:default-outline-level="2" style:list-style-name="" style:class="text" style:master-page-name="">
   <style:paragraph-properties fo:margin-top="0.73cm" fo:margin-bottom="0.73cm" style:page-number="auto"/>
   <style:text-properties fo:font-weight="bold"/>
  </style:style>
  <style:style style:name="Heading_20_3" style:display-name="Heading 3" style:family="paragraph" style:parent-style-name="Heading" style:next-style-name="Text_20_body" style:default-outline-level="3" style:class="text" style:master-page-name="">
   <style:paragraph-properties fo:margin-top="0.73cm" fo:margin-bottom="0.73cm" style:page-number="auto"/>
   <style:text-properties fo:font-style="italic"/>
  </style:style>
  <style:style style:name="Heading_20_4" style:display-name="Heading 4" style:family="paragraph" style:parent-style-name="Heading" style:next-style-name="Text_20_body" style:default-outline-level="" style:list-style-name="" style:class="text" style:master-page-name="">
   <style:paragraph-properties fo:margin-top="0.73cm" fo:margin-bottom="0.73cm" style:page-number="auto"/>
  </style:style>
  <style:style style:name="Heading_20_5" style:display-name="Heading 5" style:family="paragraph" style:parent-style-name="Heading" style:next-style-name="Text_20_body" style:default-outline-level="5" style:list-style-name="" style:class="text"/>
  <style:style style:name="Heading_20_6" style:display-name="Heading 6" style:family="paragraph" style:parent-style-name="Heading" style:next-style-name="Text_20_body" style:default-outline-level="6" style:list-style-name="" style:class="text"/>
  <style:style style:name="Quotations" style:family="paragraph" style:parent-style-name="Text_20_body" style:class="html" style:master-page-name="">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="0.499cm" fo:margin-right="0.499cm" fo:margin-top="0cm" fo:margin-bottom="0.499cm" fo:text-indent="0cm" style:auto-text-indent="false" style:page-number="auto"/>
  </style:style>
  <style:style style:name="Preformatted_20_Text" style:display-name="Preformatted Text" style:family="paragraph" style:parent-style-name="Standard" style:class="html">
   <style:paragraph-properties fo:margin-top="0cm" fo:margin-bottom="0cm"/>
  </style:style>
  <style:style style:name="Table_20_Contents" style:display-name="Table Contents" style:family="paragraph" style:parent-style-name="Text_20_body" style:class="extra"/>
  <style:style style:name="Table_20_Heading" style:display-name="Table Heading" style:family="paragraph" style:parent-style-name="Table_20_Contents" style:class="extra">
   <style:paragraph-properties fo:text-align="center" style:justify-single-word="false"/>
   <style:text-properties fo:font-style="italic" fo:font-weight="bold"/>
  </style:style>
  <style:style style:name="Footnote" style:family="paragraph" style:parent-style-name="Standard" style:class="extra">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="0.499cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="-0.499cm" style:auto-text-indent="false"/>
   <style:text-properties fo:font-size="10pt"/>
  </style:style>
  <style:style style:name="Footer" style:family="paragraph" style:parent-style-name="Standard" style:class="extra" style:master-page-name="">
   <style:paragraph-properties fo:text-align="center" style:justify-single-word="false" style:page-number="auto" text:number-lines="false" text:line-number="0">
    <style:tab-stops>
     <style:tab-stop style:position="8.5cm" style:type="center"/>
     <style:tab-stop style:position="17.002cm" style:type="right"/>
    </style:tab-stops>
   </style:paragraph-properties>
   <style:text-properties fo:font-size="11pt"/>
  </style:style>
  <style:style style:name="Horizontal_20_Line" style:display-name="Horizontal Line" style:family="paragraph" style:parent-style-name="Standard" style:next-style-name="Text_20_body" style:class="html">
   <style:paragraph-properties fo:margin-top="0cm" fo:margin-bottom="0.499cm" style:border-line-width-bottom="0.002cm 0.035cm 0.002cm" fo:padding="0cm" fo:border-left="none" fo:border-right="none" fo:border-top="none" fo:border-bottom="0.039cm double #808080" text:number-lines="false" text:line-number="0"/>
   <style:text-properties fo:font-size="6pt"/>
  </style:style>
  <style:style style:name="First_20_line_20_indent" style:display-name="First line indent" style:family="paragraph" style:parent-style-name="Text_20_body" style:class="text" style:master-page-name="">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="0cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="0.499cm" style:auto-text-indent="false" style:page-number="auto"/>
  </style:style>
  <style:style style:name="Heading_20_7" style:display-name="Heading 7" style:family="paragraph" style:parent-style-name="Heading" style:next-style-name="Text_20_body" style:default-outline-level="7" style:list-style-name="" style:class="text"/>
  <style:style style:name="Heading_20_8" style:display-name="Heading 8" style:family="paragraph" style:parent-style-name="Heading" style:next-style-name="Text_20_body" style:default-outline-level="8" style:list-style-name="" style:class="text"/>
  <style:style style:name="Heading_20_9" style:display-name="Heading 9" style:family="paragraph" style:parent-style-name="Heading" style:next-style-name="Text_20_body" style:default-outline-level="9" style:list-style-name="" style:class="text"/>
  <style:style style:name="Heading_20_10" style:display-name="Heading 10" style:family="paragraph" style:parent-style-name="Heading" style:next-style-name="Text_20_body" style:default-outline-level="10" style:list-style-name="" style:class="text">
   <style:text-properties fo:font-size="75%" fo:font-weight="bold"/>
  </style:style>
  <style:style style:name="Title" style:family="paragraph" style:parent-style-name="Standard" style:next-style-name="Subtitle" style:class="chapter" style:master-page-name="">
   <style:paragraph-properties fo:margin-top="0cm" fo:margin-bottom="0.73cm" fo:text-align="center" style:justify-single-word="false" style:page-number="auto" fo:background-color="transparent" fo:padding="0cm" fo:border="none" text:number-lines="false" text:line-number="0">
    <style:tab-stops/>
    <style:background-image/>
   </style:paragraph-properties>
   <style:text-properties fo:text-transform="uppercase" fo:letter-spacing="normal" fo:font-weight="normal" style:letter-kerning="false"/>
  </style:style>
  <style:style style:name="Subtitle" style:family="paragraph" style:parent-style-name="Title" style:class="chapter" style:master-page-name="">
   <style:paragraph-properties fo:margin-top="0cm" fo:margin-bottom="0.73cm" style:page-number="auto"/>
   <style:text-properties fo:font-variant="normal" fo:text-transform="none" fo:letter-spacing="normal"/>
  </style:style>
  <style:style style:name="Hanging_20_indent" style:display-name="Hanging indent" style:family="paragraph" style:parent-style-name="Text_20_body" style:class="text">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="1cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="-0.499cm" style:auto-text-indent="false">
    <style:tab-stops>
     <style:tab-stop style:position="0cm"/>
    </style:tab-stops>
   </style:paragraph-properties>
  </style:style>
  <style:style style:name="Text_20_body_20_indent" style:display-name="Text body indent" style:family="paragraph" style:parent-style-name="Text_20_body" style:class="text">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="0.499cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="0cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="Salutation" style:family="paragraph" style:parent-style-name="Standard" style:class="text"/>
  <style:style style:name="Signature" style:family="paragraph" style:parent-style-name="Standard" style:class="text"/>
  <style:style style:name="List_20_Indent" style:display-name="List Indent" style:family="paragraph" style:parent-style-name="Text_20_body" style:class="text">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="5.001cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="-4.5cm" style:auto-text-indent="false">
    <style:tab-stops>
     <style:tab-stop style:position="0cm"/>
    </style:tab-stops>
   </style:paragraph-properties>
  </style:style>
  <style:style style:name="Marginalia" style:family="paragraph" style:parent-style-name="Text_20_body" style:class="text">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="4.001cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="0cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="Numbering_20_1_20_Start" style:display-name="Numbering 1 Start" style:family="paragraph" style:parent-style-name="List" style:class="list">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="0.499cm" fo:margin-right="0cm" fo:margin-top="0.423cm" fo:margin-bottom="0.212cm" fo:text-indent="-0.499cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="Numbering_20_1" style:display-name="Numbering 1" style:family="paragraph" style:parent-style-name="List" style:class="list">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="0.499cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0.212cm" fo:text-indent="-0.499cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="Numbering_20_1_20_End" style:display-name="Numbering 1 End" style:family="paragraph" style:parent-style-name="List" style:class="list">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="0.499cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0.423cm" fo:text-indent="-0.499cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="Numbering_20_1_20_Cont." style:display-name="Numbering 1 Cont." style:family="paragraph" style:parent-style-name="List" style:class="list">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="0.499cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0.212cm" fo:text-indent="0cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="Numbering_20_2_20_Start" style:display-name="Numbering 2 Start" style:family="paragraph" style:parent-style-name="List" style:class="list">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="0.998cm" fo:margin-right="0cm" fo:margin-top="0.423cm" fo:margin-bottom="0.212cm" fo:text-indent="-0.499cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="Numbering_20_2" style:display-name="Numbering 2" style:family="paragraph" style:parent-style-name="List" style:class="list">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="0.998cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0.212cm" fo:text-indent="-0.499cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="Numbering_20_2_20_End" style:display-name="Numbering 2 End" style:family="paragraph" style:parent-style-name="List" style:class="list">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="0.998cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0.423cm" fo:text-indent="-0.499cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="Numbering_20_2_20_Cont." style:display-name="Numbering 2 Cont." style:family="paragraph" style:parent-style-name="List" style:class="list">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="0.998cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0.212cm" fo:text-indent="0cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="Numbering_20_3_20_Start" style:display-name="Numbering 3 Start" style:family="paragraph" style:parent-style-name="List" style:class="list">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="1.498cm" fo:margin-right="0cm" fo:margin-top="0.423cm" fo:margin-bottom="0.212cm" fo:text-indent="-0.499cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="Numbering_20_3" style:display-name="Numbering 3" style:family="paragraph" style:parent-style-name="List" style:class="list">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="1.498cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0.212cm" fo:text-indent="-0.499cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="Numbering_20_3_20_End" style:display-name="Numbering 3 End" style:family="paragraph" style:parent-style-name="List" style:class="list">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="1.498cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0.423cm" fo:text-indent="-0.499cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="Numbering_20_3_20_Cont." style:display-name="Numbering 3 Cont." style:family="paragraph" style:parent-style-name="List" style:class="list">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="1.498cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0.212cm" fo:text-indent="0cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="Numbering_20_4_20_Start" style:display-name="Numbering 4 Start" style:family="paragraph" style:parent-style-name="List" style:class="list">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="1.997cm" fo:margin-right="0cm" fo:margin-top="0.423cm" fo:margin-bottom="0.212cm" fo:text-indent="-0.499cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="Numbering_20_4" style:display-name="Numbering 4" style:family="paragraph" style:parent-style-name="List" style:class="list">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="1.997cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0.212cm" fo:text-indent="-0.499cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="Numbering_20_4_20_End" style:display-name="Numbering 4 End" style:family="paragraph" style:parent-style-name="List" style:class="list">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="1.997cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0.423cm" fo:text-indent="-0.499cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="Numbering_20_4_20_Cont." style:display-name="Numbering 4 Cont." style:family="paragraph" style:parent-style-name="List" style:class="list">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="1.997cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0.212cm" fo:text-indent="0cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="Numbering_20_5_20_Start" style:display-name="Numbering 5 Start" style:family="paragraph" style:parent-style-name="List" style:class="list">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="2.496cm" fo:margin-right="0cm" fo:margin-top="0.423cm" fo:margin-bottom="0.212cm" fo:text-indent="-0.499cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="Numbering_20_5" style:display-name="Numbering 5" style:family="paragraph" style:parent-style-name="List" style:class="list">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="2.496cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0.212cm" fo:text-indent="-0.499cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="Numbering_20_5_20_End" style:display-name="Numbering 5 End" style:family="paragraph" style:parent-style-name="List" style:class="list">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="2.496cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0.423cm" fo:text-indent="-0.499cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="Numbering_20_5_20_Cont." style:display-name="Numbering 5 Cont." style:family="paragraph" style:parent-style-name="List" style:class="list">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="2.496cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0.212cm" fo:text-indent="0cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="List_20_1_20_Start" style:display-name="List 1 Start" style:family="paragraph" style:parent-style-name="List" style:class="list">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="0.499cm" fo:margin-right="0cm" fo:margin-top="0.423cm" fo:margin-bottom="0.212cm" fo:text-indent="-0.499cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="List_20_1" style:display-name="List 1" style:family="paragraph" style:parent-style-name="List" style:class="list">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="0.499cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0.212cm" fo:text-indent="-0.499cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="List_20_1_20_End" style:display-name="List 1 End" style:family="paragraph" style:parent-style-name="List" style:class="list">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="0.499cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0.423cm" fo:text-indent="-0.499cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="List_20_1_20_Cont." style:display-name="List 1 Cont." style:family="paragraph" style:parent-style-name="List" style:class="list">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="0.499cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0.212cm" fo:text-indent="0cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="List_20_2_20_Start" style:display-name="List 2 Start" style:family="paragraph" style:parent-style-name="List" style:class="list">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="0.998cm" fo:margin-right="0cm" fo:margin-top="0.423cm" fo:margin-bottom="0.212cm" fo:text-indent="-0.499cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="List_20_2" style:display-name="List 2" style:family="paragraph" style:parent-style-name="List" style:class="list">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="0.998cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0.212cm" fo:text-indent="-0.499cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="List_20_2_20_End" style:display-name="List 2 End" style:family="paragraph" style:parent-style-name="List" style:class="list">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="0.998cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0.423cm" fo:text-indent="-0.499cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="List_20_2_20_Cont." style:display-name="List 2 Cont." style:family="paragraph" style:parent-style-name="List" style:class="list">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="0.998cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0.212cm" fo:text-indent="0cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="List_20_3_20_Start" style:display-name="List 3 Start" style:family="paragraph" style:parent-style-name="List" style:class="list">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="1.498cm" fo:margin-right="0cm" fo:margin-top="0.423cm" fo:margin-bottom="0.212cm" fo:text-indent="-0.499cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="List_20_3" style:display-name="List 3" style:family="paragraph" style:parent-style-name="List" style:class="list">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="1.498cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0.212cm" fo:text-indent="-0.499cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="List_20_3_20_End" style:display-name="List 3 End" style:family="paragraph" style:parent-style-name="List" style:class="list">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="1.498cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0.423cm" fo:text-indent="-0.499cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="List_20_3_20_Cont." style:display-name="List 3 Cont." style:family="paragraph" style:parent-style-name="List" style:class="list">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="1.498cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0.212cm" fo:text-indent="0cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="List_20_4_20_Start" style:display-name="List 4 Start" style:family="paragraph" style:parent-style-name="List" style:class="list">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="1.997cm" fo:margin-right="0cm" fo:margin-top="0.423cm" fo:margin-bottom="0.212cm" fo:text-indent="-0.499cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="List_20_4" style:display-name="List 4" style:family="paragraph" style:parent-style-name="List" style:class="list">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="1.997cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0.212cm" fo:text-indent="-0.499cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="List_20_4_20_End" style:display-name="List 4 End" style:family="paragraph" style:parent-style-name="List" style:class="list">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="1.997cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0.423cm" fo:text-indent="-0.499cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="List_20_4_20_Cont." style:display-name="List 4 Cont." style:family="paragraph" style:parent-style-name="List" style:class="list">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="1.997cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0.212cm" fo:text-indent="0cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="List_20_5_20_Start" style:display-name="List 5 Start" style:family="paragraph" style:parent-style-name="List" style:class="list">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="2.496cm" fo:margin-right="0cm" fo:margin-top="0.423cm" fo:margin-bottom="0.212cm" fo:text-indent="-0.499cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="List_20_5" style:display-name="List 5" style:family="paragraph" style:parent-style-name="List" style:class="list">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="2.496cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0.212cm" fo:text-indent="-0.499cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="List_20_5_20_End" style:display-name="List 5 End" style:family="paragraph" style:parent-style-name="List" style:class="list">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="2.496cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0.423cm" fo:text-indent="-0.499cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="List_20_5_20_Cont." style:display-name="List 5 Cont." style:family="paragraph" style:parent-style-name="List" style:class="list">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="2.496cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0.212cm" fo:text-indent="0cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="Header" style:family="paragraph" style:parent-style-name="Standard" style:class="extra" style:master-page-name="">
   <style:paragraph-properties fo:text-align="end" style:justify-single-word="false" style:page-number="auto" fo:padding="0.049cm" fo:border-left="none" fo:border-right="none" fo:border-top="none" fo:border-bottom="0.002cm solid #000000" style:shadow="none">
    <style:tab-stops>
     <style:tab-stop style:position="8.5cm" style:type="center"/>
     <style:tab-stop style:position="17.002cm" style:type="right"/>
    </style:tab-stops>
   </style:paragraph-properties>
   <style:text-properties fo:font-variant="normal" fo:text-transform="none" fo:font-style="italic"/>
  </style:style>
  <style:style style:name="Header_20_left" style:display-name="Header left" style:family="paragraph" style:parent-style-name="Standard" style:class="extra">
   <style:paragraph-properties>
    <style:tab-stops>
     <style:tab-stop style:position="8.5cm" style:type="center"/>
     <style:tab-stop style:position="17.002cm" style:type="right"/>
    </style:tab-stops>
   </style:paragraph-properties>
  </style:style>
  <style:style style:name="Header_20_right" style:display-name="Header right" style:family="paragraph" style:parent-style-name="Standard" style:class="extra">
   <style:paragraph-properties>
    <style:tab-stops>
     <style:tab-stop style:position="8.5cm" style:type="center"/>
     <style:tab-stop style:position="17.002cm" style:type="right"/>
    </style:tab-stops>
   </style:paragraph-properties>
  </style:style>
  <style:style style:name="Footer_20_left" style:display-name="Footer left" style:family="paragraph" style:parent-style-name="Standard" style:class="extra">
   <style:paragraph-properties>
    <style:tab-stops>
     <style:tab-stop style:position="8.5cm" style:type="center"/>
     <style:tab-stop style:position="17.002cm" style:type="right"/>
    </style:tab-stops>
   </style:paragraph-properties>
  </style:style>
  <style:style style:name="Footer_20_right" style:display-name="Footer right" style:family="paragraph" style:parent-style-name="Standard" style:class="extra">
   <style:paragraph-properties>
    <style:tab-stops>
     <style:tab-stop style:position="8.5cm" style:type="center"/>
     <style:tab-stop style:position="17.002cm" style:type="right"/>
    </style:tab-stops>
   </style:paragraph-properties>
  </style:style>
  <style:style style:name="Illustration" style:family="paragraph" style:parent-style-name="Caption" style:class="extra"/>
  <style:style style:name="Text" style:family="paragraph" style:parent-style-name="Caption" style:class="extra" style:master-page-name="">
   <style:paragraph-properties fo:margin-top="0.21cm" fo:margin-bottom="0.21cm" style:page-number="auto"/>
  </style:style>
  <style:style style:name="Frame_20_contents" style:display-name="Frame contents" style:family="paragraph" style:parent-style-name="Text_20_body" style:class="extra"/>
  <style:style style:name="Addressee" style:family="paragraph" style:parent-style-name="Standard" style:class="extra">
   <style:paragraph-properties fo:margin-top="0cm" fo:margin-bottom="0.106cm"/>
  </style:style>
  <style:style style:name="Sender" style:family="paragraph" style:parent-style-name="Standard" style:class="extra">
   <style:paragraph-properties fo:margin-top="0cm" fo:margin-bottom="0.106cm" fo:line-height="100%" text:number-lines="false" text:line-number="0"/>
  </style:style>
  <style:style style:name="Endnote" style:family="paragraph" style:parent-style-name="Standard" style:class="extra">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="0.499cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="-0.499cm" style:auto-text-indent="false" text:number-lines="false" text:line-number="0"/>
   <style:text-properties fo:font-size="10pt"/>
  </style:style>
  <style:style style:name="Drawing" style:family="paragraph" style:parent-style-name="Caption" style:class="extra"/>
  <style:style style:name="Index_20_Heading" style:display-name="Index Heading" style:family="paragraph" style:parent-style-name="Heading" style:class="index">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="0cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="0cm" style:auto-text-indent="false"/>
   <style:text-properties fo:font-size="16pt" fo:font-weight="bold"/>
  </style:style>
  <style:style style:name="Index_20_1" style:display-name="Index 1" style:family="paragraph" style:parent-style-name="Index" style:class="index">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="0.499cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="0cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="Index_20_2" style:display-name="Index 2" style:family="paragraph" style:parent-style-name="Index" style:class="index">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="0.499cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="0cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="Index_20_3" style:display-name="Index 3" style:family="paragraph" style:parent-style-name="Index" style:class="index">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="0cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="0cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="Index_20_Separator" style:display-name="Index Separator" style:family="paragraph" style:parent-style-name="Index" style:class="index">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="0cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="0cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="Contents_20_Heading" style:display-name="Contents Heading" style:family="paragraph" style:parent-style-name="Heading" style:class="index">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="0cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="0cm" style:auto-text-indent="false"/>
   <style:text-properties fo:font-size="16pt" fo:font-weight="bold"/>
  </style:style>
  <style:style style:name="Contents_20_1" style:display-name="Contents 1" style:family="paragraph" style:parent-style-name="Index" style:class="index">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="0cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="0cm" style:auto-text-indent="false">
    <style:tab-stops>
     <style:tab-stop style:position="17.002cm" style:type="right" style:leader-style="dotted" style:leader-text="."/>
    </style:tab-stops>
   </style:paragraph-properties>
  </style:style>
  <style:style style:name="Contents_20_2" style:display-name="Contents 2" style:family="paragraph" style:parent-style-name="Index" style:class="index">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="0.499cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="0cm" style:auto-text-indent="false">
    <style:tab-stops>
     <style:tab-stop style:position="16.503cm" style:type="right" style:leader-style="dotted" style:leader-text="."/>
    </style:tab-stops>
   </style:paragraph-properties>
  </style:style>
  <style:style style:name="Contents_20_3" style:display-name="Contents 3" style:family="paragraph" style:parent-style-name="Index" style:class="index">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="0.998cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="0cm" style:auto-text-indent="false">
    <style:tab-stops>
     <style:tab-stop style:position="16.004cm" style:type="right" style:leader-style="dotted" style:leader-text="."/>
    </style:tab-stops>
   </style:paragraph-properties>
  </style:style>
  <style:style style:name="Contents_20_4" style:display-name="Contents 4" style:family="paragraph" style:parent-style-name="Index" style:class="index">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="1.498cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="0cm" style:auto-text-indent="false">
    <style:tab-stops>
     <style:tab-stop style:position="15.505cm" style:type="right" style:leader-style="dotted" style:leader-text="."/>
    </style:tab-stops>
   </style:paragraph-properties>
  </style:style>
  <style:style style:name="Contents_20_5" style:display-name="Contents 5" style:family="paragraph" style:parent-style-name="Index" style:class="index">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="1.997cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="0cm" style:auto-text-indent="false">
    <style:tab-stops>
     <style:tab-stop style:position="15.005cm" style:type="right" style:leader-style="dotted" style:leader-text="."/>
    </style:tab-stops>
   </style:paragraph-properties>
  </style:style>
  <style:style style:name="User_20_Index_20_Heading" style:display-name="User Index Heading" style:family="paragraph" style:parent-style-name="Heading" style:class="index">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="0cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="0cm" style:auto-text-indent="false"/>
   <style:text-properties fo:font-size="16pt" fo:font-weight="bold"/>
  </style:style>
  <style:style style:name="User_20_Index_20_1" style:display-name="User Index 1" style:family="paragraph" style:parent-style-name="Index" style:class="index">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="0cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="0cm" style:auto-text-indent="false">
    <style:tab-stops>
     <style:tab-stop style:position="17.002cm" style:type="right" style:leader-style="dotted" style:leader-text="."/>
    </style:tab-stops>
   </style:paragraph-properties>
  </style:style>
  <style:style style:name="User_20_Index_20_2" style:display-name="User Index 2" style:family="paragraph" style:parent-style-name="Index" style:class="index">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="0.499cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="0cm" style:auto-text-indent="false">
    <style:tab-stops>
     <style:tab-stop style:position="16.503cm" style:type="right" style:leader-style="dotted" style:leader-text="."/>
    </style:tab-stops>
   </style:paragraph-properties>
  </style:style>
  <style:style style:name="User_20_Index_20_3" style:display-name="User Index 3" style:family="paragraph" style:parent-style-name="Index" style:class="index">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="0.998cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="0cm" style:auto-text-indent="false">
    <style:tab-stops>
     <style:tab-stop style:position="16.004cm" style:type="right" style:leader-style="dotted" style:leader-text="."/>
    </style:tab-stops>
   </style:paragraph-properties>
  </style:style>
  <style:style style:name="User_20_Index_20_4" style:display-name="User Index 4" style:family="paragraph" style:parent-style-name="Index" style:class="index">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="1.498cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="0cm" style:auto-text-indent="false">
    <style:tab-stops>
     <style:tab-stop style:position="15.505cm" style:type="right" style:leader-style="dotted" style:leader-text="."/>
    </style:tab-stops>
   </style:paragraph-properties>
  </style:style>
  <style:style style:name="User_20_Index_20_5" style:display-name="User Index 5" style:family="paragraph" style:parent-style-name="Index" style:class="index">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="1.997cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="0cm" style:auto-text-indent="false">
    <style:tab-stops>
     <style:tab-stop style:position="15.005cm" style:type="right" style:leader-style="dotted" style:leader-text="."/>
    </style:tab-stops>
   </style:paragraph-properties>
  </style:style>
  <style:style style:name="Contents_20_6" style:display-name="Contents 6" style:family="paragraph" style:parent-style-name="Index" style:class="index">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="2.496cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="0cm" style:auto-text-indent="false">
    <style:tab-stops>
     <style:tab-stop style:position="11.105cm" style:type="right" style:leader-style="dotted" style:leader-text="."/>
    </style:tab-stops>
   </style:paragraph-properties>
  </style:style>
  <style:style style:name="Contents_20_7" style:display-name="Contents 7" style:family="paragraph" style:parent-style-name="Index" style:class="index">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="2.995cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="0cm" style:auto-text-indent="false">
    <style:tab-stops>
     <style:tab-stop style:position="10.606cm" style:type="right" style:leader-style="dotted" style:leader-text="."/>
    </style:tab-stops>
   </style:paragraph-properties>
  </style:style>
  <style:style style:name="Contents_20_8" style:display-name="Contents 8" style:family="paragraph" style:parent-style-name="Index" style:class="index">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="3.494cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="0cm" style:auto-text-indent="false">
    <style:tab-stops>
     <style:tab-stop style:position="10.107cm" style:type="right" style:leader-style="dotted" style:leader-text="."/>
    </style:tab-stops>
   </style:paragraph-properties>
  </style:style>
  <style:style style:name="Contents_20_9" style:display-name="Contents 9" style:family="paragraph" style:parent-style-name="Index" style:class="index">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="3.993cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="0cm" style:auto-text-indent="false">
    <style:tab-stops>
     <style:tab-stop style:position="9.608cm" style:type="right" style:leader-style="dotted" style:leader-text="."/>
    </style:tab-stops>
   </style:paragraph-properties>
  </style:style>
  <style:style style:name="Contents_20_10" style:display-name="Contents 10" style:family="paragraph" style:parent-style-name="Index" style:class="index">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="4.493cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="0cm" style:auto-text-indent="false">
    <style:tab-stops>
     <style:tab-stop style:position="9.109cm" style:type="right" style:leader-style="dotted" style:leader-text="."/>
    </style:tab-stops>
   </style:paragraph-properties>
  </style:style>
  <style:style style:name="Illustration_20_Index_20_Heading" style:display-name="Illustration Index Heading" style:family="paragraph" style:parent-style-name="Heading" style:class="index">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="0cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="0cm" style:auto-text-indent="false" text:number-lines="false" text:line-number="0"/>
   <style:text-properties fo:font-size="16pt" fo:font-weight="bold"/>
  </style:style>
  <style:style style:name="Illustration_20_Index_20_1" style:display-name="Illustration Index 1" style:family="paragraph" style:parent-style-name="Index" style:class="index">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="0cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="0cm" style:auto-text-indent="false">
    <style:tab-stops>
     <style:tab-stop style:position="13.601cm" style:type="right" style:leader-style="dotted" style:leader-text="."/>
    </style:tab-stops>
   </style:paragraph-properties>
  </style:style>
  <style:style style:name="Object_20_index_20_heading" style:display-name="Object index heading" style:family="paragraph" style:parent-style-name="Heading" style:class="index">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="0cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="0cm" style:auto-text-indent="false" text:number-lines="false" text:line-number="0"/>
   <style:text-properties fo:font-size="16pt" fo:font-weight="bold"/>
  </style:style>
  <style:style style:name="Object_20_index_20_1" style:display-name="Object index 1" style:family="paragraph" style:parent-style-name="Index" style:class="index">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="0cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="0cm" style:auto-text-indent="false">
    <style:tab-stops>
     <style:tab-stop style:position="13.601cm" style:type="right" style:leader-style="dotted" style:leader-text="."/>
    </style:tab-stops>
   </style:paragraph-properties>
  </style:style>
  <style:style style:name="Table_20_index_20_heading" style:display-name="Table index heading" style:family="paragraph" style:parent-style-name="Heading" style:class="index">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="0cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="0cm" style:auto-text-indent="false" text:number-lines="false" text:line-number="0"/>
   <style:text-properties fo:font-size="16pt" fo:font-weight="bold"/>
  </style:style>
  <style:style style:name="Table_20_index_20_1" style:display-name="Table index 1" style:family="paragraph" style:parent-style-name="Index" style:class="index">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="0cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="0cm" style:auto-text-indent="false">
    <style:tab-stops>
     <style:tab-stop style:position="13.601cm" style:type="right" style:leader-style="dotted" style:leader-text="."/>
    </style:tab-stops>
   </style:paragraph-properties>
  </style:style>
  <style:style style:name="Bibliography_20_Heading" style:display-name="Bibliography Heading" style:family="paragraph" style:parent-style-name="Heading" style:class="index">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="0cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="0cm" style:auto-text-indent="false" text:number-lines="false" text:line-number="0"/>
   <style:text-properties fo:font-size="16pt" fo:font-weight="bold"/>
  </style:style>
  <style:style style:name="Bibliography_20_1" style:display-name="Bibliography 1" style:family="paragraph" style:parent-style-name="Index" style:class="index">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="0cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="0cm" style:auto-text-indent="false">
    <style:tab-stops>
     <style:tab-stop style:position="13.601cm" style:type="right" style:leader-style="dotted" style:leader-text="."/>
    </style:tab-stops>
   </style:paragraph-properties>
  </style:style>
  <style:style style:name="User_20_Index_20_6" style:display-name="User Index 6" style:family="paragraph" style:parent-style-name="Index" style:class="index">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="2.496cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="0cm" style:auto-text-indent="false">
    <style:tab-stops>
     <style:tab-stop style:position="11.105cm" style:type="right" style:leader-style="dotted" style:leader-text="."/>
    </style:tab-stops>
   </style:paragraph-properties>
  </style:style>
  <style:style style:name="User_20_Index_20_7" style:display-name="User Index 7" style:family="paragraph" style:parent-style-name="Index" style:class="index">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="2.995cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="0cm" style:auto-text-indent="false">
    <style:tab-stops>
     <style:tab-stop style:position="10.606cm" style:type="right" style:leader-style="dotted" style:leader-text="."/>
    </style:tab-stops>
   </style:paragraph-properties>
  </style:style>
  <style:style style:name="User_20_Index_20_8" style:display-name="User Index 8" style:family="paragraph" style:parent-style-name="Index" style:class="index">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="3.494cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="0cm" style:auto-text-indent="false">
    <style:tab-stops>
     <style:tab-stop style:position="10.107cm" style:type="right" style:leader-style="dotted" style:leader-text="."/>
    </style:tab-stops>
   </style:paragraph-properties>
  </style:style>
  <style:style style:name="User_20_Index_20_9" style:display-name="User Index 9" style:family="paragraph" style:parent-style-name="Index" style:class="index">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="3.993cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="0cm" style:auto-text-indent="false">
    <style:tab-stops>
     <style:tab-stop style:position="9.608cm" style:type="right" style:leader-style="dotted" style:leader-text="."/>
    </style:tab-stops>
   </style:paragraph-properties>
  </style:style>
  <style:style style:name="User_20_Index_20_10" style:display-name="User Index 10" style:family="paragraph" style:parent-style-name="Index" style:class="index">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="4.493cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="0cm" style:auto-text-indent="false">
    <style:tab-stops>
     <style:tab-stop style:position="9.109cm" style:type="right" style:leader-style="dotted" style:leader-text="."/>
    </style:tab-stops>
   </style:paragraph-properties>
  </style:style>
  <style:style style:name="List_20_Contents" style:display-name="List Contents" style:family="paragraph" style:parent-style-name="Standard" style:class="html">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="1cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="0cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="List_20_Heading" style:display-name="List Heading" style:family="paragraph" style:parent-style-name="Standard" style:next-style-name="List_20_Contents" style:class="html">
   <style:paragraph-properties fo:margin="100%" fo:margin-left="0cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:text-indent="0cm" style:auto-text-indent="false"/>
  </style:style>
  <style:style style:name="yWriter_20_mark" style:display-name="yWriter mark" style:family="paragraph" style:parent-style-name="Standard" style:next-style-name="Standard" style:class="text">
   <style:text-properties fo:color="#0000ff" fo:font-size="10pt"/>
  </style:style>
  <style:style style:name="yWriter_20_mark_20_unused" style:display-name="yWriter mark unused" style:family="paragraph" style:parent-style-name="Standard" style:next-style-name="Standard" style:class="text">
   <style:text-properties fo:color="#ff0000" fo:font-size="10pt"/>
  </style:style>
  <style:style style:name="yWriter_20_mark_20_info" style:display-name="yWriter mark info" style:family="paragraph" style:parent-style-name="Standard" style:next-style-name="Standard" style:class="text">
   <style:text-properties fo:color="#800000" fo:font-size="10pt"/>
  </style:style>
  <style:style style:name="Numbering_20_Symbols" style:display-name="Numbering Symbols" style:family="text"/>
  <style:style style:name="Bullet_20_Symbols" style:display-name="Bullet Symbols" style:family="text">
   <style:text-properties style:font-name="StarSymbol" fo:font-size="9pt"/>
  </style:style>
  <style:style style:name="Emphasis" style:family="text">
   <style:text-properties fo:font-style="italic" fo:background-color="transparent"/>
  </style:style>
  <style:style style:name="Strong_20_Emphasis" style:display-name="Strong Emphasis" style:family="text">
   <style:text-properties fo:text-transform="uppercase"/>
  </style:style>
  <style:style style:name="Citation" style:family="text">
   <style:text-properties fo:font-style="italic"/>
  </style:style>
  <style:style style:name="Teletype" style:family="text">
   <style:text-properties style:font-name="Cumberland" style:font-name-asian="Cumberland" style:font-name-complex="Cumberland"/>
  </style:style>
  <style:style style:name="Internet_20_link" style:display-name="Internet link" style:family="text">
   <style:text-properties fo:color="#000080" style:text-underline-style="solid" style:text-underline-width="auto" style:text-underline-color="font-color"/>
  </style:style>
  <style:style style:name="Footnote_20_Symbol" style:display-name="Footnote Symbol" style:family="text"/>
  <style:style style:name="Footnote_20_anchor" style:display-name="Footnote anchor" style:family="text">
   <style:text-properties style:text-position="super 58%"/>
  </style:style>
  <style:style style:name="Definition" style:family="text"/>
  <style:style style:name="Line_20_numbering" style:display-name="Line numbering" style:family="text">
   <style:text-properties style:font-name="Courier New" fo:font-size="8pt"/>
  </style:style>
  <style:style style:name="Page_20_Number" style:display-name="Page Number" style:family="text">
   <style:text-properties style:font-name="ITC Officina Sans Book" fo:font-size="7pt" fo:letter-spacing="0.071cm" fo:font-weight="bold"/>
  </style:style>
  <style:style style:name="Caption_20_characters" style:display-name="Caption characters" style:family="text"/>
  <style:style style:name="Drop_20_Caps" style:display-name="Drop Caps" style:family="text"/>
  <style:style style:name="Visited_20_Internet_20_Link" style:display-name="Visited Internet Link" style:family="text">
   <style:text-properties fo:color="#800000" style:text-underline-style="solid" style:text-underline-width="auto" style:text-underline-color="font-color"/>
  </style:style>
  <style:style style:name="Placeholder" style:family="text">
   <style:text-properties fo:font-variant="small-caps" fo:color="#008080" style:text-underline-style="dotted" style:text-underline-width="auto" style:text-underline-color="font-color"/>
  </style:style>
  <style:style style:name="Index_20_Link" style:display-name="Index Link" style:family="text"/>
  <style:style style:name="Endnote_20_Symbol" style:display-name="Endnote Symbol" style:family="text"/>
  <style:style style:name="Main_20_index_20_entry" style:display-name="Main index entry" style:family="text">
   <style:text-properties fo:font-weight="bold" style:font-weight-asian="bold" style:font-weight-complex="bold"/>
  </style:style>
  <style:style style:name="Endnote_20_anchor" style:display-name="Endnote anchor" style:family="text">
   <style:text-properties style:text-position="super 58%"/>
  </style:style>
  <style:style style:name="Rubies" style:family="text">
   <style:text-properties fo:font-size="6pt" style:font-size-asian="6pt" style:font-size-complex="6pt"/>
  </style:style>
  <style:style style:name="Source_20_Text" style:display-name="Source Text" style:family="text">
   <style:text-properties style:font-name="Cumberland" style:font-name-asian="Cumberland" style:font-name-complex="Cumberland"/>
  </style:style>
  <style:style style:name="Example" style:family="text">
   <style:text-properties style:font-name="Courier New1"/>
  </style:style>
  <style:style style:name="User_20_Entry" style:display-name="User Entry" style:family="text">
   <style:text-properties style:font-name="Cumberland" style:font-name-asian="Cumberland" style:font-name-complex="Cumberland"/>
  </style:style>
  <style:style style:name="Variable" style:family="text">
   <style:text-properties fo:font-style="italic" style:font-style-asian="italic" style:font-style-complex="italic"/>
  </style:style>
  <style:style style:name="Frame" style:family="graphic">
   <style:graphic-properties text:anchor-type="paragraph" svg:x="0cm" svg:y="0cm" style:wrap="parallel" style:number-wrapped-paragraphs="no-limit" style:wrap-contour="false" style:vertical-pos="top" style:vertical-rel="paragraph-content" style:horizontal-pos="center" style:horizontal-rel="paragraph-content"/>
  </style:style>
  <style:style style:name="Graphics" style:family="graphic">
   <style:graphic-properties text:anchor-type="paragraph" svg:x="0cm" svg:y="0cm" style:wrap="none" style:vertical-pos="top" style:vertical-rel="paragraph" style:horizontal-pos="center" style:horizontal-rel="paragraph"/>
  </style:style>
  <style:style style:name="OLE" style:family="graphic">
   <style:graphic-properties text:anchor-type="paragraph" svg:x="0cm" svg:y="0cm" style:wrap="none" style:vertical-pos="top" style:vertical-rel="paragraph" style:horizontal-pos="center" style:horizontal-rel="paragraph"/>
  </style:style>
  <style:style style:name="Formula" style:family="graphic">
   <style:graphic-properties text:anchor-type="as-char" svg:y="0cm" style:vertical-pos="top" style:vertical-rel="baseline"/>
  </style:style>
  <style:style style:name="Labels" style:family="graphic" style:auto-update="true">
   <style:graphic-properties text:anchor-type="as-char" svg:y="0cm" fo:margin-left="0.201cm" fo:margin-right="0.201cm" style:protect="size position" style:vertical-pos="top" style:vertical-rel="baseline"/>
  </style:style>
  <text:outline-style style:name="Outline">
   <text:outline-level-style text:level="1" style:num-format="">
    <style:list-level-properties text:min-label-distance="0.381cm"/>
   </text:outline-level-style>
   <text:outline-level-style text:level="2" style:num-format="">
    <style:list-level-properties text:min-label-distance="0.381cm"/>
   </text:outline-level-style>
   <text:outline-level-style text:level="3" style:num-format="">
    <style:list-level-properties text:min-label-distance="0.381cm"/>
   </text:outline-level-style>
   <text:outline-level-style text:level="4" style:num-format="">
    <style:list-level-properties text:min-label-distance="0.381cm"/>
   </text:outline-level-style>
   <text:outline-level-style text:level="5" style:num-format="">
    <style:list-level-properties text:min-label-distance="0.381cm"/>
   </text:outline-level-style>
   <text:outline-level-style text:level="6" style:num-format="">
    <style:list-level-properties text:min-label-distance="0.381cm"/>
   </text:outline-level-style>
   <text:outline-level-style text:level="7" style:num-format="">
    <style:list-level-properties text:min-label-distance="0.381cm"/>
   </text:outline-level-style>
   <text:outline-level-style text:level="8" style:num-format="">
    <style:list-level-properties text:min-label-distance="0.381cm"/>
   </text:outline-level-style>
   <text:outline-level-style text:level="9" style:num-format="">
    <style:list-level-properties text:min-label-distance="0.381cm"/>
   </text:outline-level-style>
   <text:outline-level-style text:level="10" style:num-format="">
    <style:list-level-properties text:min-label-distance="0.381cm"/>
   </text:outline-level-style>
  </text:outline-style>
  <text:list-style style:name="Numbering_20_1" style:display-name="Numbering 1">
   <text:list-level-style-number text:level="1" text:style-name="Numbering_20_Symbols" style:num-suffix="." style:num-format="1">
    <style:list-level-properties text:min-label-width="0.499cm"/>
   </text:list-level-style-number>
   <text:list-level-style-number text:level="2" text:style-name="Numbering_20_Symbols" style:num-suffix="." style:num-format="1">
    <style:list-level-properties text:space-before="0.499cm" text:min-label-width="0.499cm"/>
   </text:list-level-style-number>
   <text:list-level-style-number text:level="3" text:style-name="Numbering_20_Symbols" style:num-suffix="." style:num-format="1">
    <style:list-level-properties text:space-before="0.999cm" text:min-label-width="0.499cm"/>
   </text:list-level-style-number>
   <text:list-level-style-number text:level="4" text:style-name="Numbering_20_Symbols" style:num-suffix="." style:num-format="1">
    <style:list-level-properties text:space-before="1.498cm" text:min-label-width="0.499cm"/>
   </text:list-level-style-number>
   <text:list-level-style-number text:level="5" text:style-name="Numbering_20_Symbols" style:num-suffix="." style:num-format="1">
    <style:list-level-properties text:space-before="1.997cm" text:min-label-width="0.499cm"/>
   </text:list-level-style-number>
   <text:list-level-style-number text:level="6" text:style-name="Numbering_20_Symbols" style:num-suffix="." style:num-format="1">
    <style:list-level-properties text:space-before="2.496cm" text:min-label-width="0.499cm"/>
   </text:list-level-style-number>
   <text:list-level-style-number text:level="7" text:style-name="Numbering_20_Symbols" style:num-suffix="." style:num-format="1">
    <style:list-level-properties text:space-before="2.995cm" text:min-label-width="0.499cm"/>
   </text:list-level-style-number>
   <text:list-level-style-number text:level="8" text:style-name="Numbering_20_Symbols" style:num-suffix="." style:num-format="1">
    <style:list-level-properties text:space-before="3.494cm" text:min-label-width="0.499cm"/>
   </text:list-level-style-number>
   <text:list-level-style-number text:level="9" text:style-name="Numbering_20_Symbols" style:num-suffix="." style:num-format="1">
    <style:list-level-properties text:space-before="3.994cm" text:min-label-width="0.499cm"/>
   </text:list-level-style-number>
   <text:list-level-style-number text:level="10" text:style-name="Numbering_20_Symbols" style:num-suffix="." style:num-format="1">
    <style:list-level-properties text:space-before="4.493cm" text:min-label-width="0.499cm"/>
   </text:list-level-style-number>
  </text:list-style>
  <text:list-style style:name="Numbering_20_2" style:display-name="Numbering 2">
   <text:list-level-style-number text:level="1" text:style-name="Numbering_20_Symbols" style:num-format="1">
    <style:list-level-properties text:min-label-width="0.499cm"/>
   </text:list-level-style-number>
   <text:list-level-style-number text:level="2" text:style-name="Numbering_20_Symbols" style:num-format="1" text:start-value="2">
    <style:list-level-properties text:space-before="0.499cm" text:min-label-width="0.499cm"/>
   </text:list-level-style-number>
   <text:list-level-style-number text:level="3" text:style-name="Numbering_20_Symbols" style:num-format="1" text:start-value="3">
    <style:list-level-properties text:space-before="0.998cm" text:min-label-width="1cm"/>
   </text:list-level-style-number>
   <text:list-level-style-number text:level="4" text:style-name="Numbering_20_Symbols" style:num-format="1" text:start-value="4">
    <style:list-level-properties text:space-before="1.998cm" text:min-label-width="1.251cm"/>
   </text:list-level-style-number>
   <text:list-level-style-number text:level="5" text:style-name="Numbering_20_Symbols" style:num-format="1" text:start-value="5">
    <style:list-level-properties text:space-before="3.249cm" text:min-label-width="1.499cm"/>
   </text:list-level-style-number>
   <text:list-level-style-number text:level="6" text:style-name="Numbering_20_Symbols" style:num-format="1" text:start-value="6">
    <style:list-level-properties text:space-before="4.748cm" text:min-label-width="1.801cm"/>
   </text:list-level-style-number>
   <text:list-level-style-number text:level="7" text:style-name="Numbering_20_Symbols" style:num-format="1" text:start-value="7">
    <style:list-level-properties text:space-before="6.549cm" text:min-label-width="2.3cm"/>
   </text:list-level-style-number>
   <text:list-level-style-number text:level="8" text:style-name="Numbering_20_Symbols" style:num-format="1" text:start-value="8">
    <style:list-level-properties text:space-before="8.849cm" text:min-label-width="2.6cm"/>
   </text:list-level-style-number>
   <text:list-level-style-number text:level="9" text:style-name="Numbering_20_Symbols" style:num-format="1" text:start-value="9">
    <style:list-level-properties text:space-before="11.449cm" text:min-label-width="2.801cm"/>
   </text:list-level-style-number>
   <text:list-level-style-number text:level="10" text:style-name="Numbering_20_Symbols" style:num-format="1" text:start-value="10">
    <style:list-level-properties text:space-before="14.25cm" text:min-label-width="3.101cm"/>
   </text:list-level-style-number>
  </text:list-style>
  <text:list-style style:name="Numbering_20_3" style:display-name="Numbering 3">
   <text:list-level-style-number text:level="1" text:style-name="Numbering_20_Symbols" style:num-format="1">
    <style:list-level-properties text:min-label-width="3cm"/>
   </text:list-level-style-number>
   <text:list-level-style-number text:level="2" text:style-name="Numbering_20_Symbols" style:num-format="1" text:start-value="2">
    <style:list-level-properties text:space-before="3.001cm" text:min-label-width="3cm"/>
   </text:list-level-style-number>
   <text:list-level-style-number text:level="3" text:style-name="Numbering_20_Symbols" style:num-format="1" text:start-value="3">
    <style:list-level-properties text:space-before="6.001cm" text:min-label-width="3cm"/>
   </text:list-level-style-number>
   <text:list-level-style-number text:level="4" text:style-name="Numbering_20_Symbols" style:num-format="1" text:start-value="4">
    <style:list-level-properties text:space-before="9.002cm" text:min-label-width="3cm"/>
   </text:list-level-style-number>
   <text:list-level-style-number text:level="5" text:style-name="Numbering_20_Symbols" style:num-format="1" text:start-value="5">
    <style:list-level-properties text:space-before="12.002cm" text:min-label-width="3cm"/>
   </text:list-level-style-number>
   <text:list-level-style-number text:level="6" text:style-name="Numbering_20_Symbols" style:num-format="1" text:start-value="6">
    <style:list-level-properties text:space-before="15.002cm" text:min-label-width="3cm"/>
   </text:list-level-style-number>
   <text:list-level-style-number text:level="7" text:style-name="Numbering_20_Symbols" style:num-format="1" text:start-value="7">
    <style:list-level-properties text:space-before="18.003cm" text:min-label-width="3cm"/>
   </text:list-level-style-number>
   <text:list-level-style-number text:level="8" text:style-name="Numbering_20_Symbols" style:num-format="1" text:start-value="8">
    <style:list-level-properties text:space-before="21.003cm" text:min-label-width="3cm"/>
   </text:list-level-style-number>
   <text:list-level-style-number text:level="9" text:style-name="Numbering_20_Symbols" style:num-format="1" text:start-value="9">
    <style:list-level-properties text:space-before="24.003cm" text:min-label-width="3cm"/>
   </text:list-level-style-number>
   <text:list-level-style-number text:level="10" text:style-name="Numbering_20_Symbols" style:num-format="1" text:start-value="10">
    <style:list-level-properties text:space-before="27.004cm" text:min-label-width="3cm"/>
   </text:list-level-style-number>
  </text:list-style>
  <text:list-style style:name="Numbering_20_4" style:display-name="Numbering 4">
   <text:list-level-style-number text:level="1" text:style-name="Numbering_20_Symbols" style:num-suffix="." style:num-format="I">
    <style:list-level-properties text:min-label-width="0.499cm"/>
   </text:list-level-style-number>
   <text:list-level-style-number text:level="2" text:style-name="Numbering_20_Symbols" style:num-suffix="." style:num-format="I" text:start-value="2">
    <style:list-level-properties text:space-before="0.501cm" text:min-label-width="0.499cm"/>
   </text:list-level-style-number>
   <text:list-level-style-number text:level="3" text:style-name="Numbering_20_Symbols" style:num-suffix="." style:num-format="I" text:start-value="3">
    <style:list-level-properties text:space-before="1cm" text:min-label-width="0.499cm"/>
   </text:list-level-style-number>
   <text:list-level-style-number text:level="4" text:style-name="Numbering_20_Symbols" style:num-suffix="." style:num-format="I" text:start-value="4">
    <style:list-level-properties text:space-before="1.501cm" text:min-label-width="0.499cm"/>
   </text:list-level-style-number>
   <text:list-level-style-number text:level="5" text:style-name="Numbering_20_Symbols" style:num-suffix="." style:num-format="I" text:start-value="5">
    <style:list-level-properties text:space-before="2cm" text:min-label-width="0.499cm"/>
   </text:list-level-style-number>
   <text:list-level-style-number text:level="6" text:style-name="Numbering_20_Symbols" style:num-suffix="." style:num-format="I" text:start-value="6">
    <style:list-level-properties text:space-before="2.501cm" text:min-label-width="0.499cm"/>
   </text:list-level-style-number>
   <text:list-level-style-number text:level="7" text:style-name="Numbering_20_Symbols" style:num-suffix="." style:num-format="I" text:start-value="7">
    <style:list-level-properties text:space-before="3.001cm" text:min-label-width="0.499cm"/>
   </text:list-level-style-number>
   <text:list-level-style-number text:level="8" text:style-name="Numbering_20_Symbols" style:num-suffix="." style:num-format="I" text:start-value="8">
    <style:list-level-properties text:space-before="3.502cm" text:min-label-width="0.499cm"/>
   </text:list-level-style-number>
   <text:list-level-style-number text:level="9" text:style-name="Numbering_20_Symbols" style:num-suffix="." style:num-format="I" text:start-value="9">
    <style:list-level-properties text:space-before="4.001cm" text:min-label-width="0.499cm"/>
   </text:list-level-style-number>
   <text:list-level-style-number text:level="10" text:style-name="Numbering_20_Symbols" style:num-suffix="." style:num-format="I" text:start-value="10">
    <style:list-level-properties text:space-before="4.502cm" text:min-label-width="0.499cm"/>
   </text:list-level-style-number>
  </text:list-style>
  <text:list-style style:name="Numbering_20_5" style:display-name="Numbering 5">
   <text:list-level-style-number text:level="1" text:style-name="Numbering_20_Symbols" style:num-suffix="." style:num-format="1">
    <style:list-level-properties text:min-label-width="0.4cm"/>
   </text:list-level-style-number>
   <text:list-level-style-number text:level="2" text:style-name="Numbering_20_Symbols" style:num-suffix="." style:num-format="1" text:start-value="2" text:display-levels="2">
    <style:list-level-properties text:space-before="0.45cm" text:min-label-width="0.651cm"/>
   </text:list-level-style-number>
   <text:list-level-style-number text:level="3" text:style-name="Numbering_20_Symbols" style:num-suffix=")" style:num-format="a" text:start-value="3">
    <style:list-level-properties text:space-before="1.1cm" text:min-label-width="0.45cm"/>
   </text:list-level-style-number>
   <text:list-level-style-bullet text:level="4" text:style-name="Numbering_20_Symbols" text:bullet-char="•">
    <style:list-level-properties text:space-before="1.605cm" text:min-label-width="0.395cm"/>
    <style:text-properties fo:font-family="StarSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="5" text:style-name="Numbering_20_Symbols" text:bullet-char="•">
    <style:list-level-properties text:space-before="2cm" text:min-label-width="0.395cm"/>
    <style:text-properties fo:font-family="StarSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="6" text:style-name="Numbering_20_Symbols" text:bullet-char="•">
    <style:list-level-properties text:space-before="2.395cm" text:min-label-width="0.395cm"/>
    <style:text-properties fo:font-family="StarSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="7" text:style-name="Numbering_20_Symbols" text:bullet-char="•">
    <style:list-level-properties text:space-before="2.791cm" text:min-label-width="0.395cm"/>
    <style:text-properties fo:font-family="StarSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="8" text:style-name="Numbering_20_Symbols" text:bullet-char="•">
    <style:list-level-properties text:space-before="3.186cm" text:min-label-width="0.395cm"/>
    <style:text-properties fo:font-family="StarSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="9" text:style-name="Numbering_20_Symbols" text:bullet-char="•">
    <style:list-level-properties text:space-before="3.581cm" text:min-label-width="0.395cm"/>
    <style:text-properties fo:font-family="StarSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="10" text:style-name="Numbering_20_Symbols" text:bullet-char="•">
    <style:list-level-properties text:space-before="3.976cm" text:min-label-width="0.395cm"/>
    <style:text-properties fo:font-family="StarSymbol"/>
   </text:list-level-style-bullet>
  </text:list-style>
  <text:list-style style:name="List_20_1" style:display-name="List 1">
   <text:list-level-style-bullet text:level="1" text:style-name="Numbering_20_Symbols" text:bullet-char="•">
    <style:list-level-properties text:min-label-width="0.395cm"/>
    <style:text-properties style:font-name="StarSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="2" text:style-name="Numbering_20_Symbols" text:bullet-char="•">
    <style:list-level-properties text:space-before="0.395cm" text:min-label-width="0.395cm"/>
    <style:text-properties style:font-name="StarSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="3" text:style-name="Numbering_20_Symbols" text:bullet-char="•">
    <style:list-level-properties text:space-before="0.79cm" text:min-label-width="0.395cm"/>
    <style:text-properties style:font-name="StarSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="4" text:style-name="Numbering_20_Symbols" text:bullet-char="•">
    <style:list-level-properties text:space-before="1.185cm" text:min-label-width="0.395cm"/>
    <style:text-properties style:font-name="StarSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="5" text:style-name="Numbering_20_Symbols" text:bullet-char="•">
    <style:list-level-properties text:space-before="1.581cm" text:min-label-width="0.395cm"/>
    <style:text-properties style:font-name="StarSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="6" text:style-name="Numbering_20_Symbols" text:bullet-char="•">
    <style:list-level-properties text:space-before="1.976cm" text:min-label-width="0.395cm"/>
    <style:text-properties style:font-name="StarSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="7" text:style-name="Numbering_20_Symbols" text:bullet-char="•">
    <style:list-level-properties text:space-before="2.371cm" text:min-label-width="0.395cm"/>
    <style:text-properties style:font-name="StarSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="8" text:style-name="Numbering_20_Symbols" text:bullet-char="•">
    <style:list-level-properties text:space-before="2.766cm" text:min-label-width="0.395cm"/>
    <style:text-properties style:font-name="StarSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="9" text:style-name="Numbering_20_Symbols" text:bullet-char="•">
    <style:list-level-properties text:space-before="3.161cm" text:min-label-width="0.395cm"/>
    <style:text-properties style:font-name="StarSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="10" text:style-name="Numbering_20_Symbols" text:bullet-char="•">
    <style:list-level-properties text:space-before="3.556cm" text:min-label-width="0.395cm"/>
    <style:text-properties style:font-name="StarSymbol"/>
   </text:list-level-style-bullet>
  </text:list-style>
  <text:list-style style:name="List_20_2" style:display-name="List 2">
   <text:list-level-style-bullet text:level="1" text:style-name="Numbering_20_Symbols" text:bullet-char="–">
    <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">
     <style:list-level-label-alignment text:label-followed-by="listtab" text:list-tab-stop-position="0.3cm" fo:text-indent="-0.3cm" fo:margin-left="0.3cm"/>
    </style:list-level-properties>
    <style:text-properties fo:font-family="OpenSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="2" text:style-name="Numbering_20_Symbols" text:bullet-char="–">
    <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">
     <style:list-level-label-alignment text:label-followed-by="listtab" text:list-tab-stop-position="0.6cm" fo:text-indent="-0.3cm" fo:margin-left="0.6cm"/>
    </style:list-level-properties>
    <style:text-properties fo:font-family="OpenSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="3" text:style-name="Numbering_20_Symbols" text:bullet-char="–">
    <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">
     <style:list-level-label-alignment text:label-followed-by="listtab" text:list-tab-stop-position="0.9cm" fo:text-indent="-0.3cm" fo:margin-left="0.9cm"/>
    </style:list-level-properties>
    <style:text-properties fo:font-family="OpenSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="4" text:style-name="Numbering_20_Symbols" text:bullet-char="–">
    <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">
     <style:list-level-label-alignment text:label-followed-by="listtab" text:list-tab-stop-position="1.199cm" fo:text-indent="-0.3cm" fo:margin-left="1.199cm"/>
    </style:list-level-properties>
    <style:text-properties fo:font-family="OpenSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="5" text:style-name="Numbering_20_Symbols" text:bullet-char="–">
    <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">
     <style:list-level-label-alignment text:label-followed-by="listtab" text:list-tab-stop-position="1.499cm" fo:text-indent="-0.3cm" fo:margin-left="1.499cm"/>
    </style:list-level-properties>
    <style:text-properties fo:font-family="OpenSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="6" text:style-name="Numbering_20_Symbols" text:bullet-char="–">
    <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">
     <style:list-level-label-alignment text:label-followed-by="listtab" text:list-tab-stop-position="1.799cm" fo:text-indent="-0.3cm" fo:margin-left="1.799cm"/>
    </style:list-level-properties>
    <style:text-properties fo:font-family="OpenSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="7" text:style-name="Numbering_20_Symbols" text:bullet-char="–">
    <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">
     <style:list-level-label-alignment text:label-followed-by="listtab" text:list-tab-stop-position="2.101cm" fo:text-indent="-0.3cm" fo:margin-left="2.101cm"/>
    </style:list-level-properties>
    <style:text-properties fo:font-family="OpenSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="8" text:style-name="Numbering_20_Symbols" text:bullet-char="–">
    <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">
     <style:list-level-label-alignment text:label-followed-by="listtab" text:list-tab-stop-position="2.401cm" fo:text-indent="-0.3cm" fo:margin-left="2.401cm"/>
    </style:list-level-properties>
    <style:text-properties fo:font-family="OpenSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="9" text:style-name="Numbering_20_Symbols" text:bullet-char="–">
    <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">
     <style:list-level-label-alignment text:label-followed-by="listtab" text:list-tab-stop-position="2.701cm" fo:text-indent="-0.3cm" fo:margin-left="2.701cm"/>
    </style:list-level-properties>
    <style:text-properties fo:font-family="OpenSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="10" text:style-name="Numbering_20_Symbols" text:bullet-char="–">
    <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">
     <style:list-level-label-alignment text:label-followed-by="listtab" text:list-tab-stop-position="3cm" fo:text-indent="-0.3cm" fo:margin-left="3cm"/>
    </style:list-level-properties>
    <style:text-properties fo:font-family="OpenSymbol"/>
   </text:list-level-style-bullet>
  </text:list-style>
  <text:list-style style:name="List_20_3" style:display-name="List 3">
   <text:list-level-style-bullet text:level="1" text:style-name="Numbering_20_Symbols" text:bullet-char="☑">
    <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">
     <style:list-level-label-alignment text:label-followed-by="listtab" text:list-tab-stop-position="0.395cm" fo:text-indent="-0.395cm" fo:margin-left="0.395cm"/>
    </style:list-level-properties>
    <style:text-properties fo:font-family="OpenSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="2" text:style-name="Numbering_20_Symbols" text:bullet-char="□">
    <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">
     <style:list-level-label-alignment text:label-followed-by="listtab" text:list-tab-stop-position="0.79cm" fo:text-indent="-0.395cm" fo:margin-left="0.79cm"/>
    </style:list-level-properties>
    <style:text-properties fo:font-family="OpenSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="3" text:style-name="Numbering_20_Symbols" text:bullet-char="☑">
    <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">
     <style:list-level-label-alignment text:label-followed-by="listtab" text:list-tab-stop-position="0.395cm" fo:text-indent="-0.395cm" fo:margin-left="0.395cm"/>
    </style:list-level-properties>
    <style:text-properties fo:font-family="OpenSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="4" text:style-name="Numbering_20_Symbols" text:bullet-char="□">
    <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">
     <style:list-level-label-alignment text:label-followed-by="listtab" text:list-tab-stop-position="0.79cm" fo:text-indent="-0.395cm" fo:margin-left="0.79cm"/>
    </style:list-level-properties>
    <style:text-properties fo:font-family="OpenSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="5" text:style-name="Numbering_20_Symbols" text:bullet-char="☑">
    <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">
     <style:list-level-label-alignment text:label-followed-by="listtab" text:list-tab-stop-position="0.395cm" fo:text-indent="-0.395cm" fo:margin-left="0.395cm"/>
    </style:list-level-properties>
    <style:text-properties fo:font-family="OpenSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="6" text:style-name="Numbering_20_Symbols" text:bullet-char="□">
    <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">
     <style:list-level-label-alignment text:label-followed-by="listtab" text:list-tab-stop-position="0.79cm" fo:text-indent="-0.395cm" fo:margin-left="0.79cm"/>
    </style:list-level-properties>
    <style:text-properties fo:font-family="OpenSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="7" text:style-name="Numbering_20_Symbols" text:bullet-char="☑">
    <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">
     <style:list-level-label-alignment text:label-followed-by="listtab" text:list-tab-stop-position="0.395cm" fo:text-indent="-0.395cm" fo:margin-left="0.395cm"/>
    </style:list-level-properties>
    <style:text-properties fo:font-family="OpenSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="8" text:style-name="Numbering_20_Symbols" text:bullet-char="□">
    <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">
     <style:list-level-label-alignment text:label-followed-by="listtab" text:list-tab-stop-position="0.79cm" fo:text-indent="-0.395cm" fo:margin-left="0.79cm"/>
    </style:list-level-properties>
    <style:text-properties fo:font-family="OpenSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="9" text:style-name="Numbering_20_Symbols" text:bullet-char="☑">
    <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">
     <style:list-level-label-alignment text:label-followed-by="listtab" text:list-tab-stop-position="0.395cm" fo:text-indent="-0.395cm" fo:margin-left="0.395cm"/>
    </style:list-level-properties>
    <style:text-properties fo:font-family="OpenSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="10" text:style-name="Numbering_20_Symbols" text:bullet-char="□">
    <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">
     <style:list-level-label-alignment text:label-followed-by="listtab" text:list-tab-stop-position="0.79cm" fo:text-indent="-0.395cm" fo:margin-left="0.79cm"/>
    </style:list-level-properties>
    <style:text-properties fo:font-family="OpenSymbol"/>
   </text:list-level-style-bullet>
  </text:list-style>
  <text:list-style style:name="List_20_4" style:display-name="List 4">
   <text:list-level-style-bullet text:level="1" text:style-name="Numbering_20_Symbols" text:bullet-char="➢">
    <style:list-level-properties text:min-label-width="0.4cm"/>
    <style:text-properties fo:font-family="StarSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="2" text:style-name="Numbering_20_Symbols" text:bullet-char="">
    <style:list-level-properties text:space-before="0.401cm" text:min-label-width="0.4cm"/>
    <style:text-properties fo:font-family="StarSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="3" text:style-name="Numbering_20_Symbols" text:bullet-char="">
    <style:list-level-properties text:space-before="0.799cm" text:min-label-width="0.4cm"/>
    <style:text-properties fo:font-family="StarSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="4" text:style-name="Numbering_20_Symbols" text:bullet-char="">
    <style:list-level-properties text:space-before="1.2cm" text:min-label-width="0.4cm"/>
    <style:text-properties fo:font-family="StarSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="5" text:style-name="Numbering_20_Symbols" text:bullet-char="">
    <style:list-level-properties text:space-before="1.6cm" text:min-label-width="0.4cm"/>
    <style:text-properties fo:font-family="StarSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="6" text:style-name="Numbering_20_Symbols" text:bullet-char="">
    <style:list-level-properties text:space-before="2.001cm" text:min-label-width="0.4cm"/>
    <style:text-properties fo:font-family="StarSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="7" text:style-name="Numbering_20_Symbols" text:bullet-char="">
    <style:list-level-properties text:space-before="2.399cm" text:min-label-width="0.4cm"/>
    <style:text-properties fo:font-family="StarSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="8" text:style-name="Numbering_20_Symbols" text:bullet-char="">
    <style:list-level-properties text:space-before="2.8cm" text:min-label-width="0.4cm"/>
    <style:text-properties fo:font-family="StarSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="9" text:style-name="Numbering_20_Symbols" text:bullet-char="">
    <style:list-level-properties text:space-before="3.2cm" text:min-label-width="0.4cm"/>
    <style:text-properties fo:font-family="StarSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="10" text:style-name="Numbering_20_Symbols" text:bullet-char="">
    <style:list-level-properties text:space-before="3.601cm" text:min-label-width="0.4cm"/>
    <style:text-properties fo:font-family="StarSymbol"/>
   </text:list-level-style-bullet>
  </text:list-style>
  <text:list-style style:name="List_20_5" style:display-name="List 5">
   <text:list-level-style-bullet text:level="1" text:style-name="Numbering_20_Symbols" text:bullet-char="✗">
    <style:list-level-properties text:min-label-width="0.4cm"/>
    <style:text-properties fo:font-family="StarSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="2" text:style-name="Numbering_20_Symbols" text:bullet-char="✗">
    <style:list-level-properties text:space-before="0.401cm" text:min-label-width="0.4cm"/>
    <style:text-properties fo:font-family="StarSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="3" text:style-name="Numbering_20_Symbols" text:bullet-char="✗">
    <style:list-level-properties text:space-before="0.799cm" text:min-label-width="0.4cm"/>
    <style:text-properties fo:font-family="StarSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="4" text:style-name="Numbering_20_Symbols" text:bullet-char="✗">
    <style:list-level-properties text:space-before="1.2cm" text:min-label-width="0.4cm"/>
    <style:text-properties fo:font-family="StarSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="5" text:style-name="Numbering_20_Symbols" text:bullet-char="✗">
    <style:list-level-properties text:space-before="1.6cm" text:min-label-width="0.4cm"/>
    <style:text-properties fo:font-family="StarSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="6" text:style-name="Numbering_20_Symbols" text:bullet-char="✗">
    <style:list-level-properties text:space-before="2.001cm" text:min-label-width="0.4cm"/>
    <style:text-properties fo:font-family="StarSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="7" text:style-name="Numbering_20_Symbols" text:bullet-char="✗">
    <style:list-level-properties text:space-before="2.399cm" text:min-label-width="0.4cm"/>
    <style:text-properties fo:font-family="StarSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="8" text:style-name="Numbering_20_Symbols" text:bullet-char="✗">
    <style:list-level-properties text:space-before="2.8cm" text:min-label-width="0.4cm"/>
    <style:text-properties fo:font-family="StarSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="9" text:style-name="Numbering_20_Symbols" text:bullet-char="✗">
    <style:list-level-properties text:space-before="3.2cm" text:min-label-width="0.4cm"/>
    <style:text-properties fo:font-family="StarSymbol"/>
   </text:list-level-style-bullet>
   <text:list-level-style-bullet text:level="10" text:style-name="Numbering_20_Symbols" text:bullet-char="✗">
    <style:list-level-properties text:space-before="3.601cm" text:min-label-width="0.4cm"/>
    <style:text-properties fo:font-family="StarSymbol"/>
   </text:list-level-style-bullet>
  </text:list-style>
  <text:notes-configuration text:note-class="footnote" text:citation-style-name="Footnote_20_Symbol" text:citation-body-style-name="Footnote_20_anchor" style:num-format="1" text:start-value="0" text:footnotes-position="page" text:start-numbering-at="document"/>
  <text:notes-configuration text:note-class="endnote" style:num-format="i" text:start-value="0"/>
  <text:linenumbering-configuration text:number-lines="false" text:offset="0.499cm" style:num-format="1" text:number-position="left" text:increment="5"/>
 </office:styles>
 <office:automatic-styles>
  <style:page-layout style:name="Mpm1">
   <style:page-layout-properties fo:page-width="21.001cm" fo:page-height="29.7cm" style:num-format="1" style:paper-tray-name="[From printer settings]" style:print-orientation="portrait" fo:margin-top="3.2cm" fo:margin-bottom="2.499cm" fo:margin-left="2.701cm" fo:margin-right="3cm" style:writing-mode="lr-tb" style:footnote-max-height="0cm">
    <style:columns fo:column-count="1" fo:column-gap="0cm"/>
    <style:footnote-sep style:width="0.018cm" style:distance-before-sep="0.101cm" style:distance-after-sep="0.101cm" style:adjustment="left" style:rel-width="25%" style:color="#000000"/>
   </style:page-layout-properties>
   <style:header-style/>
   <style:footer-style>
    <style:header-footer-properties fo:min-height="1.699cm" fo:margin-left="0cm" fo:margin-right="0cm" fo:margin-top="1.199cm" style:shadow="none" style:dynamic-spacing="false"/>
   </style:footer-style>
  </style:page-layout>
  <style:page-layout style:name="Mpm2">
   <style:page-layout-properties fo:page-width="21.001cm" fo:page-height="29.7cm" style:num-format="1" style:print-orientation="portrait" fo:margin-top="2cm" fo:margin-bottom="2cm" fo:margin-left="2.499cm" fo:margin-right="2.499cm" style:shadow="none" fo:background-color="transparent" style:writing-mode="lr-tb" style:footnote-max-height="0cm">
    <style:background-image/>
    <style:columns fo:column-count="1" fo:column-gap="0cm"/>
    <style:footnote-sep style:width="0.018cm" style:distance-before-sep="0.101cm" style:distance-after-sep="0.101cm" style:adjustment="left" style:rel-width="25%" style:color="#000000"/>
   </style:page-layout-properties>
   <style:header-style/>
   <style:footer-style/>
  </style:page-layout>
  <style:page-layout style:name="Mpm3" style:page-usage="left">
   <style:page-layout-properties fo:page-width="21.001cm" fo:page-height="29.7cm" style:num-format="1" style:print-orientation="portrait" fo:margin-top="2cm" fo:margin-bottom="1cm" fo:margin-left="2.499cm" fo:margin-right="4.5cm" style:writing-mode="lr-tb" style:footnote-max-height="0cm">
    <style:footnote-sep style:width="0.018cm" style:distance-before-sep="0.101cm" style:distance-after-sep="0.101cm" style:adjustment="left" style:rel-width="25%" style:color="#000000"/>
   </style:page-layout-properties>
   <style:header-style/>
   <style:footer-style/>
  </style:page-layout>
  <style:page-layout style:name="Mpm4" style:page-usage="right">
   <style:page-layout-properties fo:page-width="21.001cm" fo:page-height="29.7cm" style:num-format="1" style:print-orientation="portrait" fo:margin-top="2cm" fo:margin-bottom="1cm" fo:margin-left="2.499cm" fo:margin-right="4.5cm" style:writing-mode="lr-tb" style:footnote-max-height="0cm">
    <style:footnote-sep style:width="0.018cm" style:distance-before-sep="0.101cm" style:distance-after-sep="0.101cm" style:adjustment="left" style:rel-width="25%" style:color="#000000"/>
   </style:page-layout-properties>
   <style:header-style/>
   <style:footer-style/>
  </style:page-layout>
  <style:page-layout style:name="Mpm5">
   <style:page-layout-properties fo:page-width="22.721cm" fo:page-height="11.4cm" style:num-format="1" style:print-orientation="landscape" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:margin-left="0cm" fo:margin-right="0cm" style:writing-mode="lr-tb" style:footnote-max-height="0cm">
    <style:footnote-sep style:width="0.018cm" style:distance-before-sep="0.101cm" style:distance-after-sep="0.101cm" style:adjustment="left" style:rel-width="25%" style:color="#000000"/>
   </style:page-layout-properties>
   <style:header-style/>
   <style:footer-style/>
  </style:page-layout>
  <style:page-layout style:name="Mpm6">
   <style:page-layout-properties fo:page-width="14.801cm" fo:page-height="21.001cm" style:num-format="1" style:print-orientation="portrait" fo:margin-top="2cm" fo:margin-bottom="2cm" fo:margin-left="2cm" fo:margin-right="2cm" style:writing-mode="lr-tb" style:footnote-max-height="0cm">
    <style:footnote-sep style:width="0.018cm" style:distance-before-sep="0.101cm" style:distance-after-sep="0.101cm" style:adjustment="left" style:rel-width="25%" style:color="#000000"/>
   </style:page-layout-properties>
   <style:header-style/>
   <style:footer-style/>
  </style:page-layout>
  <style:page-layout style:name="Mpm7">
   <style:page-layout-properties fo:page-width="20.999cm" fo:page-height="29.699cm" style:num-format="1" style:print-orientation="portrait" fo:margin-top="2cm" fo:margin-bottom="2cm" fo:margin-left="2cm" fo:margin-right="2cm" style:writing-mode="lr-tb" style:footnote-max-height="0cm">
    <style:footnote-sep style:adjustment="left" style:rel-width="25%" style:color="#000000"/>
   </style:page-layout-properties>
   <style:header-style/>
   <style:footer-style/>
  </style:page-layout>
 </office:automatic-styles>
 <office:master-styles>
  <style:master-page style:name="Standard" style:page-layout-name="Mpm1">
   <style:footer>
    <text:p text:style-name="Footer"><text:page-number text:select-page="current">14</text:page-number></text:p>
   </style:footer>
  </style:master-page>
  <style:master-page style:name="First_20_Page" style:display-name="First Page" style:page-layout-name="Mpm2" style:next-style-name="Standard"/>
  <style:master-page style:name="Left_20_Page" style:display-name="Left Page" style:page-layout-name="Mpm3"/>
  <style:master-page style:name="Right_20_Page" style:display-name="Right Page" style:page-layout-name="Mpm4"/>
  <style:master-page style:name="Envelope" style:page-layout-name="Mpm5"/>
  <style:master-page style:name="Index" style:page-layout-name="Mpm6" style:next-style-name="Standard"/>
  <style:master-page style:name="Endnote" style:page-layout-name="Mpm7"/>
 </office:master-styles>
</office:document-styles>
'''
    _MIMETYPE = 'application/vnd.oasis.opendocument.text'

    def tear_down(self):
        """Delete the temporary directory 
        containing the unpacked ODT directory structure.
        """
        try:
            rmtree(self._TEMPDIR)
        except:
            pass

    def set_up(self):
        """Create a temporary directory containing the internal 
        structure of an ODT file except 'content.xml'.
        """
        self.tear_down()
        os.mkdir(self._TEMPDIR)
        os.mkdir(self._TEMPDIR + '/META-INF')

        # Generate mimetype

        try:
            with open(self._TEMPDIR + '/mimetype', 'w', encoding='utf-8') as f:
                f.write(self._MIMETYPE)
        except:
            return 'ERROR: Cannot write "mimetype"'

        # Generate manifest.rdf

        try:
            with open(self._TEMPDIR + '/manifest.rdf', 'w', encoding='utf-8') as f:
                f.write(self._MANIFEST_RDF)
        except:
            return 'ERROR: Cannot write "manifest.rdf"'

        # Generate settings.xml

        try:
            with open(self._TEMPDIR + '/settings.xml', 'w', encoding='utf-8') as f:
                f.write(self._SETTINGS_XML)
        except:
            return 'ERROR: Cannot write "settings.xml"'

        # Generate META-INF\manifest.xml

        try:
            with open(self._TEMPDIR + '/META-INF/manifest.xml', 'w', encoding='utf-8') as f:
                f.write(self._MANIFEST_XML)
        except:
            return 'ERROR: Cannot write "manifest.xml"'

        # Generate styles.xml with system language set as document language

        localeCodes = locale.getdefaultlocale()[0].split('_')
        languageCode = localeCodes[0]
        countryCode = localeCodes[1]
        text = self._STYLES_XML
        text = re.sub('fo\:language\=\"..',
                      'fo:language="' + languageCode, text)
        text = re.sub('fo\:country\=\"..',
                      'fo:country="' + countryCode, text)
        try:
            with open(self._TEMPDIR + '/styles.xml', 'w', encoding='utf-8') as f:
                f.write(text)
        except:
            return 'ERROR: Cannot write "styles.xml"'

        # Generate meta.xml with actual document metadata

        dt = datetime.today()
        date = str(dt.year) + '-' + str(dt.month).rjust(2, '0') + '-' + \
            str(dt.day).rjust(2, '0')
        time = str(dt.hour).rjust(2, '0') + ':' + \
            str(dt.minute).rjust(2, '0') + ':' + \
            str(dt.second).rjust(2, '0')
        text = self._META_XML.replace('%author%', self.author).replace('%title%', self.title).replace(
            '%summary%', '<![CDATA[' + self.desc + ']]>').replace('%date%', date).replace('%time%', time)

        try:
            with open(self._TEMPDIR + '/meta.xml', 'w', encoding='utf-8') as f:
                f.write(text)
        except:
            return 'ERROR: Cannot write "meta.xml".'

        return 'SUCCESS: ODT structure generated.'
from abc import abstractmethod


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
        # xml: <PROJECT><Title>

        self.desc = None
        # str
        # xml: <PROJECT><Desc>

        self.author = None
        # str
        # xml: <PROJECT><AuthorName>

        self.fieldTitle1 = None
        # str
        # xml: <PROJECT><FieldTitle1>

        self.fieldTitle2 = None
        # str
        # xml: <PROJECT><FieldTitle2>

        self.fieldTitle3 = None
        # str
        # xml: <PROJECT><FieldTitle3>

        self.fieldTitle4 = None
        # str
        # xml: <PROJECT><FieldTitle4>

        self.chapters = {}
        # dict
        # xml: <CHAPTERS><CHAPTER><ID>
        # key = chapter ID, value = Chapter object.
        # The order of the elements does not matter (the novel's
        # order of the chapters is defined by srtChapters)

        self.scenes = {}
        # dict
        # xml: <SCENES><SCENE><ID>
        # key = scene ID, value = Scene object.
        # The order of the elements does not matter (the novel's
        # order of the scenes is defined by the order of the chapters
        # and the order of the scenes within the chapters)

        self.srtChapters = []
        # list of str
        # The novel's chapter IDs. The order of its elements
        # corresponds to the novel's order of the chapters.

        self.locations = {}
        # dict
        # xml: <LOCATIONS>
        # key = location ID, value = Object.
        # The order of the elements does not matter.

        self.items = {}
        # dict
        # xml: <ITEMS>
        # key = item ID, value = Object.
        # The order of the elements does not matter.

        self.characters = {}
        # dict
        # xml: <CHARACTERS>
        # key = character ID, value = Character object.
        # The order of the elements does not matter.

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
    def merge(self, novel):
        """Merge selected novel properties.
        To be overwritten by file format specific subclasses.
        """

    @abstractmethod
    def write(self):
        """Write selected properties to the file.
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


def to_odt(text):
    """Convert yw7 raw markup to odt. Return an xml string."""
    try:
        # process italics and bold markup reaching across linebreaks

        italics = False
        bold = False
        newlines = []
        lines = text.split('\n')
        for line in lines:
            if italics:
                line = '[i]' + line
                italics = False

            while line.count('[i]') > line.count('[/i]'):
                line += '[/i]'
                italics = True

            while line.count('[/i]') > line.count('[i]'):
                line = '[i]' + line

            line = line.replace('[i][/i]', '')

            if bold:
                line = '[b]' + line
                bold = False

            while line.count('[b]') > line.count('[/b]'):
                line += '[/b]'
                bold = True

            while line.count('[/b]') > line.count('[b]'):
                line = '[b]' + line

            line = line.replace('[b][/b]', '')

            newlines.append(line)

        text = '\n'.join(newlines)
        text = text.replace('&', '&amp;')
        text = text.replace('>', '&gt;')
        text = text.replace('<', '&lt;')
        text = text.rstrip().replace(
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




class OdtFile(Novel, OdtTemplate):
    """OpenDocument xml project file representation."""
    _FILE_EXTENSION = '.odt'

    _SCENE_DIVIDER = '* * *'
    # To be placed between scene ending and beginning tags.

    def write_content_xml(self):
        """Write scene content to "content.xml".

        Considered are "used" scenes within
        chapters not marked  "Other" or "Unused" or "Info".

        Generate "content.xml" containing:
        - the scene titles as comments,
        - the scene contents.
        Return a message beginning with SUCCESS or ERROR.
        """
        lines = [self._CONTENT_XML_HEADER]
        lines.append(self._ODT_TITLE_START + self.title + self._ODT_PARA_END)
        lines.append(self._ODT_SUBTITLE_START +
                     self.author + self._ODT_PARA_END)

        for chId in self.srtChapters:

            if self.chapters[chId].isUnused:
                continue

            if self.chapters[chId].chType != 0:
                continue

            # Write chapter heading.

            lines.append(self._ODT_HEADING_STARTS[self.chapters[chId].chLevel] +
                         self.chapters[chId].get_title() + self._ODT_HEADING_END)
            firstSceneInChapter = True

            for scId in self.chapters[chId].srtScenes:

                if self.scenes[scId].isUnused:
                    continue

                if self.scenes[scId].doNotExport:
                    continue

                # Write Scene divider.

                if not (firstSceneInChapter or self.scenes[scId].appendToPrev):
                    lines.append(
                        self._ODT_SCENEDIV_START + self._SCENE_DIVIDER + self._ODT_PARA_END)

                if self.scenes[scId].appendToPrev:
                    scenePrefix = self._ODT_PARA_START

                else:
                    scenePrefix = self._ODT_FIRST_PARA_START

                # Write scene title as comment.

                scenePrefix += ('<office:annotation>\n' +
                                '<dc:creator>scene title</dc:creator>\n' +
                                '<text:p>' + self.scenes[scId].title + '</text:p>\n' +
                                '</office:annotation>')

                # Write scene content.

                if self.scenes[scId].sceneContent is not None:
                    lines.append(scenePrefix +
                                 to_odt(self.scenes[scId].sceneContent) + self._ODT_PARA_END)

                else:
                    lines.append(scenePrefix + self._ODT_PARA_END)

                firstSceneInChapter = False

        lines.append(self._CONTENT_XML_FOOTER)
        text = '\n'.join(lines)

        try:
            with open(self._TEMPDIR + '/content.xml', 'w', encoding='utf-8') as f:
                f.write(text)

        except:
            return 'ERROR: Cannot write "content.xml".'

        return 'SUCCESS: Content written to "content.xml"'

    def merge(self, novel):
        """Copy selected novel attributes.
        """

        if novel.title is None:
            self.title = ''

        else:
            self.title = novel.title

        if novel.desc is None:
            self.desc = ''

        else:
            self.desc = novel.desc

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

        if novel.characters is not None:
            self.characters = novel.characters

        if novel.locations is not None:
            self.locations = novel.locations

        if novel.items is not None:
            self.items = novel.items

    def write(self):
        """Generate an odt file from a template.
        Return a message beginning with SUCCESS or ERROR.
        """

        # Create a temporary directory containing the internal
        # structure of an ODT file except "content.xml".

        message = self.set_up()

        if message.startswith('ERROR'):
            return message

        # Add "content.xml" to the temporary directory.

        message = self.write_content_xml()

        if message.startswith('ERROR'):
            return message

        # Pack the contents of the temporary directory
        # into the ODT file.

        workdir = os.getcwd()

        try:
            with zipfile.ZipFile(self.filePath, 'w') as odtTarget:
                os.chdir(self._TEMPDIR)

                for file in self._ODT_COMPONENTS:
                    odtTarget.write(file)
        except:
            os.chdir(workdir)
            return 'ERROR: Cannot generate "' + self._filePath + '".'

        # Remove temporary data.

        os.chdir(workdir)
        self.tear_down()
        return 'SUCCESS: "' + self._filePath + '" saved.'

import xml.etree.ElementTree as ET



class Chapter():
    """yWriter chapter representation.
    # xml: <CHAPTERS><CHAPTER>
    """

    def __init__(self):
        self.title = None
        # str
        # xml: <Title>

        self.desc = None
        # str
        # xml: <Desc>

        self.chLevel = None
        # int
        # xml: <SectionStart>
        # 0 = chapter level
        # 1 = section level ("this chapter begins a section")

        self.chType = None
        # int
        # xml: <Type>
        # 0 = chapter type (marked "Chapter")
        # 1 = other type (marked "Other")

        self.isUnused = None
        # bool
        # xml: <Unused> -1

        self.suppressChapterTitle = None
        # bool
        # xml: <Fields><Field_SuppressChapterTitle> 1
        # True: Remove 'Chapter ' from the chapter title upon import.
        # False: Do not modify the chapter title.

        self.isTrash = None
        # bool
        # xml: <Fields><Field_IsTrash> 1
        # True: This chapter is the yw7 project's "trash bin".
        # False: This chapter is not a "trash bin".

        self.doNotExport = None
        # bool
        # xml: <<Fields>Field_SuppressChapterBreak> 0

        self.srtScenes = []
        # list of str
        # xml: <Scenes><ScID>
        # The chapter's scene IDs. The order of its elements
        # corresponds to the chapter's order of the scenes.

    def get_title(self):
        """Fix auto-chapter titles for non-English """
        text = self.title

        if self.suppressChapterTitle:
            text = text.replace('Chapter ', '')

        return text



class Scene():
    """yWriter scene representation.
    # xml: <SCENES><SCENE>
    """

    # Emulate an enumeration for the scene status

    STATUS = [None, 'Outline', 'Draft', '1st Edit', '2nd Edit', 'Done']

    def __init__(self):
        self.title = None
        # str
        # xml: <Title>

        self.desc = None
        # str
        # xml: <Desc>

        self._sceneContent = None
        # str
        # xml: <SceneContent>
        # Scene text with yW7 raw markup.

        self.wordCount = 0
        # int # xml: <WordCount>
        # To be updated by the sceneContent setter

        self.letterCount = 0
        # int
        # xml: <LetterCount>
        # To be updated by the sceneContent setter

        self.isUnused = None
        # bool
        # xml: <Unused> -1

        self.status = None
        # int # xml: <Status>

        self.sceneNotes = None
        # str
        # xml: <Notes>

        self.tags = None
        # list of str
        # xml: <Tags>

        self.field1 = None
        # str
        # xml: <Field1>

        self.field2 = None
        # str
        # xml: <Field2>

        self.field3 = None
        # str
        # xml: <Field3>

        self.field4 = None
        # str
        # xml: <Field4>

        self.appendToPrev = None
        # bool
        # xml: <AppendToPrev> -1

        self.isReactionScene = None
        # bool
        # xml: <ReactionScene> -1

        self.isSubPlot = None
        # bool
        # xml: <SubPlot> -1

        self.goal = None
        # str
        # xml: <Goal>

        self.conflict = None
        # str
        # xml: <Conflict>

        self.outcome = None
        # str
        # xml: <Outcome>

        self.characters = None
        # list of str
        # xml: <Characters><CharID>

        self.locations = None
        # list of str
        # xml: <Locations><LocID>

        self.items = None
        # list of str
        # xml: <Items><ItemID>

        # xml: <SpecificDateMode>-1</SpecificDateMode>
        # xml: <SpecificDateTime>1900-06-01 20:38:00</SpecificDateTime>

        # xml: <Minute>
        # xml: <Hour>
        # xml: <Day>

        # xml: <LastsMinutes>
        # xml: <LastsHours>
        # xml: <LastsDays>

    @property
    def sceneContent(self):
        return self._sceneContent

    @sceneContent.setter
    def sceneContent(self, text):
        """Set sceneContent updating word count and letter count."""
        self._sceneContent = text
        text = re.sub('\[.+?\]|\.|\,| -', '', self._sceneContent)
        # Remove yWriter raw markup for word count

        wordList = text.split()
        self.wordCount = len(wordList)

        text = re.sub('\[.+?\]', '', self._sceneContent)
        # Remove yWriter raw markup for letter count

        text = text.replace('\n', '')
        text = text.replace('\r', '')
        self.letterCount = len(text)



class Object():
    """yWriter object representation.
    # xml: <LOCATIONS><LOCATION> or # xml: <ITEMS><ITEM>
    """

    def __init__(self):
        self.title = None
        # str
        # xml: <Title>

        self.desc = None
        # str
        # xml: <Desc>

        self.tags = None
        # list of str
        # xml: <Tags>

        self.aka = None
        # str
        # xml: <AKA>


class Character(Object):
    """yWriter character representation.
    # xml: <CHARACTERS><CHARACTER>
    """

    def __init__(self):
        Object.__init__(self)

        self.notes = None
        # str
        # xml: <Notes>

        self.bio = None
        # str
        # xml: <Bio>

        self.goals = None
        # str
        # xml: <Goals>

        self.fullName = None
        # str
        # xml: <FullName>

        self.isMajor = None
        # bool
        # xml: <Major>
from html import unescape

EM_DASH = '—'
EN_DASH = '–'
SAFE_DASH = '--'


def replace_unsafe_glyphs(text):
    """Replace glyphs being corrupted by yWriter with safe substitutes. """
    return text.replace(EN_DASH, SAFE_DASH).replace(EM_DASH, SAFE_DASH)


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


def xml_postprocess(filePath, fileEncoding, cdataTags: list):
    '''Postprocess the xml file created by ElementTree:
       Put a header on top, insert the missing CDATA tags,
       and replace "ampersand" xml entity by plain text.
    '''
    with open(filePath, 'r', encoding=fileEncoding) as f:
        lines = f.readlines()

    newlines = ['<?xml version="1.0" encoding="' + fileEncoding + '"?>\n']

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
    newXml = unescape(newXml)

    try:
        with open(filePath, 'w', encoding=fileEncoding) as f:
            f.write(newXml)

    except:
        return 'ERROR: Can not write"' + filePath + '".'

    return 'SUCCESS: "' + filePath + '" written.'




class YwFile(Novel):
    """yWriter xml project file representation."""

    def __init__(self, filePath):
        Novel.__init__(self, filePath)
        self._cdataTags = ['Title', 'AuthorName', 'Bio', 'Desc',
                           'FieldTitle1', 'FieldTitle2', 'FieldTitle3',
                           'FieldTitle4', 'LaTeXHeaderFile', 'Tags',
                           'AKA', 'ImageFile', 'FullName', 'Goals',
                           'Notes', 'RTFFile', 'SceneContent',
                           'Outcome', 'Goal', 'Conflict']
        # Names of yWriter xml elements containing CDATA.
        # ElementTree.write omits CDATA tags, so they have to be inserted
        # afterwards.

    @property
    def filePath(self):
        return self._filePath

    @filePath.setter
    def filePath(self, filePath):
        """Accept only filenames with the correct extension. """

        if filePath.lower().endswith('.yw7'):
            self._FILE_EXTENSION = '.yw7'
            self._ENCODING = 'utf-8'
            self._filePath = filePath

        elif filePath.lower().endswith('.yw6'):
            self._FILE_EXTENSION = '.yw6'
            self._ENCODING = 'utf-8'
            self._filePath = filePath

        elif filePath.lower().endswith('.yw5'):
            self._FILE_EXTENSION = '.yw5'
            self._ENCODING = 'iso-8859-1'
            self._filePath = filePath

    def read(self):
        """Parse the yWriter xml file located at filePath, fetching the Novel attributes.
        Return a message beginning with SUCCESS or ERROR.
        """

        # Complete the list of tags requiring CDATA (if incomplete).

        try:
            with open(self._filePath, 'r', encoding=self._ENCODING) as f:
                xmlData = f.read()

        except(FileNotFoundError):
            return 'ERROR: "' + self._filePath + '" not found.'

        lines = xmlData.split('\n')

        for line in lines:
            tag = re.search('\<(.+?)\>\<\!\[CDATA', line)

            if tag is not None:

                if not (tag.group(1) in self._cdataTags):
                    self._cdataTags.append(tag.group(1))

        # Open the file again to let ElementTree parse its xml structure.

        try:
            self._tree = ET.parse(self._filePath)
            root = self._tree.getroot()

        except:
            return 'ERROR: Can not process "' + self._filePath + '".'

        # Read locations from the xml element tree.

        for loc in root.iter('LOCATION'):
            lcId = loc.find('ID').text

            self.locations[lcId] = Object()
            self.locations[lcId].title = loc.find('Title').text

            if loc.find('Desc') is not None:
                self.locations[lcId].desc = loc.find('Desc').text

            if loc.find('AKA') is not None:
                self.locations[lcId].aka = loc.find('AKA').text

            if loc.find('Tags') is not None:

                if loc.find('Tags').text is not None:
                    self.locations[lcId].tags = loc.find(
                        'Tags').text.split(';')

        # Read items from the xml element tree.

        for itm in root.iter('ITEM'):
            itId = itm.find('ID').text

            self.items[itId] = Object()
            self.items[itId].title = itm.find('Title').text

            if itm.find('Desc') is not None:
                self.items[itId].desc = itm.find('Desc').text

            if itm.find('AKA') is not None:
                self.items[itId].aka = itm.find('AKA').text

            if itm.find('Tags') is not None:

                if itm.find('Tags').text is not None:
                    self.items[itId].tags = itm.find(
                        'Tags').text.split(';')

        # Read characters from the xml element tree.

        for crt in root.iter('CHARACTER'):
            crId = crt.find('ID').text

            self.characters[crId] = Character()
            self.characters[crId].title = crt.find('Title').text

            if crt.find('Desc') is not None:
                self.characters[crId].desc = crt.find('Desc').text

            if crt.find('AKA') is not None:
                self.characters[crId].aka = crt.find('AKA').text

            if crt.find('Tags') is not None:

                if crt.find('Tags').text is not None:
                    self.characters[crId].tags = crt.find(
                        'Tags').text.split(';')

            if crt.find('Notes') is not None:
                self.characters[crId].notes = crt.find('Notes').text

            if crt.find('Bio') is not None:
                self.characters[crId].bio = crt.find('Bio').text

            if crt.find('Goals') is not None:
                self.characters[crId].goals = crt.find('Goals').text

            if crt.find('FullName') is not None:
                self.characters[crId].fullName = crt.find('FullName').text

            if crt.find('Major') is not None:
                self.characters[crId].isMajor = True

            else:
                self.characters[crId].isMajor = False

        # Read attributes at novel level from the xml element tree.

        prj = root.find('PROJECT')
        self.title = prj.find('Title').text

        if prj.find('AuthorName') is not None:
            self.author = prj.find('AuthorName').text

        if prj.find('Desc') is not None:
            self.desc = prj.find('Desc').text

        self.fieldTitle1 = prj.find('FieldTitle1').text
        self.fieldTitle2 = prj.find('FieldTitle2').text
        self.fieldTitle3 = prj.find('FieldTitle3').text
        self.fieldTitle4 = prj.find('FieldTitle4').text

        # Read attributes at chapter level from the xml element tree.

        for chp in root.iter('CHAPTER'):
            chId = chp.find('ID').text
            self.chapters[chId] = Chapter()
            self.chapters[chId].title = chp.find('Title').text
            self.srtChapters.append(chId)

            if chp.find('Desc') is not None:
                self.chapters[chId].desc = chp.find('Desc').text

            if chp.find('SectionStart') is not None:
                self.chapters[chId].chLevel = 1

            else:
                self.chapters[chId].chLevel = 0

            self.chapters[chId].chType = int(chp.find('Type').text)

            if chp.find('Unused') is not None:
                self.chapters[chId].isUnused = True

            else:
                self.chapters[chId].isUnused = False

            for fields in chp.findall('Fields'):

                if fields.find('Field_SuppressChapterTitle') is not None:

                    if fields.find('Field_SuppressChapterTitle').text == '1':
                        self.chapters[chId].suppressChapterTitle = True

                    else:
                        self.chapters[chId].suppressChapterTitle = False

                if fields.find('Field_IsTrash') is not None:

                    if fields.find('Field_IsTrash').text == '1':
                        self.chapters[chId].isTrash = True

                    else:
                        self.chapters[chId].isTrash = False

                if fields.find('Field_SuppressChapterBreak') is not None:

                    if fields.find('Field_SuppressChapterTitle').text == '0':
                        self.chapters[chId].doNotExport = True

                    else:
                        self.chapters[chId].doNotExport = False

                else:
                    self.chapters[chId].doNotExport = False

            self.chapters[chId].srtScenes = []

            if chp.find('Scenes') is not None:

                if not self.chapters[chId].isTrash:

                    for scn in chp.find('Scenes').findall('ScID'):
                        scId = scn.text
                        self.chapters[chId].srtScenes.append(scId)

        # Read attributes at scene level from the xml element tree.

        for scn in root.iter('SCENE'):
            scId = scn.find('ID').text
            self.scenes[scId] = Scene()
            self.scenes[scId].title = scn.find('Title').text

            if scn.find('Desc') is not None:
                self.scenes[scId].desc = scn.find('Desc').text

            if scn.find('SceneContent') is not None:
                sceneContent = scn.find('SceneContent').text

                if sceneContent is not None:
                    self.scenes[scId].sceneContent = sceneContent

            if scn.find('Unused') is not None:
                self.scenes[scId].isUnused = True

            else:
                self.scenes[scId].isUnused = False

            if scn.find('ExportCondSpecific') is None:
                self.scenes[scId].doNotExport = False

            elif scn.find('ExportWhenRTF') is not None:
                self.scenes[scId].doNotExport = False

            else:
                self.scenes[scId].doNotExport = True

            if scn.find('Status') is not None:
                self.scenes[scId].status = int(scn.find('Status').text)

            if scn.find('Notes') is not None:
                self.scenes[scId].sceneNotes = scn.find('Notes').text

            if scn.find('Tags') is not None:

                if scn.find('Tags').text is not None:
                    self.scenes[scId].tags = scn.find(
                        'Tags').text.split(';')

            if scn.find('Field1') is not None:
                self.scenes[scId].field1 = scn.find('Field1').text

            if scn.find('Field2') is not None:
                self.scenes[scId].field2 = scn.find('Field2').text

            if scn.find('Field3') is not None:
                self.scenes[scId].field3 = scn.find('Field3').text

            if scn.find('Field4') is not None:
                self.scenes[scId].field4 = scn.find('Field4').text

            if scn.find('AppendToPrev') is not None:
                self.scenes[scId].appendToPrev = True

            else:
                self.scenes[scId].appendToPrev = False

            if scn.find('ReactionScene') is not None:
                self.scenes[scId].isReactionScene = True

            else:
                self.scenes[scId].isReactionScene = False

            if scn.find('SubPlot') is not None:
                self.scenes[scId].isSubPlot = True

            else:
                self.scenes[scId].isSubPlot = False

            if scn.find('Goal') is not None:
                self.scenes[scId].goal = scn.find('Goal').text

            if scn.find('Conflict') is not None:
                self.scenes[scId].conflict = scn.find('Conflict').text

            if scn.find('Outcome') is not None:
                self.scenes[scId].outcome = scn.find('Outcome').text

            for crId in scn.find('Characters').iter('CharID'):

                if self.scenes[scId].characters is None:
                    self.scenes[scId].characters = []

                self.scenes[scId].characters.append(crId.text)

            for lcId in scn.find('Locations').iter('LocID'):

                if self.scenes[scId].locations is None:
                    self.scenes[scId].locations = []

                self.scenes[scId].locations.append(lcId.text)

            for itId in scn.find('Items').iter('ItemID'):

                if self.scenes[scId].items is None:
                    self.scenes[scId].items = []

                self.scenes[scId].items.append(itId.text)

        return 'SUCCESS: ' + str(len(self.scenes)) + ' Scenes read from "' + self._filePath + '".'

    def merge(self, novel):
        """Copy selected novel attributes.
        """

        # Merge locations.

        if novel.locations != {}:

            for lcId in novel.locations:

                if novel.locations[lcId].title:
                    # avoids deleting the title, if it is empty by accident
                    self.locations[lcId].title = novel.locations[lcId].title

                if novel.locations[lcId].desc is not None:
                    self.locations[lcId].desc = novel.locations[lcId].desc

                if novel.locations[lcId].aka is not None:
                    self.locations[lcId].aka = novel.locations[lcId].aka

                if novel.locations[lcId].tags is not None:
                    self.locations[lcId].tags = novel.locations[lcId].tags

        # Merge items.

        if novel.items != {}:

            for itId in novel.items:

                if novel.items[itId].title:
                    # avoids deleting the title, if it is empty by accident
                    self.items[itId].title = novel.items[itId].title

                if novel.items[itId].desc is not None:
                    self.items[itId].desc = novel.items[itId].desc

                if novel.items[itId].aka is not None:
                    self.items[itId].aka = novel.items[itId].aka

                if novel.items[itId].tags is not None:
                    self.items[itId].tags = novel.items[itId].tags

        # Merge characters.

        if novel.characters != {}:

            for crId in novel.characters:

                if novel.characters[crId].title:
                    # avoids deleting the title, if it is empty by accident
                    self.characters[crId].title = novel.characters[crId].title

                if novel.characters[crId].desc is not None:
                    self.characters[crId].desc = novel.characters[crId].desc

                if novel.characters[crId].aka is not None:
                    self.characters[crId].aka = novel.characters[crId].aka

                if novel.characters[crId].tags is not None:
                    self.characters[crId].tags = novel.characters[crId].tags

                if novel.characters[crId].notes is not None:
                    self.characters[crId].notes = novel.characters[crId].notes

                if novel.characters[crId].bio is not None:
                    self.characters[crId].bio = novel.characters[crId].bio

                if novel.characters[crId].goals is not None:
                    self.characters[crId].goals = novel.characters[crId].goals

                if novel.characters[crId].fullName is not None:
                    self.characters[crId].fullName = novel.characters[crId].fullName

                if novel.characters[crId].isMajor is not None:
                    self.characters[crId].isMajor = novel.characters[crId].isMajor

        # Merge attributes at novel level.

        if novel.title:
            # avoids deleting the title, if it is empty by accident
            self.title = novel.title

        if novel.desc is not None:
            self.desc = novel.desc

        if novel.author is not None:
            self.author = novel.author

        if novel.fieldTitle1 is not None:
            self.fieldTitle1 = novel.fieldTitle1

        if novel.fieldTitle2 is not None:
            self.fieldTitle2 = novel.fieldTitle2

        if novel.fieldTitle3 is not None:
            self.fieldTitle3 = novel.fieldTitle3

        if novel.fieldTitle4 is not None:
            self.fieldTitle4 = novel.fieldTitle4

        '''Do not modify these items yet:
        
        if novel.srtChapters != []:
            self.srtChapters = novel.srtChapters
            
        '''

        # Merge attributes at chapter level.

        if novel.chapters != {}:

            for chId in novel.chapters:

                if novel.chapters[chId].title:
                    # avoids deleting the title, if it is empty by accident
                    self.chapters[chId].title = novel.chapters[chId].title

                if novel.chapters[chId].desc is not None:
                    self.chapters[chId].desc = novel.chapters[chId].desc

                if novel.chapters[chId].chLevel is not None:
                    self.chapters[chId].chLevel = novel.chapters[chId].chLevel

                if novel.chapters[chId].chType is not None:
                    self.chapters[chId].chType = novel.chapters[chId].chType

                if novel.chapters[chId].isUnused is not None:
                    self.chapters[chId].isUnused = novel.chapters[chId].isUnused

                if novel.chapters[chId].suppressChapterTitle is not None:
                    self.chapters[chId].suppressChapterTitle = novel.chapters[chId].suppressChapterTitle

                if novel.chapters[chId].isTrash is not None:
                    self.chapters[chId].isTrash = novel.chapters[chId].isTrash

                '''Do not modify these items yet:
                
                if novel.chapters[chId].srtScenes != []:
                    self.chapters[chId].srtScenes = novel.chapters[chId].srtScenes

                '''

        # Merge attributes at scene level.

        if novel.scenes != {}:

            for scId in novel.scenes:

                if novel.scenes[scId].title:
                    # avoids deleting the title, if it is empty by accident
                    self.scenes[scId].title = novel.scenes[scId].title

                if novel.scenes[scId].desc is not None:
                    self.scenes[scId].desc = novel.scenes[scId].desc

                if novel.scenes[scId].sceneContent is not None:
                    self.scenes[scId].sceneContent = novel.scenes[scId].sceneContent

                if novel.scenes[scId].isUnused is not None:
                    self.scenes[scId].isUnused = novel.scenes[scId].isUnused

                if novel.scenes[scId].status is not None:
                    self.scenes[scId].status = novel.scenes[scId].status

                if novel.scenes[scId].sceneNotes is not None:
                    self.scenes[scId].sceneNotes = novel.scenes[scId].sceneNotes

                if novel.scenes[scId].tags is not None:
                    self.scenes[scId].tags = novel.scenes[scId].tags

                if novel.scenes[scId].field1 is not None:
                    self.scenes[scId].field1 = novel.scenes[scId].field1

                if novel.scenes[scId].field2 is not None:
                    self.scenes[scId].field2 = novel.scenes[scId].field2

                if novel.scenes[scId].field3 is not None:
                    self.scenes[scId].field3 = novel.scenes[scId].field3

                if novel.scenes[scId].field4 is not None:
                    self.scenes[scId].field4 = novel.scenes[scId].field4

                if novel.scenes[scId].appendToPrev is not None:
                    self.scenes[scId].appendToPrev = novel.scenes[scId].appendToPrev

                if novel.scenes[scId].isReactionScene is not None:
                    self.scenes[scId].isReactionScene = novel.scenes[scId].isReactionScene

                if novel.scenes[scId].isSubPlot is not None:
                    self.scenes[scId].isSubPlot = novel.scenes[scId].isSubPlot

                if novel.scenes[scId].goal is not None:
                    self.scenes[scId].goal = novel.scenes[scId].goal

                if novel.scenes[scId].conflict is not None:
                    self.scenes[scId].conflict = novel.scenes[scId].conflict

                if novel.scenes[scId].outcome is not None:
                    self.scenes[scId].outcome = novel.scenes[scId].outcome

                if novel.scenes[scId].characters is not None:
                    self.scenes[scId].characters = []

                    for crId in novel.scenes[scId].characters:

                        if crId in self.characters:
                            self.scenes[scId].characters.append(crId)

                if novel.scenes[scId].locations is not None:
                    self.scenes[scId].locations = []

                    for lcId in novel.scenes[scId].locations:

                        if lcId in self.locations:
                            self.scenes[scId].locations.append(lcId)

                if novel.scenes[scId].items is not None:
                    self.scenes[scId].items = []

                    for itId in novel.scenes[scId].items:

                        if itId in self.items:
                            self.scenes[scId].append(crId)

    def write(self):
        """Open the yWriter xml file located at filePath and 
        replace a set of attributes not being None.
        Return a message beginning with SUCCESS or ERROR.
        """

        root = self._tree.getroot()

        # Write locations to the xml element tree.

        for loc in root.iter('LOCATION'):
            lcId = loc.find('ID').text

            if lcId in self.locations:

                if self.locations[lcId].title is not None:
                    loc.find('Title').text = self.locations[lcId].title

                if self.locations[lcId].desc is not None:

                    if loc.find('Desc') is None:
                        ET.SubElement(
                            loc, 'Desc').text = self.locations[lcId].desc

                    else:
                        loc.find('Desc').text = self.locations[lcId].desc

                if self.locations[lcId].aka is not None:

                    if loc.find('AKA') is None:
                        ET.SubElement(
                            loc, 'AKA').text = self.locations[lcId].aka

                    else:
                        loc.find('AKA').text = self.locations[lcId].aka

                if self.locations[lcId].tags is not None:

                    if loc.find('Tags') is None:
                        ET.SubElement(loc, 'Tags').text = ';'.join(
                            self.locations[lcId].tags)

                    else:
                        loc.find('Tags').text = ';'.join(
                            self.locations[lcId].tags)

        # Write items to the xml element tree.

        for itm in root.iter('ITEM'):
            itId = itm.find('ID').text

            if itId in self.items:

                if self.items[itId].title is not None:
                    itm.find('Title').text = self.items[itId].title

                if self.items[itId].desc is not None:

                    if itm.find('Desc') is None:
                        ET.SubElement(itm, 'Desc').text = self.items[itId].desc

                    else:
                        itm.find('Desc').text = self.items[itId].desc

                if self.items[itId].aka is not None:

                    if itm.find('AKA') is None:
                        ET.SubElement(itm, 'AKA').text = self.items[itId].aka

                    else:
                        itm.find('AKA').text = self.items[itId].aka

                if self.items[itId].tags is not None:

                    if itm.find('Tags') is None:
                        ET.SubElement(itm, 'Tags').text = ';'.join(
                            self.items[itId].tags)

                    else:
                        itm.find('Tags').text = ';'.join(
                            self.items[itId].tags)

        # Write characters to the xml element tree.

        for crt in root.iter('CHARACTER'):
            crId = crt.find('ID').text

            if crId in self.characters:

                if self.characters[crId].title is not None:
                    crt.find('Title').text = self.characters[crId].title

                if self.characters[crId].desc is not None:

                    if crt.find('Desc') is None:
                        ET.SubElement(
                            crt, 'Desc').text = self.characters[crId].desc

                    else:
                        crt.find('Desc').text = self.characters[crId].desc

                if self.characters[crId].aka is not None:

                    if crt.find('AKA') is None:
                        ET.SubElement(
                            crt, 'AKA').text = self.characters[crId].aka

                    else:
                        crt.find('AKA').text = self.characters[crId].aka

                if self.characters[crId].tags is not None:

                    if crt.find('Tags') is None:
                        ET.SubElement(crt, 'Tags').text = ';'.join(
                            self.characters[crId].tags)

                    else:
                        crt.find('Tags').text = ';'.join(
                            self.characters[crId].tags)

                if self.characters[crId].notes is not None:

                    if crt.find('Notes') is None:
                        ET.SubElement(
                            crt, 'Notes').text = self.characters[crId].notes

                    else:
                        crt.find(
                            'Notes').text = self.characters[crId].notes

                if self.characters[crId].bio is not None:

                    if crt.find('Bio') is None:
                        ET.SubElement(
                            crt, 'Bio').text = self.characters[crId].bio

                    else:
                        crt.find('Bio').text = self.characters[crId].bio

                if self.characters[crId].goals is not None:

                    if crt.find('Goals') is None:
                        ET.SubElement(
                            crt, 'Goals').text = self.characters[crId].goals

                    else:
                        crt.find(
                            'Goals').text = self.characters[crId].goals

                if self.characters[crId].fullName is not None:

                    if crt.find('FullName') is None:
                        ET.SubElement(
                            crt, 'FullName').text = self.characters[crId].fullName

                    else:
                        crt.find(
                            'FullName').text = self.characters[crId].fullName

                majorMarker = crt.find('Major')

                if majorMarker is not None:

                    if not self.characters[crId].isMajor:
                        crt.remove(majorMarker)

                else:
                    if self.characters[crId].isMajor:
                        ET.SubElement(crt, 'Major').text = '-1'

        # Write attributes at novel level to the xml element tree.

        prj = root.find('PROJECT')
        prj.find('Title').text = self.title

        if self.desc is not None:

            if prj.find('Desc') is None:
                ET.SubElement(prj, 'Desc').text = self.desc

            else:
                prj.find('Desc').text = self.desc

        if self.author is not None:

            if prj.find('AuthorName') is None:
                ET.SubElement(prj, 'AuthorName').text = self.author

            else:
                prj.find('AuthorName').text = self.author

        prj.find('FieldTitle1').text = self.fieldTitle1
        prj.find('FieldTitle2').text = self.fieldTitle2
        prj.find('FieldTitle3').text = self.fieldTitle3
        prj.find('FieldTitle4').text = self.fieldTitle4

        # Write attributes at chapter level to the xml element tree.

        for chp in root.iter('CHAPTER'):
            chId = chp.find('ID').text

            if chId in self.chapters:
                chp.find('Title').text = self.chapters[chId].title

                if self.chapters[chId].desc is not None:

                    if chp.find('Desc') is None:
                        ET.SubElement(
                            chp, 'Desc').text = self.chapters[chId].desc

                    else:
                        chp.find('Desc').text = self.chapters[chId].desc

                levelInfo = chp.find('SectionStart')

                if levelInfo is not None:

                    if self.chapters[chId].chLevel == 0:
                        chp.remove(levelInfo)

                chp.find('Type').text = str(self.chapters[chId].chType)

                if self.chapters[chId].isUnused:

                    if chp.find('Unused') is None:
                        ET.SubElement(chp, 'Unused').text = '-1'

                elif chp.find('Unused') is not None:
                    chp.remove(chp.find('Unused'))

        # Write attributes at scene level to the xml element tree.

        for scn in root.iter('SCENE'):
            scId = scn.find('ID').text

            if scId in self.scenes:

                if self.scenes[scId].title is not None:
                    scn.find('Title').text = self.scenes[scId].title

                if self.scenes[scId].desc is not None:

                    if scn.find('Desc') is None:
                        ET.SubElement(
                            scn, 'Desc').text = self.scenes[scId].desc

                    else:
                        scn.find('Desc').text = self.scenes[scId].desc

                if self.scenes[scId]._sceneContent is not None:
                    scn.find(
                        'SceneContent').text = replace_unsafe_glyphs(self.scenes[scId]._sceneContent)
                    scn.find('WordCount').text = str(
                        self.scenes[scId].wordCount)
                    scn.find('LetterCount').text = str(
                        self.scenes[scId].letterCount)

                if self.scenes[scId].isUnused:

                    if scn.find('Unused') is None:
                        ET.SubElement(scn, 'Unused').text = '-1'

                elif scn.find('Unused') is not None:
                    scn.remove(scn.find('Unused'))

                if self.scenes[scId].status is not None:
                    scn.find('Status').text = str(self.scenes[scId].status)

                if self.scenes[scId].sceneNotes is not None:

                    if scn.find('Notes') is None:
                        ET.SubElement(
                            scn, 'Notes').text = self.scenes[scId].sceneNotes

                    else:
                        scn.find(
                            'Notes').text = self.scenes[scId].sceneNotes

                if self.scenes[scId].tags is not None:

                    if scn.find('Tags') is None:
                        ET.SubElement(scn, 'Tags').text = ';'.join(
                            self.scenes[scId].tags)

                    else:
                        scn.find('Tags').text = ';'.join(
                            self.scenes[scId].tags)

                if self.scenes[scId].field1 is not None:

                    if scn.find('Field1') is None:
                        ET.SubElement(
                            scn, 'Field1').text = self.scenes[scId].field1

                    else:
                        scn.find('Field1').text = self.scenes[scId].field1

                if self.scenes[scId].field2 is not None:

                    if scn.find('Field2') is None:
                        ET.SubElement(
                            scn, 'Field2').text = self.scenes[scId].field2

                    else:
                        scn.find('Field2').text = self.scenes[scId].field2

                if self.scenes[scId].field3 is not None:

                    if scn.find('Field3') is None:
                        ET.SubElement(
                            scn, 'Field3').text = self.scenes[scId].field3

                    else:
                        scn.find('Field3').text = self.scenes[scId].field3

                if self.scenes[scId].field4 is not None:

                    if scn.find('Field4') is None:
                        ET.SubElement(
                            scn, 'Field4').text = self.scenes[scId].field4

                    else:
                        scn.find('Field4').text = self.scenes[scId].field4

                if self.scenes[scId].appendToPrev:

                    if scn.find('AppendToPrev') is None:
                        ET.SubElement(scn, 'AppendToPrev').text = '-1'

                elif scn.find('AppendToPrev') is not None:
                    scn.remove(scn.find('AppendToPrev'))

                if self.scenes[scId].isReactionScene:

                    if scn.find('ReactionScene') is None:
                        ET.SubElement(scn, 'ReactionScene').text = '-1'

                elif scn.find('ReactionScene') is not None:
                    scn.remove(scn.find('ReactionScene'))

                if self.scenes[scId].isSubPlot:

                    if scn.find('SubPlot') is None:
                        ET.SubElement(scn, 'SubPlot').text = '-1'

                elif scn.find('SubPlot') is not None:
                    scn.remove(scn.find('SubPlot'))

                if self.scenes[scId].goal is not None:

                    if scn.find('Goal') is None:
                        ET.SubElement(
                            scn, 'Goal').text = self.scenes[scId].goal

                    else:
                        scn.find('Goal').text = self.scenes[scId].goal

                if self.scenes[scId].conflict is not None:

                    if scn.find('Conflict') is None:
                        ET.SubElement(
                            scn, 'Conflict').text = self.scenes[scId].conflict

                    else:
                        scn.find(
                            'Conflict').text = self.scenes[scId].conflict

                if self.scenes[scId].outcome is not None:

                    if scn.find('Outcome') is None:
                        ET.SubElement(
                            scn, 'Outcome').text = self.scenes[scId].outcome

                    else:
                        scn.find(
                            'Outcome').text = self.scenes[scId].outcome

                if self.scenes[scId].characters is not None:
                    characters = scn.find('Characters')

                    for oldCrId in characters.findall('CharID'):
                        characters.remove(oldCrId)

                    for crId in self.scenes[scId].characters:
                        ET.SubElement(characters, 'CharID').text = crId

                if self.scenes[scId].locations is not None:
                    locations = scn.find('Locations')

                    for oldLcId in locations.findall('LocID'):
                        locations.remove(oldLcId)

                    for lcId in self.scenes[scId].locations:
                        ET.SubElement(locations, 'LocID').text = lcId

                if self.scenes[scId].items is not None:
                    items = scn.find('Items')

                    for oldItId in items.findall('ItemID'):
                        items.remove(oldItId)

                    for itId in self.scenes[scId].items:
                        ET.SubElement(items, 'ItemID').text = itId

        # Pretty print the xml tree.

        indent(root)

        # Save the xml tree in a file.

        self._tree = ET.ElementTree(root)

        try:
            self._tree.write(
                self._filePath, xml_declaration=False, encoding=self._ENCODING)

        except(PermissionError):
            return 'ERROR: "' + self._filePath + '" is write protected.'

        # Postprocess the xml file created by ElementTree.

        message = xml_postprocess(
            self._filePath, self._ENCODING, self._cdataTags)

        if message.startswith('ERROR'):
            return message

        return 'SUCCESS: project data written to "' + self._filePath + '".'

    def is_locked(self):
        """Test whether a .lock file placed by yWriter exists.
        """
        if os.path.isfile(self._filePath + '.lock'):
            return True

        else:
            return False


SUFFIX = ''
# File name suffix for the exported odt file.
# Example:
# foo.yw7 --> foo_exp.odt


def main():
    sourcePath = None

    files = os.listdir('.')

    for file in files:

        if file.endswith('.yw7'):
            sourcePath = file
            break

    if not sourcePath:

        for file in files:

            if file.endswith('.yw6'):
                sourcePath = file
                break

    if sourcePath is None:
        return 'ERROR: No yWriter project found.'

    print('Export yWriter scenes content to odt')
    print('Project: "' + sourcePath + '"')
    ywFile = YwFile(sourcePath)

    if ywFile.is_locked():
        return 'ERROR: yWriter seems to be open. Please close first.'

    message = ywFile.read()

    if message.startswith('ERROR'):
        return message

    fileName, fileExtension = os.path.splitext(sourcePath)
    document = OdtFile(fileName + SUFFIX + '.odt')
    document.comments = True
    document.merge(ywFile)
    message = document.write()
    return message


if __name__ == '__main__':
    message = main()
    print(message)