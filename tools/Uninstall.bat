@echo off
REM Removes the yW2OO software package.
REM 
REM See: https://github.com/peter88213/yW2OO
REM License: The MIT License (https://opensource.org/licenses/mit-license.php)
REM Copyright: (c) 2020, Peter Triesberger
REM 
REM Note: This script is to be executed manually.
REM 
REM Preconditions:
REM * yW2OO is installed.
REM * LibreOffice 5.x or 6.x is installed.
RREM
REM Postconditions:
REM * Previously auto-installed items of yW2OO are removed.
REM * "writer.bat" is removed from all yWriter project directories within [userprofile]\Documents.

set _release=2.0.0

pushd setup

set _LibreOffice5_w64=c:\Program Files (x86)\LibreOffice 5
set _LibreOffice5_w32=c:\Program Files\LibreOffice 5
set _LibreOffice6_w64=c:\Program Files (x86)\LibreOffice
set _LibreOffice6_w32=c:\Program Files\LibreOffice

set _LibreOffice_Userprofile=AppData\Roaming\LibreOffice\4\user

echo -----------------------------------------------------------------
echo yW2OO (yWriter to OpenOffice/LibreOffice) v%_release%
echo Installing software package ...
echo -----------------------------------------------------------------

rem Detect Combination of Windows and Office 

f exist "%_LibreOffice5_w64%\program\swriter.exe" goto LibreOffice5-Win64
if exist "%_LibreOffice5_w32%\program\swriter.exe" goto LibreOffice5-Win32
if exist "%_LibreOffice6_w64%\program\swriter.exe" goto LibreOffice6-Win64
if exist "%_LibreOffice6_w32%\program\swriter.exe" goto LibreOffice6-Win32
echo ERROR: No supported version of LibreOffice found!
echo Installation aborted
goto end

:LibreOffice5-Win64
set _writer=%_LibreOffice5_w64%
set _user=%USERPROFILE%\%_LibreOffice_Userprofile%
echo LibreOffice
goto settings_done

:LibreOffice5-Win32
set _writer=%_LibreOffice5_w32%
set _user=%USERPROFILE%\%_LibreOffice_Userprofile%
echo LibreOffice
goto settings_done

:LibreOffice6-Win64
set _writer=%_LibreOffice6_w64%
set _user=%USERPROFILE%\%_LibreOffice_Userprofile%
echo LibreOffice
goto settings_done

:LibreOffice6-Win32
set _writer=%_LibreOffice6_w32%
set _user=%USERPROFILE%\%_LibreOffice_Userprofile%
echo LibreOffice
goto settings_done

:settings_done

echo Deleting program components in %_user%\yW2OO and removing folder ...

rmdir /s /q "%_user%\yW2OO"

echo Deleting writer.bat ...

del writer.bat

echo Removing OpenOffice extension ...

"%_writer%\program\unopkg" remove -f yW2OO-L-%_release%.oxt

call genRemoveWriter.bat
call RemoveWriter.bat

popd

echo -----------------------------------------------------------------
echo #
echo # yW2OO v%_release% is removed from your PC.
echo #
echo -----------------------------------------------------------------
pause



:end
