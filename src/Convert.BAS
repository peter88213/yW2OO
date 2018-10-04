''  *****  BASIC  *****
''
'' summary: Post-Processing an imported HTML file in order to be saved as ODT
'' 
'' author: Peter Triesberger
'' see: https://github.com/peter88213/yW2OO
'' license: The MIT License (https://opensource.org/licenses/mit-license.php)
'' copyright: (c) 2018, Peter Triesberger
'' version: v1.0.1
'' 
'' note: This script is to be called automatically by batch file per command line parameter.
'' 
'' precondition: English or german Office installation.
'' precondition: The input file "Exported Project.html" must be open and pre-processed by "yW2OO.py".
'' postcondition: The output file "Exported Project.odt" is generated and saved in the same directory where the input file is ( details see below).
'' 
'' since: 2018-10-01
'' change: 2018-10-03 v1.0.0: Added comments and version number.
'' change: 2018-10-03 v1.0.1: rename: "First-line indent" --> "First line indent".



sub yHTML_en

'' ----------------------------------------------------------------------
'' Use English style names for (en-US) OpenOffice installation
'' ----------------------------------------------------------------------

SetParagraphStyles_en
SetPagestyle_en
SaveAsODT

End Sub



sub yHTML_de

'' ----------------------------------------------------------------------
'' Use German style names for (de) OpenOffice installation
'' ----------------------------------------------------------------------

SetParagraphStyles_de
SetPagestyle_de
SaveAsODT

End Sub



Sub SetParagraphStyles_de

'' ----------------------------------------------------------------------
'' Eine importierte HTML-Datei für die Umwandlung in ODT nachbearbeiten
'' 
'' Eingabe: yWriter HTML Export-Datei
'' folgendermaßen vorverarbeitet:
'' Kapitelüberschrift ist "Überschrift 2"
'' Szenenüberschrift ist "Überschrift 4"
'' Jeder erste Absatz in Kapitel oder Szene ist "Überschrift 6"
'' Jeder andere Absatz ist "Textkörper"
'' 
'' Dieses BASIC Script formatiert alle Absätze um:
'' "Textkörper" --> "Textkörper Einzug"
'' "Überschrift 6" --> "Textkörper"
'' "Überschrift 2" --> "Überschrift 2" (harte Formatierungen entfernen)
'' "Überschrift 4" --> "Überschrift 4" (harte Formatierungen entfernen)
'' 
'' ----------------------------------------------------------------------

document   = ThisComponent.CurrentController.Frame
dispatcher = createUnoService("com.sun.star.frame.DispatchHelper")

dim args1(1) as new com.sun.star.beans.PropertyValue
args1(0).Name = "Template"
args1(0).Value = "Standard"
args1(1).Name = "Family"
args1(1).Value = 8

dispatcher.executeDispatch(document, ".uno:StyleApply", "", 0, args1())

'' ----------------------------------------------------------------------
'' Textkörper --> Textkörper Einzug
'' ----------------------------------------------------------------------

dim args2(18) as new com.sun.star.beans.PropertyValue
args2(0).Name = "SearchItem.StyleFamily"
args2(0).Value = 2
args2(1).Name = "SearchItem.CellType"
args2(1).Value = 0
args2(2).Name = "SearchItem.RowDirection"
args2(2).Value = true
args2(3).Name = "SearchItem.AllTables"
args2(3).Value = false
args2(4).Name = "SearchItem.Backward"
args2(4).Value = false
args2(5).Name = "SearchItem.Pattern"
args2(5).Value = true
args2(6).Name = "SearchItem.Content"
args2(6).Value = false
args2(7).Name = "SearchItem.AsianOptions"
args2(7).Value = false
args2(8).Name = "SearchItem.AlgorithmType"
args2(8).Value = 0
args2(9).Name = "SearchItem.SearchFlags"
args2(9).Value = 65536
args2(10).Name = "SearchItem.SearchString"
args2(10).Value = "Textkörper"
args2(11).Name = "SearchItem.ReplaceString"
args2(11).Value = "Textkörper Einzug"
args2(12).Name = "SearchItem.Locale"
args2(12).Value = 255
args2(13).Name = "SearchItem.ChangedChars"
args2(13).Value = 2
args2(14).Name = "SearchItem.DeletedChars"
args2(14).Value = 2
args2(15).Name = "SearchItem.InsertedChars"
args2(15).Value = 2
args2(16).Name = "SearchItem.TransliterateFlags"
args2(16).Value = 1280
args2(17).Name = "SearchItem.Command"
args2(17).Value = 3
args2(18).Name = "Quiet"
args2(18).Value = true

dispatcher.executeDispatch(document, ".uno:ExecuteSearch", "", 0, args2())

'' ----------------------------------------------------------------------
'' Überschrift 6 --> Textkörper
'' ----------------------------------------------------------------------

dim args3(18) as new com.sun.star.beans.PropertyValue
args3(0).Name = "SearchItem.StyleFamily"
args3(0).Value = 2
args3(1).Name = "SearchItem.CellType"
args3(1).Value = 0
args3(2).Name = "SearchItem.RowDirection"
args3(2).Value = true
args3(3).Name = "SearchItem.AllTables"
args3(3).Value = false
args3(4).Name = "SearchItem.Backward"
args3(4).Value = false
args3(5).Name = "SearchItem.Pattern"
args3(5).Value = true
args3(6).Name = "SearchItem.Content"
args3(6).Value = false
args3(7).Name = "SearchItem.AsianOptions"
args3(7).Value = false
args3(8).Name = "SearchItem.AlgorithmType"
args3(8).Value = 0
args3(9).Name = "SearchItem.SearchFlags"
args3(9).Value = 65536
args3(10).Name = "SearchItem.SearchString"
args3(10).Value = "Überschrift 6"
args3(11).Name = "SearchItem.ReplaceString"
args3(11).Value = "Textkörper"
args3(12).Name = "SearchItem.Locale"
args3(12).Value = 255
args3(13).Name = "SearchItem.ChangedChars"
args3(13).Value = 2
args3(14).Name = "SearchItem.DeletedChars"
args3(14).Value = 2
args3(15).Name = "SearchItem.InsertedChars"
args3(15).Value = 2
args3(16).Name = "SearchItem.TransliterateFlags"
args3(16).Value = 1280
args3(17).Name = "SearchItem.Command"
args3(17).Value = 3
args3(18).Name = "Quiet"
args3(18).Value = true

dispatcher.executeDispatch(document, ".uno:ExecuteSearch", "", 0, args3())

'' ----------------------------------------------------------------------
'' Überschrift 2 --> Überschrift 2
'' ----------------------------------------------------------------------

dim args4(18) as new com.sun.star.beans.PropertyValue
args4(0).Name = "SearchItem.StyleFamily"
args4(0).Value = 2
args4(1).Name = "SearchItem.CellType"
args4(1).Value = 0
args4(2).Name = "SearchItem.RowDirection"
args4(2).Value = true
args4(3).Name = "SearchItem.AllTables"
args4(3).Value = false
args4(4).Name = "SearchItem.Backward"
args4(4).Value = false
args4(5).Name = "SearchItem.Pattern"
args4(5).Value = true
args4(6).Name = "SearchItem.Content"
args4(6).Value = false
args4(7).Name = "SearchItem.AsianOptions"
args4(7).Value = false
args4(8).Name = "SearchItem.AlgorithmType"
args4(8).Value = 0
args4(9).Name = "SearchItem.SearchFlags"
args4(9).Value = 65536
args4(10).Name = "SearchItem.SearchString"
args4(10).Value = "Überschrift 2"
args4(11).Name = "SearchItem.ReplaceString"
args4(11).Value = "Überschrift 2"
args4(12).Name = "SearchItem.Locale"
args4(12).Value = 255
args4(13).Name = "SearchItem.ChangedChars"
args4(13).Value = 2
args4(14).Name = "SearchItem.DeletedChars"
args4(14).Value = 2
args4(15).Name = "SearchItem.InsertedChars"
args4(15).Value = 2
args4(16).Name = "SearchItem.TransliterateFlags"
args4(16).Value = 1280
args4(17).Name = "SearchItem.Command"
args4(17).Value = 3
args4(18).Name = "Quiet"
args4(18).Value = true

dispatcher.executeDispatch(document, ".uno:ExecuteSearch", "", 0, args4())

'' ----------------------------------------------------------------------
'' Überschrift 4 --> Überschrift 4
'' ----------------------------------------------------------------------

dim args5(18) as new com.sun.star.beans.PropertyValue
args5(0).Name = "SearchItem.StyleFamily"
args5(0).Value = 2
args5(1).Name = "SearchItem.CellType"
args5(1).Value = 0
args5(2).Name = "SearchItem.RowDirection"
args5(2).Value = true
args5(3).Name = "SearchItem.AllTables"
args5(3).Value = false
args5(4).Name = "SearchItem.Backward"
args5(4).Value = false
args5(5).Name = "SearchItem.Pattern"
args5(5).Value = true
args5(6).Name = "SearchItem.Content"
args5(6).Value = false
args5(7).Name = "SearchItem.AsianOptions"
args5(7).Value = false
args5(8).Name = "SearchItem.AlgorithmType"
args5(8).Value = 0
args5(9).Name = "SearchItem.SearchFlags"
args5(9).Value = 65536
args5(10).Name = "SearchItem.SearchString"
args5(10).Value = "Überschrift 4"
args5(11).Name = "SearchItem.ReplaceString"
args5(11).Value = "Überschrift 4"
args5(12).Name = "SearchItem.Locale"
args5(12).Value = 255
args5(13).Name = "SearchItem.ChangedChars"
args5(13).Value = 2
args5(14).Name = "SearchItem.DeletedChars"
args5(14).Value = 2
args5(15).Name = "SearchItem.InsertedChars"
args5(15).Value = 2
args5(16).Name = "SearchItem.TransliterateFlags"
args5(16).Value = 1280
args5(17).Name = "SearchItem.Command"
args5(17).Value = 3
args5(18).Name = "Quiet"
args5(18).Value = true

dispatcher.executeDispatch(document, ".uno:ExecuteSearch", "", 0, args5())

end Sub



sub SetParagraphStyles_en

'' ----------------------------------------------------------------------
'' Post-Processing an imported HTML file in order to be saved as ODT
'' 
'' Input: yWriter HTML export file 
'' pre-processed as follows:
'' Chapter heading is "Heading 2"
'' Scene heading is "Heading 4" 
'' First paragraph of each chapter and scene is "Heading 6"
'' Any other paragraph is "Text body"
'' 
'' This BASIC Script re-formats all paragraphs:
'' "Text body" --> "First line indent"
'' "Heading 6" --> "Text body"
'' "Heading 2" --> "Heading 2" (cleaning up hard formatting of Heading 2)
'' "Heading 4" --> "Heading 4" (cleaning up hard formatting of Heading 4)
'' 
'' ----------------------------------------------------------------------

document   = ThisComponent.CurrentController.Frame
dispatcher = createUnoService("com.sun.star.frame.DispatchHelper")

dim args1(1) as new com.sun.star.beans.PropertyValue
args1(0).Name = "Template"
args1(0).Value = "Standard"
args1(1).Name = "Family"
args1(1).Value = 8

dispatcher.executeDispatch(document, ".uno:StyleApply", "", 0, args1())

'' ----------------------------------------------------------------------
'' Text body --> First line indent
'' ----------------------------------------------------------------------

dim args2(18) as new com.sun.star.beans.PropertyValue
args2(0).Name = "SearchItem.StyleFamily"
args2(0).Value = 2
args2(1).Name = "SearchItem.CellType"
args2(1).Value = 0
args2(2).Name = "SearchItem.RowDirection"
args2(2).Value = true
args2(3).Name = "SearchItem.AllTables"
args2(3).Value = false
args2(4).Name = "SearchItem.Backward"
args2(4).Value = false
args2(5).Name = "SearchItem.Pattern"
args2(5).Value = true
args2(6).Name = "SearchItem.Content"
args2(6).Value = false
args2(7).Name = "SearchItem.AsianOptions"
args2(7).Value = false
args2(8).Name = "SearchItem.AlgorithmType"
args2(8).Value = 0
args2(9).Name = "SearchItem.SearchFlags"
args2(9).Value = 65536
args2(10).Name = "SearchItem.SearchString"
args2(10).Value = "Text body"
args2(11).Name = "SearchItem.ReplaceString"
args2(11).Value = "First line indent"
args2(12).Name = "SearchItem.Locale"
args2(12).Value = 255
args2(13).Name = "SearchItem.ChangedChars"
args2(13).Value = 2
args2(14).Name = "SearchItem.DeletedChars"
args2(14).Value = 2
args2(15).Name = "SearchItem.InsertedChars"
args2(15).Value = 2
args2(16).Name = "SearchItem.TransliterateFlags"
args2(16).Value = 1280
args2(17).Name = "SearchItem.Command"
args2(17).Value = 3
args2(18).Name = "Quiet"
args2(18).Value = true

dispatcher.executeDispatch(document, ".uno:ExecuteSearch", "", 0, args2())

'' ----------------------------------------------------------------------
'' "Heading 6" --> "Text body"
'' ----------------------------------------------------------------------

dim args3(18) as new com.sun.star.beans.PropertyValue
args3(0).Name = "SearchItem.StyleFamily"
args3(0).Value = 2
args3(1).Name = "SearchItem.CellType"
args3(1).Value = 0
args3(2).Name = "SearchItem.RowDirection"
args3(2).Value = true
args3(3).Name = "SearchItem.AllTables"
args3(3).Value = false
args3(4).Name = "SearchItem.Backward"
args3(4).Value = false
args3(5).Name = "SearchItem.Pattern"
args3(5).Value = true
args3(6).Name = "SearchItem.Content"
args3(6).Value = false
args3(7).Name = "SearchItem.AsianOptions"
args3(7).Value = false
args3(8).Name = "SearchItem.AlgorithmType"
args3(8).Value = 0
args3(9).Name = "SearchItem.SearchFlags"
args3(9).Value = 65536
args3(10).Name = "SearchItem.SearchString"
args3(10).Value = "Heading 6"
args3(11).Name = "SearchItem.ReplaceString"
args3(11).Value = "Text body"
args3(12).Name = "SearchItem.Locale"
args3(12).Value = 255
args3(13).Name = "SearchItem.ChangedChars"
args3(13).Value = 2
args3(14).Name = "SearchItem.DeletedChars"
args3(14).Value = 2
args3(15).Name = "SearchItem.InsertedChars"
args3(15).Value = 2
args3(16).Name = "SearchItem.TransliterateFlags"
args3(16).Value = 1280
args3(17).Name = "SearchItem.Command"
args3(17).Value = 3
args3(18).Name = "Quiet"
args3(18).Value = true

dispatcher.executeDispatch(document, ".uno:ExecuteSearch", "", 0, args3())

'' ----------------------------------------------------------------------
'' Heading 2" --> "Heading 2" (cleaning up hard formatting of Heading 2)
'' ----------------------------------------------------------------------

dim args4(18) as new com.sun.star.beans.PropertyValue
args4(0).Name = "SearchItem.StyleFamily"
args4(0).Value = 2
args4(1).Name = "SearchItem.CellType"
args4(1).Value = 0
args4(2).Name = "SearchItem.RowDirection"
args4(2).Value = true
args4(3).Name = "SearchItem.AllTables"
args4(3).Value = false
args4(4).Name = "SearchItem.Backward"
args4(4).Value = false
args4(5).Name = "SearchItem.Pattern"
args4(5).Value = true
args4(6).Name = "SearchItem.Content"
args4(6).Value = false
args4(7).Name = "SearchItem.AsianOptions"
args4(7).Value = false
args4(8).Name = "SearchItem.AlgorithmType"
args4(8).Value = 0
args4(9).Name = "SearchItem.SearchFlags"
args4(9).Value = 65536
args4(10).Name = "SearchItem.SearchString"
args4(10).Value = "Heading 2"
args4(11).Name = "SearchItem.ReplaceString"
args4(11).Value = "Heading 2"
args4(12).Name = "SearchItem.Locale"
args4(12).Value = 255
args4(13).Name = "SearchItem.ChangedChars"
args4(13).Value = 2
args4(14).Name = "SearchItem.DeletedChars"
args4(14).Value = 2
args4(15).Name = "SearchItem.InsertedChars"
args4(15).Value = 2
args4(16).Name = "SearchItem.TransliterateFlags"
args4(16).Value = 1280
args4(17).Name = "SearchItem.Command"
args4(17).Value = 3
args4(18).Name = "Quiet"
args4(18).Value = true

dispatcher.executeDispatch(document, ".uno:ExecuteSearch", "", 0, args4())

'' ----------------------------------------------------------------------
'' Heading 4" --> "Heading 4" (cleaning up hard formatting of Heading 4)
'' ----------------------------------------------------------------------

dim args5(18) as new com.sun.star.beans.PropertyValue
args5(0).Name = "SearchItem.StyleFamily"
args5(0).Value = 2
args5(1).Name = "SearchItem.CellType"
args5(1).Value = 0
args5(2).Name = "SearchItem.RowDirection"
args5(2).Value = true
args5(3).Name = "SearchItem.AllTables"
args5(3).Value = false
args5(4).Name = "SearchItem.Backward"
args5(4).Value = false
args5(5).Name = "SearchItem.Pattern"
args5(5).Value = true
args5(6).Name = "SearchItem.Content"
args5(6).Value = false
args5(7).Name = "SearchItem.AsianOptions"
args5(7).Value = false
args5(8).Name = "SearchItem.AlgorithmType"
args5(8).Value = 0
args5(9).Name = "SearchItem.SearchFlags"
args5(9).Value = 65536
args5(10).Name = "SearchItem.SearchString"
args5(10).Value = "Heading 4"
args5(11).Name = "SearchItem.ReplaceString"
args5(11).Value = "Heading 4"
args5(12).Name = "SearchItem.Locale"
args5(12).Value = 255
args5(13).Name = "SearchItem.ChangedChars"
args5(13).Value = 2
args5(14).Name = "SearchItem.DeletedChars"
args5(14).Value = 2
args5(15).Name = "SearchItem.InsertedChars"
args5(15).Value = 2
args5(16).Name = "SearchItem.TransliterateFlags"
args5(16).Value = 1280
args5(17).Name = "SearchItem.Command"
args5(17).Value = 3
args5(18).Name = "Quiet"
args5(18).Value = true

dispatcher.executeDispatch(document, ".uno:ExecuteSearch", "", 0, args5())

end Sub



sub SetPagestyle_de

'' ----------------------------------------------------------------------
'' Seitenformat  "Standard " laden und zum Anfang springen.
'' ----------------------------------------------------------------------

dim document   as object
dim dispatcher as object
document   = ThisComponent.CurrentController.Frame
dispatcher = createUnoService("com.sun.star.frame.DispatchHelper")

dim args1(1) as new com.sun.star.beans.PropertyValue
args1(0).Name = "Template"
args1(0).Value = "Standard"
args1(1).Name = "Family"
args1(1).Value = 8

dispatcher.executeDispatch(document, ".uno:StyleApply", "", 0, args1())
dispatcher.executeDispatch(document, ".uno:GoToStartOfDoc", "", 0, Array())

end Sub



sub SetPagestyle_en

'' ----------------------------------------------------------------------
'' Load pagestyle  "Default " and go to top.
'' ----------------------------------------------------------------------

dim document   as object
dim dispatcher as object
'' get access to the document
document   = ThisComponent.CurrentController.Frame
dispatcher = createUnoService("com.sun.star.frame.DispatchHelper")

dim args1(1) as new com.sun.star.beans.PropertyValue
args1(0).Name = "Template"
args1(0).Value = "Default"
args1(1).Name = "Family"
args1(1).Value = 8

dispatcher.executeDispatch(document, ".uno:StyleApply", "", 0, args1())
dispatcher.executeDispatch(document, ".uno:GoToStartOfDoc", "", 0, Array())

end Sub



sub SaveAsODT

'' ----------------------------------------------------------------------
'' Save document in OpenDocument format
'' ----------------------------------------------------------------------

dim document   as object
dim dispatcher as object
dim DocPath as string

document   = ThisComponent.CurrentController.Frame
dispatcher = createUnoService("com.sun.star.frame.DispatchHelper")
DocPath = ThisComponent.getURL()
DocPath = Left(DocPath,len(DocPath)-4)+"odt"


'' ----------------------------------------------------------------------
'' Use path and name of input file -- just change file extension
'' ----------------------------------------------------------------------

dim args1(1) as new com.sun.star.beans.PropertyValue
args1(0).Name = "URL"
args1(0).Value = DocPath
args1(1).Name = "FilterName"
args1(1).Value = "writer8"

dispatcher.executeDispatch(document, ".uno:SaveAs", "", 0, args1())

end Sub



sub SetDocLang_de

'' ----------------------------------------------------------------------
'' Set document language "de"
'' ----------------------------------------------------------------------

dim document   as object
dim dispatcher as object
document   = ThisComponent.CurrentController.Frame
dispatcher = createUnoService("com.sun.star.frame.DispatchHelper")

dim args1(0) as new com.sun.star.beans.PropertyValue
args1(0).Name = "Language"
args1(0).Value = "Default_Deutsch (Deutschland)"

dispatcher.executeDispatch(document, ".uno:LanguageStatus", "", 0, args1())
