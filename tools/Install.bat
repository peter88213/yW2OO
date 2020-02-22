@echo off
REM Installation script for the yW2OO software package.
REM 
REM See: https://github.com/peter88213/yW2OO
REM License: The MIT License (https://opensource.org/licenses/mit-license.php)
REM Copyright: (c) 2020, Peter Triesberger
REM 
REM Note: This script is to be executed manually after un-packing the setup file.
REM 
REM Preconditions:
REM * Setup folder structure must exist in the working directory.
REM * LibreOffice 5.x or 6.x is installed.
REM
REM Postconditions: 
REM * The yW2OO Python scripts are installed in the LibreOffice user profile.
REM * The program starter "export.bat" is generated in the setup directory.
REM * "export.bat" is copied to all yWriter project directories within [userprofile]\Documents.

set _release=2.3.1

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

rem Detect Combination of Windows and Office 

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

echo Removing old OpenOffice extension ...

"%_writer%\program\unopkg" remove -f yW2OO.OXT >nul


echo Copying program components to %_user%\Scripts\python ...

if not exist "%_user%\Scripts" mkdir "%_user%\Scripts"
if not exist "%_user%\Scripts\python" mkdir "%_user%\Scripts\python"
copy /y program\*.py "%_user%\Scripts\python"

echo Creating "export.bat" ...

echo @echo off > export.bat
echo if exist "%_user%\Scripts\python\yw2oo.py" goto inst_ok >> export.bat
echo echo ERROR: yW2OO Software is not installed! >> export.bat
echo goto end >> export.bat
echo :inst_ok >> export.bat
echo echo yW2OO v%_release% >> export.bat

echo echo Starting yWriter to LibreOffice conversion ... >> export.bat
echo "%_writer%\program\python.exe" "%_user%\Scripts\python\yw2oo.py" >> export.bat
echo if errorlevel 1 goto end >> export.bat

echo exit >> export.bat
echo :end >> export.bat
echo pause >> export.bat

echo "%_writer%\program\python.exe" "findyw7.py" >> findyw7.bat
call findyw7.bat
call Copyexport.bat
popd

echo -----------------------------------------------------------------
echo #
echo # Installation of yW2OO software package v%_release% finished.
echo #
echo # Operation: 
echo # Go into your yWriter Project folder and run "export.bat"
echo #
echo -----------------------------------------------------------------

:end
pause