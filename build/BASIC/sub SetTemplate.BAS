Sub SetTemplate
		path=createunoservice("com.sun.star.util.PathSettings")
		match = InStr(path.UserConfig,"config")
		TemplatePath = Left(path.UserConfig,match-1)+"template/Manuscript_de-DE.ott"
		rem Msgbox TemplatePath
        dim args(0) as new com.sun.star.beans.PropertyValue
        sTemplateName = "Manuscript_de-DE.ott"
        sURL = TemplatePath
        args(0).Name = "OverwriteStyles"
        args(0).Value = True
        ThisComponent.stylefamilies.loadStylesFromURL( sURL, args() )
        ThisComponent.DocumentInfo.Template = sTemplateName
        ThisComponent.DocumentInfo.TemplateFileName = sURL
End Sub
