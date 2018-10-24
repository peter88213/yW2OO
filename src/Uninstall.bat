@echo off
REM
REM summary: Removes the yW2OO software package.
REM 
REM author: Peter Triesberger
REM see: https://github.com/peter88213/yW2OO
REM license: The MIT License (https://opensource.org/licenses/mit-license.php)
REM copyright: (c) 2018, Peter Triesberger
REM 
REM note: This script is to be executed manually.
REM 
REM precondition: yW2OO is installed.
REM precondition: OpenOffice.org 3.x or Apache OpenOffice 4.x is installed.
REM postcondition: Previously auto-installed items of yW2OO are removed.
REM postcondition: The template remains, if user wants it.
REM 
REM since: 2018-10-04
REM change: 2018-10-09 v1.3.0: Created german localized copy of v1.2.0 "Uninstall.bat".
REM change: 2018-10-10 v1.4.0: Update release info.
REM change: 2018-10-13 v1.4.1: Update release info. 
REM change: 2018-10-16 v1.4.1: Add LibreOffice 5 suppport.
REM change: 2018-10-17 v1.5.0: Update release info. 
REM change: 2018-10-23 v1.6.0: Update release info. 
REM change: 2018-10-24 v1.7.0: Added new document template. 
REM change: 2018-10-24 v1.7.0: Simplify texts for locale-independent use.

set _release=1.7.0

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
echo yW2OO (yWriter to OpenOffice) v%_release%
echo Removing software package ...
echo -----------------------------------------------------------------
rem Detect Combination of Windows and Office 
if exist "%_OpenOffice4_w64%\program\swriter.exe" goto OpenOffice4-Win64
if exist "%_OpenOffice4_w32%\program\swriter.exe" goto OpenOffice4-Win32
if exist "%_OpenOffice3_w64%\program\swriter.exe" goto OpenOffice3-Win64
if exist "%_OpenOffice3_w32%\program\swriter.exe" goto OpenOffice3-Win32
if exist "%_LibreOffice5_w64%\program\swriter.exe" goto LibreOffice5-Win64
if exist "%_LibreOffice5_w32%\program\swriter.exe" goto LibreOffice5-Win32
echo ERROR: No supported version of OpenOffice/LibreOffice found!
echo De-Installation aborted.
goto end

:OpenOffice4-Win64
set _writer=%_OpenOffice4_w64%
set _user=%USERPROFILE%\%_OpenOffice4_Userprofile%
echo OpenOffice 4.x - Windows (64 bit)
goto settings_done

:OpenOffice4-Win32
set _writer=%_OpenOffice4_w32%
set _user=%USERPROFILE%\%_OpenOffice4_Userprofile%
echo OpenOffice 4.x - Windows (32 bit)
goto settings_done

:OpenOffice3-Win64
set _writer=%_OpenOffice3_w64%
set _user=%USERPROFILE%\%_OpenOffice3_Userprofile%
echo OpenOffice 3.x - Windows (64 bit)
goto settings_done

:OpenOffice3-Win32
set _writer=%_OpenOffice3_w32%
set _user=%USERPROFILE%\%_OpenOffice3_Userprofile%
echo OpenOffice 3.x - Windows (32 bit)
goto settings_done

:LibreOffice5-Win64
set _writer=%_LibreOffice5_w64%
set _user=%USERPROFILE%\%_LibreOffice5_Userprofile%
echo LibreOffice 5.x on Windows (64 bit) detected.
goto settings_done

:LibreOffice5-Win32
set _writer=%_LibreOffice5_w32%
set _user=%USERPROFILE%\%_LibreOffice5_Userprofile%
echo LibreOffice 5.x on Windows (32 bit) detected.
goto settings_done

:settings_done

echo Deleting templates in %_user%\template (on confirmation only) ...

set _file="%_user%\template\Manuscript_en-US.ott"
if exist %_file% del /p %_file%

set _file="%_user%\template\Manuscript_de-DE.ott"
if exist %_file% del /p %_file%

set _file="%_user%\template\StandardPages.ott"
if exist %_file% del /p %_file%

echo Deleting program components in %_user%\yW2OO and removing folder ...

rmdir /s /q "%_user%\yW2OO"

echo Deleting writer.bat ...

del writer.bat

echo Removing OpenOffice extension ...

"%_writer%\program\unopkg" remove -f yW2OO-%_release%.oxt

echo -----------------------------------------------------------------
echo #
echo # yW2OO v%_release% is removed from your PC.
echo #
echo # You may delete copies of copy "writer.bat" 
echo # in your yWriter Project "Export" folder manually
echo #
echo -----------------------------------------------------------------
pause



:end
