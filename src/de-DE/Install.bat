@echo off
REM
REM summary: Deutsches Installationsprogramm für das yW2OO-Paket.
REM 
REM author: Peter Triesberger
REM see: https://github.com/peter88213/yW2OO
REM license: The MIT License (https://opensource.org/licenses/mit-license.php)
REM copyright: (c) 2018, Peter Triesberger
REM version: v1.4.0
REM 
REM Diese Datei muss von Hand ausgeführt werden, nachdem das Installationsarchiv entpackt ist.
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
REM change: 2018-10-05 v1.2.0: Update release info. Update "writer.bat" generator.
REM change: 2018-10-09 v1.3.0: Created german localized copy of v1.2.0 "install.bat".
REM change: 2018-10-19 v1.4.0: Update release info.

set _release=v1.4.0

echo -----------------------------------------------------------------
echo yW2OO (yWriter to OpenOffice) %_release%
echo Installing software package ...
echo -----------------------------------------------------------------
rem Determine Combination of Windows and Office 
if exist "c:\Program Files (x86)\OpenOffice 4\program\swriter.exe" goto OpenOffice4-Win64
if exist "c:\Program Files\OpenOffice 4\program\swriter.exe" goto OpenOffice4-Win32
if exist "c:\Program Files (x86)\OpenOffice.org 3\program\swriter.exe" goto OpenOffice3-Win64
if exist "c:\Program Files\OpenOffice.org 3\program\swriter.exe" goto OpenOffice3-Win32
echo FEHLER: OpenOffice 3.x or 4.x nicht gefunden!
echo Installation wird abgebrochen.
goto end

:OpenOffice4-Win64
set _writer=c:\Program Files (x86)\OpenOffice 4
set _user=%USERPROFILE%\AppData\Roaming\OpenOffice\4\user
echo OpenOffice 4.x unter Windows (64-Bit) gefunden.
goto go-install

:OpenOffice4-Win32
set _writer=c:\Program Files\OpenOffice 4
set _user=%USERPROFILE%\AppData\Roaming\OpenOffice\4\user
echo OpenOffice 4.x unter Windows (32-Bit) gefunden.
goto go-install

:OpenOffice3-Win64
set _writer=c:\Program Files (x86)\OpenOffice.org 3
set _user=%USERPROFILE%\AppData\Roaming\OpenOffice.org\3\user
echo OpenOffice 3.x unter Windows (64-Bit) gefunden.
goto go-install

:OpenOffice3-Win32
set _writer=c:\Program Files\OpenOffice.org 3
set _user=%USERPROFILE%\AppData\Roaming\OpenOffice.org\3\user
echo OpenOffice 3.x unter Windows (32-Bit) gefunden.
goto go-install

:go-install

echo Programmkomponenten und Vorlagen werden nach %_user% kopiert ...

mkdir "%_user%\yW2OO"
copy /y yW2OO.py "%_user%\yW2OO"
copy /y Manuscript_de-DE.ott "%_user%\template"

rem Create language-dependent "writer.bat"
echo @echo off > writer.bat
echo if exist "%_user%\yW2OO\yW2OO.py" goto inst_ok >> writer.bat
echo echo FEHLER: yW2OO Software ist nicht installiert! >> writer.bat
echo pause >> writer.bat
echo goto end >> writer.bat
echo :inst_ok >> writer.bat
echo echo yW2OO %_release% >> writer.bat
echo echo yWriter zu OpenOffice-Konvertierung beginnt ... >> writer.bat
echo if not exist "Exported Project.html" goto error >> writer.bat
echo copy "Exported Project.html" "Exported Project.html.bak" ^> NUL >> writer.bat
echo "%_writer%\program\python.exe" "%_user%\yW2OO\yW2OO.py" >> writer.bat
echo if errorlevel 1 goto end >> writer.bat
echo echo Office wird jetzt aufgerufen ... >> writer.bat
echo "%_writer%\program\swriter.exe" "macro:///yW2OO.Convert.yHTML_de" "Exported Project.html"  >> writer.bat
echo goto end >> writer.bat
echo :error >> writer.bat
echo echo FEHLER: "Exported Project.html" existiert nicht! >> writer.bat
echo pause >> writer.bat
echo :end >> writer.bat
echo exit >> writer.bat

"%_writer%\program\unopkg" add -f yW2OO.OXT

echo -----------------------------------------------------------------
echo #
echo # Installation von yW2OO %_release% beendet.
echo #
echo # Bitte die Datei "writer.bat" in den "Export"-Ordner des yWriter-Projekts kopieren!
echo # Exportieren Sie Ihr yWriter-Project als HTML. Starten Sie dann "writer.bat"
echo #
echo -----------------------------------------------------------------

:end
pause