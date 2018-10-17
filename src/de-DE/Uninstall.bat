@echo off
REM
REM summary: Entfernt das yW2OO Softwarepaket.
REM 
REM author: Peter Triesberger
REM see: https://github.com/peter88213/yW2OO
REM license: The MIT License (https://opensource.org/licenses/mit-license.php)
REM copyright: (c) 2018, Peter Triesberger
REM version: v1.5.0
REM 
REM note: This script is to be executed manually.
REM 
REM precondition: yW2OO is installed.
REM precondition: OpenOffice.org 3.x or Apache OpenOffice 4.x must be installed in english or german localization.
REM postcondition: Previously auto-installed items of yW2OO are removed.
REM postcondition: The template remains, if user wants it.
REM postcondition: The yW2OO Office Extension must be removed via Extension Manager.
REM 
REM since: 2018-10-04
REM change: 2018-10-09 v1.3.0: Created german localized copy of v1.2.0 "Uninstall.bat".
REM change: 2018-10-10 v1.4.0: Update release info.
REM change: 2018-10-13 v1.4.1: Update release info. 
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
echo Entferne Softwarepaket ...
echo -----------------------------------------------------------------
rem Detet Combination of Windows and Office 
if exist "%_OpenOffice4_w64%\program\swriter.exe" goto OpenOffice4-Win64
if exist "%_OpenOffice4_w32%\program\swriter.exe" goto OpenOffice4-Win32
if exist "%_OpenOffice3_w64%\program\swriter.exe" goto OpenOffice3-Win64
if exist "%_OpenOffice3_w32%\program\swriter.exe" goto OpenOffice3-Win32
if exist "%_LibreOffice5_w64%\program\swriter.exe" goto LibreOffice5-Win64
if exist "%_LibreOffice5_w32%\program\swriter.exe" goto LibreOffice5-Win32
echo FEHLER: Keine passende OpenOffice/LibreOffice-Version gefunden!
echo Deinstallation wird abgebrochen.
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

echo Dokumentvorlage in %_user%\template entfernen (nur auf Wunsch) ...

set _file="%_user%\template\Manuscript_de-DE.ott"
if exist %_file% del /p %_file%

set _file="%_user%\template\Manuscript_en-US.ott"
if exist %_file% del /p %_file%

echo Programmkomponenten in %_user%\yW2OO werden mitsamt dem Ordner entfernt ...

rmdir /s /q "%_user%\yW2OO"

echo writer.bat wird entfernt (Die Kopien in  ^<Ihr yWriter Projektordner^>\Export bitte von Hand entfernen) ...

del writer.bat

echo OpenOffice Erweiterung wird deinstalliert ...

"%_writer%\program\unopkg" remove -f yW2OO.OXT

echo Fertig.
pause



:end
