@echo off
REM
REM summary: Deutsches Installationsprogramm für das yW2OO-Paket.
REM 
REM author: Peter Triesberger
REM see: https://github.com/peter88213/yW2OO
REM license: The MIT License (https://opensource.org/licenses/mit-license.php)
REM copyright: (c) 2018, Peter Triesberger
REM version: v1.5.0
REM 
REM note: This script is to be executed manually after un-packing the setup file.
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
REM change: 2018-10-10 v1.4.0: Update release info.
REM change: 2018-10-13 v1.4.1: Update release info. Apply new directory structure.
REM change: 2018-10-15 v1.4.1: Create target directories if necessary.
REM change: 2018-10-16 v1.4.1: Add LibreOffice 5 suppport.
REM change: 2018-10-17 v1.5.0: Update release info. 

set _release=v1.5.0 

set _OpenOffice4_w64=c:\Program Files (x86)\OpenOffice 4
set _OpenOffice4_w32=c:\Program Files\OpenOffice 4
set _OpenOffice3_w64=c:\Program Files (x86)\OpenOffice.org 3
set _OpenOffice3_w32=c:\Program Files\OpenOffice.org 3
set _LibreOffice5_w64=c:\Program Files (x86)\LibreOffice 5
set _LibreOffice5_w32=c:\Program Files\LibreOffice 5

set _OpenOffice4_Userprofile=AppData\Roaming\OpenOffice\4\user
set _OpenOffice3_Userprofile=AppData\Roaming\OpenOffice.org\3\user
set _LibreOffice5_Userprofile=AppData\Roaming\LibreOffice\4\user

echo -----------------------------------------------------------------
echo yW2OO (yWriter to OpenOffice/LibreOffice) %_release%
echo Installing software package ...
echo -----------------------------------------------------------------
rem Detect Combination of Windows and Office 
if exist "%_OpenOffice4_w64%\program\swriter.exe" goto OpenOffice4-Win64
if exist "%_OpenOffice4_w32%\program\swriter.exe" goto OpenOffice4-Win32
if exist "%_OpenOffice3_w64%\program\swriter.exe" goto OpenOffice3-Win64
if exist "%_OpenOffice3_w32%\program\swriter.exe" goto OpenOffice3-Win32
if exist "%_LibreOffice5_w64%\program\swriter.exe" goto LibreOffice5-Win64
if exist "%_LibreOffice5_w32%\program\swriter.exe" goto LibreOffice5-Win32
echo FEHLER: Keine passende OpenOffice/LibreOffice-Version gefunden!
echo Installation wird abgebrochen.
goto end

:OpenOffice4-Win64
set _writer=%_OpenOffice4_w64%
set _user=%USERPROFILE%\%_OpenOffice4_Userprofile%
echo OpenOffice 4.x unter Windows (64-Bit) gefunden.
goto settings_done

:OpenOffice4-Win32
set _writer=%_OpenOffice4_w32%
set _user=%USERPROFILE%\%_OpenOffice4_Userprofile%
echo OpenOffice 4.x unter Windows (32-Bit) gefunden.
goto settings_done

:OpenOffice3-Win64
set _writer=%_OpenOffice3_w64%
set _user=%USERPROFILE%\%_OpenOffice3_Userprofile%
echo OpenOffice 3.x unter Windows (64-Bit) gefunden.
goto settings_done

:OpenOffice3-Win32
set _writer=%_OpenOffice3_w32%
set _user=%USERPROFILE%\%_OpenOffice3_Userprofile%
echo OpenOffice 3.x unter Windows (32-Bit) gefunden.
goto settings_done

:LibreOffice5-Win64
set _writer=%_LibreOffice5_w64%
set _user=%USERPROFILE%\%_LibreOffice5_Userprofile%
echo LibreOffice 5.x unter Windows (64-Bit) gefunden.
goto settings_done

:LibreOffice5-Win32
set _writer=%_LibreOffice5_w32%
set _user=%USERPROFILE%\%_LibreOffice5_Userprofile%
echo LibreOffice 5.x unter Windows (32-Bit) gefunden.
goto settings_done

:settings_done

echo Programmkomponenten und Vorlagen werden nach %_user% kopiert ...

if not exist "%_user%\yW2OO" mkdir "%_user%\yW2OO"
copy /y program\yW2OO.py "%_user%\yW2OO"

if not exist "%_user%\template" mkdir "%_user%\template"
copy program\Manuscript_de-DE.ott "%_user%\template"


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

"%_writer%\program\unopkg" add -f program\yW2OO.OXT

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