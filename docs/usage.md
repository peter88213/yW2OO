[Project homepage](https://peter88213.github.io/yW2OO)

------------------------------------------------------------------

## Command reference

-   [Export to odt](#export-to-odt)
-   [Brief synopsis](#brief-synopsis)
-   [Proof reading](#proof-reading)
-   [Manuscript](#manuscript)
-   [Scene descriptions](#scene-descriptions)
-   [Chapter descriptions](#chapter-descriptions)
-   [Part descriptions](#part-descriptions)
-   [Character list](#character-list)
-   [Location list](#location-list)
-   [Item list](#item-list)
-   [Cross references](#cross-references)
-   [Character descriptions](#character-descriptions)
-   [Location descriptions](#location-descriptions)
-   [Item descriptions](#item-descriptions)
-   [Scene list](#scene-list)
-   [Plot list](#plot-list)


yWriter to OpenOffice/LibreOffice converter - yWriter export to odt/ods documents. 

# Instructions for use

## How to install yW2OO

1. If you have already installed an older version of yW2OO, please run the uninstaller for it. 

2. Unzip `yW2OO_<version number>.zip` within your user profile.

3. Move into the `yW2OO_<version number>` folder and run `setup.pyw` (double click).
   This will copy all needed files to the right places. 
   
4. If everything works well, an Explorer window will open, showing the installation folder.
   Now, add the context menu entries by double-clicking  `add_context_menu.reg`. 
   You may be asked for approval to modify  the Windows registry. Please accept.

You can remove the context menu entries by double-clicking  `rem_context_menu.reg`.

Please note that these context menus depend on the currently installed Python version. After a major Python update you may need to run the setup program again and renew the registry entries.

## How to use yW2OO

1. Move into your yWriter project folder, and right-click your .yw6 or .yw7 project file. 
   In the context menu, choose `Export to OpenOffice`. 
   
2. A sub menu with document types will open. Select the desired one.

3. If everything goes well, a success message pops up. The newly created file is located 
   in the same folder as your yWriter project. If you want to edit your new document immediately, 
   just click on the `open` button. 


## How to uninstall yW2OO

Move into the installation folder `~\.yw2oo` and double click on `rem_context_menu.reg`. 
You may be asked for approval to modify the registry. Please accept to remove the Explorer context
menu entry. 


# Command reference

## Export to odt

This will load yWriter 7 chapters and scenes into a new OpenDocument
text document (odt).

-   The document is placed in the same folder as the yWriter project.
-   Document's **filename**: `<yW project name>.odt`.
-   Text markup: Bold and italics are supported. Other highlighting such
    as underline and strikethrough are lost.
-   Only "normal" chapters and scenes are exported. Chapters and
    scenes marked "unused", "todo" or "notes" are not exported.
-   Only scenes that are intended for RTF export in yWriter will be
    exported.
-   Comments in the text bracketed with slashes and asterisks (like
    `/* this is a comment */`) are converted to author's comments.
-   Interspersed HTML, TEX, or RTF commands are taken over unchanged.
-   Gobal variables and project variables are not resolved.
-   Chapter titles appear as first level heading if the chapter is
    marked as beginning of a new section in yWriter. Such headings are
    considered as "part" headings.
-   Chapter titles appear as second level heading if the chapter is not
    marked as beginning of a new section. Such headings are considered
    as "chapter" headings.
-   Scene titles appear as navigable comments pinned to the beginning of
    the scene.
-   Usually, scenes are separated by blank lines. The first line is not
    indented.
-   Starting from the second paragraph, paragraphs begin with
    indentation of the first line.
-   Scenes marked "attach to previous scene" in yWriter appear like
    continuous paragraphs.



[Top of page](#top)

------------------------------------------------------------------------

## Brief synopsis

This will load a brief synopsis with chapter and scenes titles into a new
 OpenDocument text document (odt).

-   The document is placed in the same folder as the yWriter project.
-   Document's **filename**: `<yW project name_brf_synopsis>.odt`.
-   Only "normal" chapters and scenes are exported. Chapters and
    scenes marked "unused", "todo" or "notes" are not exported.
-   Only scenes that are intended for RTF export in yWriter will be
    exported.
-   Chapter titles appear as first level heading if the chapter is
    marked as beginning of a new section in yWriter. Such headings are
    considered as "part" headings.
-   Chapter titles appear as second level heading if the chapter is not
    marked as beginning of a new section. Such headings are considered
    as "chapter" headings.
-   Scene titles appear as plain paragraphs.



[Top of page](#top)

------------------------------------------------------------------------

## Proof reading

This will load yWriter 7 chapters and scenes into a new OpenDocument
text document (odt) with chapter and scene markers. File name suffix is
`_proof`.

-   The proof read document is placed in the same folder as the yWriter
    project.
-   Document's filename: `<yW project name>_proof.odt`.
-   Text markup: Bold and italics are supported. Other highlighting such
    as underline and strikethrough are lost.
-   All chapters and scenes will be exported, whether "used" or
    "unused".
-   The document contains chapter `[ChID:x]` and scene `[ScID:y]`
    markers according to yWriter 5 standard. **Do not touch lines
    containing the markers** if you want to be able to reimport the
    document into yWriter.
-   Back up your yWriter project and close yWriter before.



[Top of page](#top)

------------------------------------------------------------------------

## Manuscript

This will load yWriter 7 chapters and scenes into a new OpenDocument
text document (odt) with invisible chapter and scene sections (to be
seen in the Navigator). File name suffix is `_manuscript`.



[Top of page](#top)

------------------------------------------------------------------------

## Scene descriptions

This will generate a new OpenDocument text document (odt) containing a
**full synopsis** with chapter titles and scene descriptions that can be
edited and written back to yWriter format. File name suffix is
`_scenes`.



[Top of page](#top)

------------------------------------------------------------------------

## Chapter descriptions

This will generate a new OpenDocument text document (odt) containing a
**brief synopsis** with chapter titles and chapter descriptions that can
be edited and written back to yWriter format. File name suffix is
`_chapters`.

**Note:** Doesn't apply to chapters marked
`This chapter begins a new section` in yWriter.



[Top of page](#top)

------------------------------------------------------------------------

## Part descriptions

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

## Character descriptions

This will generate a new OpenDocument text document (odt) containing
character descriptions, bio, goals, and notes that can be edited in Office
Writer and written back to yWriter format. File name suffix is
`_characters`.



[Top of page](#top)

------------------------------------------------------------------------

## Location descriptions

This will generate a new OpenDocument text document (odt) containing
location descriptions that can be edited in Office Writer and written
back to yWriter format. File name suffix is `_locations`.



[Top of page](#top)

------------------------------------------------------------------------

## Item descriptions

This will generate a new OpenDocument text document (odt) containing
item descriptions that can be edited in Office Writer and written back
to yWriter format. File name suffix is `_items`.



[Top of page](#top)

------------------------------------------------------------------------

## Scene list

This will generate a new OpenDocument spreadsheet (ods) listing scene
title, scene descriptions, and links to the manuscript's scene
sections. Further scene metadata (e.g. tags, goals, time), if any. File
name suffix is `_scenelist`.



[Top of page](#top)

------------------------------------------------------------------------

## Plot list

This will generate a new OpenDocument spreadsheet (ods) listing plot
related metadata that can be displayed and edited. File name suffix is
`_plotlist`.

### Plotting conventions

In yWriter, you can divide your novel into **Plot Sections** (e.g. acts
or steps) by inserting "Notes" chapters. They will show up in
blue color and won't get exported.

**Plot-related events** (e.g. "Mid Point", "Climax") can be
identified by "scene tags" if you want to link them to a specific
scene.

You can use scene notes for **plot-specific explanations**.

If you want to **visualize character arcs**, you can use the project's
rating names by changing them to the names of up to four main
characters. Then you can quantify the state of these four characters and
put them into the scenes. It's easy then to let OpenOffice Calc show a
diagram for the scene ratings over scene count or word count.

-   Only rating field names corresponding to character names or
    containing the string "story", e.g. "A-Story", "BStoryline"
    (up to 10 case insensitive characters) appear in the plot list.
-   Only ratings greater than 1 appear in the plot list, i.e. 1 means
    "a rating is not set for this chapter".
-   Recommended ratings:
    -   1 = N/A
    -   2 = unhappy
    -   3 = dissatisfied
    -   4 = vague
    -   5 = satisfied
    -   6 = happy
-   Ratings deleted while editing the plotlist will be converted to 1 on
    writing back.



[Top of page](#top)

------------------------------------------------------------------------

## Installation path

The **setup.py** installation script installs *yw2oo.pyw* in the user profile. This is the installation path: 

`c:\Users\<user name>\.pywriter\yw2oo`

