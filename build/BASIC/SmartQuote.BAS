sub Smart_Quotes
rem ----------------------------------------------------------------------
rem define variables
dim document   as object
dim dispatcher as object
rem ----------------------------------------------------------------------
rem get access to the document
document   = ThisComponent.CurrentController.Frame
dispatcher = createUnoService("com.sun.star.frame.DispatchHelper")

rem ----------------------------------------------------------------------
dim args1(18) as new com.sun.star.beans.PropertyValue
args1(0).Name = "SearchItem.StyleFamily"
args1(0).Value = 2
args1(1).Name = "SearchItem.CellType"
args1(1).Value = 0
args1(2).Name = "SearchItem.RowDirection"
args1(2).Value = true
args1(3).Name = "SearchItem.AllTables"
args1(3).Value = false
args1(4).Name = "SearchItem.Backward"
args1(4).Value = false
args1(5).Name = "SearchItem.Pattern"
args1(5).Value = false
args1(6).Name = "SearchItem.Content"
args1(6).Value = false
args1(7).Name = "SearchItem.AsianOptions"
args1(7).Value = false
args1(8).Name = "SearchItem.AlgorithmType"
args1(8).Value = 1
args1(9).Name = "SearchItem.SearchFlags"
args1(9).Value = 65536
args1(10).Name = "SearchItem.SearchString"
args1(10).Value = "(\"+CHR$(34)+"\<)([^\"+CHR$(34)+"]*[\.\?!,]?)(\"+CHR$(34)+")"
args1(11).Name = "SearchItem.ReplaceString"
args1(11).Value = "»$2«"
args1(12).Name = "SearchItem.Locale"
args1(12).Value = 255
args1(13).Name = "SearchItem.ChangedChars"
args1(13).Value = 2
args1(14).Name = "SearchItem.DeletedChars"
args1(14).Value = 2
args1(15).Name = "SearchItem.InsertedChars"
args1(15).Value = 2
args1(16).Name = "SearchItem.TransliterateFlags"
args1(16).Value = 1280
args1(17).Name = "SearchItem.Command"
args1(17).Value = 3
args1(18).Name = "Quiet"
args1(18).Value = true

dispatcher.executeDispatch(document, ".uno:ExecuteSearch", "", 0, args1())

rem ----------------------------------------------------------------------
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
args2(5).Value = false
args2(6).Name = "SearchItem.Content"
args2(6).Value = false
args2(7).Name = "SearchItem.AsianOptions"
args2(7).Value = false
args2(8).Name = "SearchItem.AlgorithmType"
args2(8).Value = 1
args2(9).Name = "SearchItem.SearchFlags"
args2(9).Value = 65536
args2(10).Name = "SearchItem.SearchString"
args2(10).Value = "(\'\<)([^\']*[\.\?!,]?)(\')"
args2(11).Name = "SearchItem.ReplaceString"
args2(11).Value = "›$2‹"
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


end sub