@echo off

echo -----------------------------------------------------------------
echo Installing yW2OO (yWriter to OpenOffice) software package ...
echo -----------------------------------------------------------------
rem Determine Combination of Windows and Office 
if exist "c:\Program Files (x86)\OpenOffice 4\program\swriter.exe" goto OpenOffice4-Win64
if exist "c:\Program Files\OpenOffice 4\program\swriter.exe" goto OpenOffice4-Win32
if exist "c:\Program Files (x86)\OpenOffice.org 3\program\swriter.exe" goto OpenOffice3-Win64
if exist "c:\Program Files\OpenOffice.org 3\program\swriter.exe" goto OpenOffice3-Win32
echo ERROR: OpenOffice 3.x or 4.x not found
echo Installation aborted
goto end

:OpenOffice4-Win64
set _writer=c:\Program Files (x86)\OpenOffice 4
set _user=%USERPROFILE%\AppData\Roaming\OpenOffice\4\user
echo OpenOffice 4.x on Windows (64 bit) detected.
goto go-install

:OpenOffice4-Win32
set _writer=c:\Program Files\OpenOffice 4
set _user=%USERPROFILE%\AppData\Roaming\OpenOffice\4\user
echo OpenOffice 4.x on Windows (32 bit) detected.
goto go-install

:OpenOffice3-Win64
set _writer=c:\Program Files (x86)\OpenOffice.org 3
set _user=%USERPROFILE%\AppData\Roaming\OpenOffice.org\3\user
echo OpenOffice 3.x on Windows (64 bit) detected.
goto go-install

:OpenOffice3-Win32
set _writer=c:\Program Files\OpenOffice.org 3
set _user=%USERPROFILE%\AppData\Roaming\OpenOffice.org\3\user
echo OpenOffice 3.x on Windows (32 bit) detected.
goto go-install

:go-install

echo Copying tools and templates to %_user% ...

mkdir "%_user%\yW2OO"
copy yW2OO.py "%_user%\yW2OO"
copy manuscript.ott "%_user%\template"

rem Create language-dependent "writer.bat"
echo @echo off > writer.bat
echo if not exist "Exported Project.html" goto error >> writer.bat
echo copy "Exported Project.html" "Exported Project.html.bak" ^> NUL >> writer.bat
echo "%_writer%\program\python.exe" "%_user%\yW2OO\yW2OO.py" >> writer.bat
echo echo Starting Office ... >> writer.bat

rem Trying to determine Office's language
if exist "%_writer%\readmes\readme_de.txt" goto german
goto english


:german:
echo Use german localization -- style names in german language
echo "%_writer%\program\swriter.exe" "macro:///yW2OO.Convert.yHTML_de" "Exported Project.html"  >> writer.bat
goto international

:english:
echo Use english localization -- style names in english language
echo "%_writer%\program\swriter.exe" "macro:///yW2OO.Convert.yHTML_en" "Exported Project.html"  >> writer.bat
goto international

:international
echo goto end >> writer.bat
echo :error >> writer.bat
echo echo ERROR: "Exported Project.html" does not exist! >> writer.bat
echo pause >> writer.bat
echo :end >> writer.bat
echo exit >> writer.bat


echo -----------------------------------------------------------------
echo Office's Extension Manager will be started automatically.
echo Please confirm installation of extension "yW2OO2",
echo then close Office!
echo -----------------------------------------------------------------
pause

"%_writer%\program\swriter.exe" -nodefault yW2OO.oxt

echo Installation of yW2OO software package finished.

echo -----------------------------------------------------------------
echo Please copy "writer.bat" to your yWriter Project "Export" folder!
echo Export your yWriter project as HTML, then run "writer.bat"
echo -----------------------------------------------------------------

:end
pause