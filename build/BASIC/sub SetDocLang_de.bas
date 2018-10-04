sub SetDocLang_de
'' ----------------------------------------------------------------------
'' define variables
dim document   as object
dim dispatcher as object
'' ----------------------------------------------------------------------
'' get access to the document
document   = ThisComponent.CurrentController.Frame
dispatcher = createUnoService("com.sun.star.frame.DispatchHelper")

'' ----------------------------------------------------------------------
dim args1(0) as new com.sun.star.beans.PropertyValue
args1(0).Name = "Language"
args1(0).Value = "Default_Deutsch (Deutschland)"

dispatcher.executeDispatch(document, ".uno:LanguageStatus", "", 0, args1())


end sub