@echo off
REM Installation script for the yW2OO software package.
REM 
REM See: https://github.com/peter88213/yW2OO
REM License: The MIT License (https://opensource.org/licenses/mit-license.php)
REM Copyright: (c) 2020, peter88213
REM 
REM Note: This script is to be executed manually after un-packing the setup file.
REM 
REM Preconditions:
REM * Setup folder structure must exist in the working directory.
REM * LibreOffice 5.x or 6.x is installed.
REM
REM Postconditions: 
REM * The yW2OO Python scripts are installed in the LibreOffice user profile.
REM * For yWriter7 files, there is an Explorer context menu entry "Export to LibreOffice".
REM * There is a batch file in c:\pywriter to invoke the Python interpreter.

set _release=2.8.0

pushd setup

set _LibreOffice5_w64=c:\Program Files (x86)\LibreOffice 5
set _LibreOffice5_w32=c:\Program Files\LibreOffice 5
set _LibreOffice6_w64=c:\Program Files (x86)\LibreOffice
set _LibreOffice6_w32=c:\Program Files\LibreOffice

set _LibreOffice_Userprofile=AppData\Roaming\LibreOffice\4\user

echo -----------------------------------------------------------------
echo yW2OO (yWriter to LibreOffice) v%_release%
echo Installing software package ...
echo -----------------------------------------------------------------

rem Detect combination of Windows and Office 

if exist "%_LibreOffice5_w64%\program\swriter.exe" goto LibreOffice5-Win64
if exist "%_LibreOffice5_w32%\program\swriter.exe" goto LibreOffice5-Win32
if exist "%_LibreOffice6_w64%\program\swriter.exe" goto LibreOffice6-Win64
if exist "%_LibreOffice6_w32%\program\swriter.exe" goto LibreOffice6-Win32
echo ERROR: No supported version of LibreOffice found!
echo Installation aborted
goto end


:LibreOffice5-Win64
set _writer=%_LibreOffice5_w64%
set _user=%USERPROFILE%\%_LibreOffice_Userprofile%
echo LibreOffice 5 found ...
goto settings_done

:LibreOffice5-Win32
set _writer=%_LibreOffice5_w32%
set _user=%USERPROFILE%\%_LibreOffice_Userprofile%
echo LibreOffice 5 found ...
goto settings_done

:LibreOffice6-Win64
set _writer=%_LibreOffice6_w64%
set _user=%USERPROFILE%\%_LibreOffice_Userprofile%
echo LibreOffice found ...
goto settings_done

:LibreOffice6-Win32
set _writer=%_LibreOffice6_w32%
set _user=%USERPROFILE%\%_LibreOffice_Userprofile%
echo LibreOffice found ...
goto settings_done

:settings_done

echo Copying program components to %_user%\Scripts\python ...

if not exist "%_user%\Scripts" mkdir "%_user%\Scripts"
if not exist "%_user%\Scripts\python" mkdir "%_user%\Scripts\python"
copy /y program\*.py "%_user%\Scripts\python"

echo Installing Explorer context menu entry (You may be asked for approval) ...

if not exist c:\pywriter mkdir c:\pywriter 

echo "%_writer%\program\python.exe" "%_user%\Scripts\python\yw2oo.py" > c:\pywriter\yw2oo.bat

add_cm.reg

popd

echo -----------------------------------------------------------------
echo #
echo # Installation of yW2OO software package v%_release% finished.
echo #
echo # Operation: 
echo # Right click your yWriter 6/7 Project file
echo # and select "Export to LibreOffice".
echo #
echo -----------------------------------------------------------------

:end
pause