@echo off
REM
REM summary: Installation file for the yW2OO software package.
REM 
REM author: Peter Triesberger
REM see: https://github.com/peter88213/yW2OO
REM license: The MIT License (https://opensource.org/licenses/mit-license.php)
REM copyright: (c) 2018, Peter Triesberger
REM version: v1.1.0
REM 
REM note: This script is to be run manually after un-packing the setup file.
REM 
REM precondition: All installation files must exist in the working directory.
REM precondition: OpenOffice.org 3.x or Apache OpenOffice 4.x must be installed in english or german localization.
REM postcondition: The yW2OO Python preprocessor is installed in the OpenOffice user profile.
REM postcondition: Optional templates are installed in the OpenOffice user profile.
REM postcondition: The yW2OO Office Extension is installed.
REM postcondition: The program starter "writer.bat" is generated in the working directory.
REM 
REM since: 2018-10-01
REM change: 2018-10-03 v1.0.0: Added comments, version number and release info. Update "writer.bat" generator.
REM change: 2018-10-03 v1.1.0: Update release info. Update "writer.bat" generator.

set _release=v1.1.0 

echo -----------------------------------------------------------------
echo yW2OO (yWriter to OpenOffice) %_release%
echo Installing software package ...
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
copy /y yW2OO.py "%_user%\yW2OO"
copy /y manuscript.ott "%_user%\template"

rem Create language-dependent "writer.bat"
echo @echo off > writer.bat
 
echo echo yW2OO %_release% >> writer.bat
echo echo Starting yWriter to OpenOffice conversion ... >> writer.bat
echo if not exist "Exported Project.html" goto error >> writer.bat
echo copy "Exported Project.html" "Exported Project.html.bak" ^> NUL >> writer.bat
echo "%_writer%\program\python.exe" "%_user%\yW2OO\yW2OO.py" >> writer.bat
echo if errorlevel 1 goto end >> writer.bat
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

rem "%_writer%\program\swriter.exe" -nodefault yW2OO.oxt
yW2OO.oxt


echo -----------------------------------------------------------------
echo #
echo # Installation of yW2OO software package %_release% finished.
echo #
echo # Please copy "writer.bat" to your yWriter Project "Export" folder!
echo # Export your yWriter project as HTML, then run "writer.bat"
echo #
echo -----------------------------------------------------------------

:end
pause