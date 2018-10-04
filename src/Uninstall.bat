@echo off
REM
REM summary: Removes most parts of the yW2OO software package.
REM 
REM author: Peter Triesberger
REM see: https://github.com/peter88213/yW2OO
REM license: The MIT License (https://opensource.org/licenses/mit-license.php)
REM copyright: (c) 2018, Peter Triesberger
REM version: v1.1.0
REM 
REM note: This script is to be run manually.
REM 
REM precondition: yW2OO is installed.
REM precondition: OpenOffice.org 3.x or Apache OpenOffice 4.x must be installed in english or german localization.
REM postcondition: Previously auto-installed items of yW2OO are removed.
REM postcondition: The template remains, if user wants it.
REM postcondition: The yW2OO Office Extension must be removed via Extension Manager.
REM 
REM since: 2018-10-04

set _release=v1.1.0 

echo -----------------------------------------------------------------
echo yW2OO (yWriter to OpenOffice) %_release%
echo Removing software package ...
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

echo Deleting tools and templates in %_user% ...

del /p "%_user%\template\manuscript.ott"
rem del /s /q yW2OO.py "%_user%\yW2OO\"
rmdir /s /q "%_user%\yW2OO"
del writer.bat
 
echo -----------------------------------------------------------------
echo #
echo # Almost done ...
echo #
echo # Please run Office and call the Extension Manager
echo # Remove the extension "yW2OO"
echo # 
echo -----------------------------------------------------------------
pause



:end
