[Project homepage](https://peter88213.github.io/yW2OO)

------------------------------------------------------------------

## Command reference

-   [Manuscript without tags](#manuscript-without-tags)
-   [Manuscript with visible tags for proof reading](#manuscript-with-visible-tags-for-proof-reading)
-   [Manuscript for editing](#manuscript-for-editing)
-   [Scene descriptions for editing](#scene-descriptions-for-editing)
-   [Chapter descriptions for editing](#chapter-descriptions-for-editing)
-   [Part descriptions for editing](#part-descriptions-for-editing)
-   [Character list](#character-list)
-   [Location list](#location-list)
-   [Item list](#item-list)
-   [Character descriptions for editing](#character-descriptions-for-editing)
-   [Location descriptions for editing](#location-descriptions-for-editing)
-   [Item descriptions for editing](#item-descriptions-for-editing)
-   [Scene list for editing](#scene-list)
-   [Notes chapters for editing](#notes-chapters-for-editing)
-   [Todo chapters for editing](#todo-chapters-for-editing)
-   [Brief synopsis](#brief-synopsis)
-   [Cross references](#cross-references)


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


# Command reference

## Manuscript without tags

This will write yWriter 7 chapters and scenes into a new OpenDocument
text document (odt).

-   The document is placed in the same folder as the yWriter project.
-   Document's **filename**: `<yW project name>.odt`.
-   Text markup: Bold and italics are supported. Other highlighting such
    as underline and strikethrough are lost.
-   Only "normal" chapters and scenes are exported. Chapters and
    scenes marked "unused", "todo" or "notes" are not exported.
-   Only scenes that are intended for RTF export in yWriter will be
    exported.
-   Scenes beginning with `<HTML>` or `<TEX>` are not exported.
-   Comments in the text bracketed with slashes and asterisks (like
    `/* this is a comment */`) are converted to author's comments.
-   Interspersed HTML, TEX, or RTF commands are removed.
-   Gobal variables and project variables are not resolved.
-   Chapter titles appear as first level heading if the chapter is
    marked as beginning of a new section in yWriter. Such headings are
    considered as "part" headings.
-   Chapter titles appear as second level heading if the chapter is not
    marked as beginning of a new section. Such headings are considered
    as "chapter" headings.
-   Scene titles appear as navigable comments pinned to the beginning of
    the scene.
-   Scenes are separated by `* * *`. The first line is not
    indented. You can replace the scene separators by blank lines with 
    the menu command **Format >  Replace scene dividers with blank lines**.
-   Starting from the second paragraph, paragraphs begin with
    indentation of the first line.
-   Scenes marked "attach to previous scene" in yWriter appear like
    continuous paragraphs.
-   Paragraphs starting with `> ` are formatted as quotations.


[Top of page](#top)

------------------------------------------------------------------------

## Manuscript with visible tags for proof reading

This will write yWriter 7 chapters and scenes into a new OpenDocument
text document (odt) with chapter and scene markers. File name suffix is
`_proof`.

-   The proof read document is placed in the same folder as the yWriter
    project.
-   Document's filename: `<yW project name>_proof.odt`.
-   Text markup: Bold and italics are supported. Other highlighting such
    as underline and strikethrough are lost.
-   Scenes beginning with `<HTML>` or `<TEX>` are not exported.
-   All other chapters and scenes are exported, whether "used" or
    "unused".
-   Interspersed HTML, TEX, or RTF commands are taken over unchanged.
-   The document contains chapter `[ChID:x]` and scene `[ScID:y]`
    markers according to yWriter 5 standard. **Do not touch lines
    containing the markers** if you want to be able to write the
    document back into yWriter.
-   Chapters and scenes can neither be rearranged nor deleted. 
-   You can split scenes by inserting headings or a scene divider:
    -  *Heading 1* --› New chapter title (beginning a new section).
    -  *Heading 2* --› New chapter title.
    -  `###` --› Scene divider. Optionally, you can append the 
       scene title to the scene divider.


[Top of page](#top)

------------------------------------------------------------------------

## Manuscript for editing

This will write yWriter 7 chapters and scenes into a new OpenDocument
text document (odt) with invisible chapter and scene sections (to be
seen in the Navigator). File name suffix is `_manuscript`.

-   Only "normal" chapters and scenes are exported. Chapters and
    scenes marked "unused", "todo" or "notes" are not exported.
-   Scenes beginning with `<HTML>` or `<TEX>` are not exported.
-   Comments within scenes are written back as scene titles 
    if surrounded by `~`.
-   Comments in the text bracketed with slashes and asterisks (like
    `/* this is a comment */`) are converted to author's comments.
-   Interspersed HTML, TEX, or RTF commands are taken over unchanged.
-   Gobal variables and project variables are not resolved.
-   Chapters and scenes can neither be rearranged nor deleted.
-   You can split scenes by inserting headings or a scene divider:
    -  *Heading 1* --› New chapter title (beginning a new section).
    -  *Heading 2* --› New chapter title.
    -  `###` --› Scene divider. Optionally, you can also append the 
       scene title to the scene divider.

[Top of page](#top)

------------------------------------------------------------------------


## Scene descriptions for editing

This will generate a new OpenDocument text document (odt) containing a
**full synopsis** with chapter titles and scene descriptions that can be
edited and written back to yWriter format. File name suffix is
`_scenes`.



[Top of page](#top)

------------------------------------------------------------------------

## Chapter descriptions for editing

This will generate a new OpenDocument text document (odt) containing a
**brief synopsis** with chapter titles and chapter descriptions that can
be edited and written back to yWriter format. File name suffix is
`_chapters`.

**Note:** Doesn't apply to chapters marked
`This chapter begins a new section` in yWriter.



[Top of page](#top)

------------------------------------------------------------------------

## Part descriptions for editing

This will generate a new OpenDocument text document (odt) containing a
**very brief synopsis** with part titles and part descriptions that can
be edited and written back to yWriter format. File name suffix is
`_parts`.

**Note:** Applies only to chapters marked
`This chapter  begins a new section` in yWriter.



[Top of page](#top)

------------------------------------------------------------------------

## Character list

This will generate a new OpenDocument spreadsheet (ods) containing a
character list that can be edited in Office Calc and written back to
yWriter format. File name suffix is `_charlist`.

You may change the sort order of the rows. You may also add or remove
rows. New entities must get a unique ID.



[Top of page](#top)

------------------------------------------------------------------------

## Location list

This will generate a new OpenDocument spreadsheet (ods) containing a
location list that can be edited in Office Calc and written back to
yWriter format. File name suffix is `_loclist`.

You may change the sort order of the rows. You may also add or remove
rows. New entities must get a unique ID.



[Top of page](#top)

------------------------------------------------------------------------

## Item list

This will generate a new OpenDocument spreadsheet (ods) containing an
item list that can be edited in Office Calc and written back to yWriter
format. File name suffix is `_itemlist`.

You may change the sort order of the rows. You may also add or remove
rows. New entities must get a unique ID.



[Top of page](#top)

------------------------------------------------------------------------

## Cross references

This will generate a new OpenDocument text document (odt) containing
navigable cross references. File name suffix is `_xref`. The cross
references are:

-   Scenes per character,
-   scenes per location,
-   scenes per item,
-   scenes per tag,
-   characters per tag,
-   locations per tag,
-   items per tag.



[Top of page](#top)

------------------------------------------------------------------------

## Character descriptions for editing

This will generate a new OpenDocument text document (odt) containing
character descriptions, bio, goals, and notes that can be edited in Office
Writer and written back to yWriter format. File name suffix is
`_characters`.



[Top of page](#top)

------------------------------------------------------------------------

## Location descriptions for editing

This will generate a new OpenDocument text document (odt) containing
location descriptions that can be edited in Office Writer and written
back to yWriter format. File name suffix is `_locations`.



[Top of page](#top)

------------------------------------------------------------------------

## Item descriptions for editing

This will generate a new OpenDocument text document (odt) containing
item descriptions that can be edited in Office Writer and written back
to yWriter format. File name suffix is `_items`.



[Top of page](#top)

------------------------------------------------------------------------

## Scene list

This will generate a new OpenDocument spreadsheet (ods) listing the following:

- Hyperlink to the manuscript's scene section
- Scene title
- Scene description
- Tags
- Scene notes
- A/R
- Goal
- Conflict
- Outcome
- Sequential scene number
- Words total
- Rating 1
- Rating 2
- Rating 3
- Rating 4
- Word count
- Letter count
- Status
- Characters
- Locations
- Items

Only "normal" scenes that would be exported as RTF in yWriter get a 
row in the scene list. Scenes of the "Unused", "Notes", or "ToDo" 
type are omitted.

Scenes beginning with `<HTML>` or `<TEX>` are omitted.

File name suffix is `_scenelist`.


[Top of page](#top)

------------------------------------------------------------------------

## Notes chapters for editing

This will write yWriter 7 "Notes" chapters with child scenes into a new 
OpenDocument text document (odt) with invisible chapter and scene 
sections (to be seen in the Navigator). File name suffix is `_notes`.

-  Comments within scenes are written back as scene titles
   if surrounded by `~`.
-  Chapters and scenes can neither be rearranged nor deleted.
-  Scenes can be split by inserting headings or a scene divider:
    -  *Heading 1* --› New chapter title (beginning a new section).
    -  *Heading 2* --› New chapter title.
    -  `###` --› Scene divider. Optionally, you can append the 
       scene title to the scene divider.


[Top of page](#top)

------------------------------------------------------------------------

## Todo chapters for editing

This will write yWriter 7 "Todo" chapters with child scenes into a new 
OpenDocument text document (odt) with invisible chapter and scene 
sections (to be seen in the Navigator). File name suffix is `_todo`.

-  Comments within scenes are written back as scene titles
   if surrounded by `~`.
-  Chapters and scenes can neither be rearranged nor deleted.
-  Scenes can be split by inserting headings or a scene divider:
    -  *Heading 1* --› New chapter title (beginning a new section).
    -  *Heading 2* --› New chapter title.
    -  `###` --› Scene divider. Optionally, you can append the 
       scene title to the scene divider.


[Top of page](#top)

------------------------------------------------------------------------

## Brief synopsis

This will write a brief synopsis with chapter and scenes titles into a new 
OpenDocument text document.  File name suffix is `_brf_synopsis`.
 
-   Only "normal" chapters and scenes are exported. Chapters and
    scenes marked "unused", "todo" or "notes" are not exported.
-   Only scenes that are intended for RTF export in yWriter will be
    exported.
-   Titles of scenes beginning with `<HTML>` or `<TEX>` are not exported.
-   Chapter titles appear as first level heading if the chapter is
    marked as beginning of a new section in yWriter. Such headings are
    considered as "part" headings.
-   Chapter titles appear as second level heading if the chapter is not
    marked as beginning of a new section. Such headings are considered
    as "chapter" headings.
-   Scene titles appear as plain paragraphs.



[Top of page](#top)

------------------------------------------------------------------------

## Cross references

This will generate a new OpenDocument text document (odt) containing
navigable cross references. File name suffix is `_xref`. The cross
references are:

-   Scenes per character,
-   scenes per location,
-   scenes per item,
-   scenes per tag,
-   characters per tag,
-   locations per tag,
-   items per tag.



[Top of page](#top)

------------------------------------------------------------------------


## Installation path

The **setup.py** installation script installs *yw2oo.pyw* in the user profile. This is the OptioOptioOptionally, you can appendter\yw2oo`

