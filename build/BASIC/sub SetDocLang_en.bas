sub SetDocLang_en
rem ----------------------------------------------------------------------
rem define variables
dim document   as object
dim dispatcher as object
rem ----------------------------------------------------------------------
rem get access to the document
document   = ThisComponent.CurrentController.Frame
dispatcher = createUnoService("com.sun.star.frame.DispatchHelper")

rem ----------------------------------------------------------------------
dim args1(0) as new com.sun.star.beans.PropertyValue
args1(0).Name = "Language"
args1(0).Value = "Default_English (USA)"

dispatcher.executeDispatch(document, ".uno:LanguageStatus", "", 0, args1())


end sub