[Project homepage](../index) > [Instructions for use](../usage) > Command reference: Import

--- 

# Import

**Import from ODT/ODS to yWriter**

This writes back the document's content to the yWriter project file.

-   Make sure not to change a generated document's file name before
    writing back to yWriter format.
-   The yWriter 7 project to rewrite must exist in the same folder as
    the document.
-   If the document's file name has no suffix, the document is
    considered a [Work in
    progress](#how-to-set-up-a-work-in-progress-for-export) or an
    [Outline](#how-to-set-up-an-outline-for-export) to be exported into
    a newly created yWriter project. **Note:** Existing yWriter projects
    will not be overwritten.



[About formatting text](#about-formatting-text)

[About document language handling](#about-document-language-handling)

[How to set up a work in progress for export](#how-to-set-up-a-work-in-progress-for-export)

[How to set up an outline for export](#how-to-set-up-an-outline-for-export)

--- 

## General

### About formatting text

It is assumed that very few types of text markup are needed for a fictional text:

- *Emphasized* (usually shown as italics).
- *Strongly emphasized* (usually shown as capitalized).
- *Citation* (paragraph visually distinguished from body text).

When importing to yw7 format, the converter replaces these formattings as follows: 

- Text formatted as *Emphasized* is *italics* in yWriter.
- Text formatted as *Strongly emphasized* is *Bold* in yWriter. 
- Paragraphs formatted as *Quote*  starting with `"> "` in yWriter.


### About document language handling

ODF documents are generally assigned a language that determines spell checking and country-specific character substitutions. In addition, Office Writer lets you assign text passages to languages other than the document language to mark foreign language usage or to suspend spell checking. 

#### Document overall

- If a document language (Language code acc. to ISO 639-1 and country code acc. to ISO 3166-2) is detected in the source document during conversion to yw7 format, these codes are set as yWriter project variables. 

- If language code and country code exist as project variables during conversion from yw7 format, they are inserted into the generated ODF document. 

- If no language and country code exist as project variables when converting from yw7 format, language and country code from the operating system settings are entered into the generated ODF document. 

- The language and country codes are checked superficially. If they obviously do not comply with the ISO standards, they are replaced by the values for "No language". These are:
    - Language = zxx
    - Country = none

#### Text passages in scenes

If text markups for other languages are detected during conversion to the yw7 format, they are converted and transferred to the yWriter scene. 

This then looks like this, for example:

`xxx xxxx [lang=en-AU]yyy yyyy yyyy[/lang=en-AU] xxx xxx` 

To prevent these text markups from interfering with *yWriter*, they are automatically set as project variables in such a way that *yWriter* interprets them as HTML instructions during document export. 

For the example shown above, the project variable definition for the opening tag looks like this: 

- *Variable Name:* `lang=en-AU` 
- *Value/Text:* `<HTM <SPAN LANG="en-AU"> /HTM>`

The point of this is that such language assignments are preserved even after multiple conversions in both directions, so they are always effective for spell checking in the ODT document.

It is recommended not to modify such markups in yWriter to avoid unwanted nesting and broken enclosing. 

## HowTo

## General note

Pleawe make sure that the headings are not hard-formatted in your original document. With LibreOffice, select the headings (you can use the Find dialog with "Format" activated), and reset the formatting with `Ctrl`-`M`.
Then you can remove stray language tags: Select the whole document with `Ctrl`-`A`, then set the language of the selection to your default language.

## How to set up a work in progress for export

A work in progress has no third level heading.

-   *Heading 1* → New chapter title (beginning a new section).
-   *Heading 2* → New chapter title.
-   `* * *` → Scene divider (not needed for the first scenes in a
    chapter).
-   Comments right at the scene beginning are considered scene titles.
-   All other text is considered scene content.

## How to set up an outline for export

An outline has at least one third level heading.

-   *Heading 1* → New chapter title (beginning a new section).
-   *Heading 2* → New chapter title.
-   *Heading 3* → New scene title.
-   All other text is considered to be chapter/scene description.

---

[<< Previous](export_menu) -- [Next >>](descriptions_menu)
