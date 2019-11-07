@echo off
REM Installation script for the yW2OO software package.
REM 
REM See: https://github.com/peter88213/yW2OO
REM License: The MIT License (https://opensource.org/licenses/mit-license.php)
REM Copyright: (c) 2019, Peter Triesberger
REM 
REM Note: This script is to be executed manually after un-packing the setup file.
REM 
REM Preconditions:
REM * Setup folder structure must exist in the working directory.
REM * OpenOffice.org 3.x or Apache OpenOffice 4.x or LibreOffice 6.x is installed.
REM
REM Postconditions: 
REM * The yW2OO Python scripts are installed in the Open/LibreOffice user profile.
REM * The yW2OO Office Extension is installed.
REM * The program starter "writer.bat" is generated in the setup directory.
REM * "writer.bat" is copied to all yWriter "Export" directories within [userprofile]\Documents.

set _release=1.15.1

pushd setup

set _OpenOffice4_w64=c:\Program Files (x86)\OpenOffice 4
set _OpenOffice4_w32=c:\Program Files\OpenOffice 4
set _OpenOffice3_w64=c:\Program Files (x86)\OpenOffice.org 3
set _OpenOffice3_w32=c:\Program Files\OpenOffice.org 3
set _LibreOffice5_w64=c:\Program Files (x86)\LibreOffice 5
set _LibreOffice5_w32=c:\Program Files\LibreOffice 5
set _LibreOffice6_w64=c:\Program Files (x86)\LibreOffice
set _LibreOffice6_w32=c:\Program Files\LibreOffice

set _OpenOffice4_Userprofile=AppData\Roaming\OpenOffice\4\user
set _OpenOffice3_Userprofile=AppData\Roaming\OpenOffice.org\3\user
set _LibreOffice_Userprofile=AppData\Roaming\LibreOffice\4\user

echo -----------------------------------------------------------------
echo yW2OO (yWriter to OpenOffice/LibreOffice) v%_release%
echo Installing software package ...
echo -----------------------------------------------------------------

rem Detect Combination of Windows and Office 

if exist "%_OpenOffice4_w64%\program\swriter.exe" goto OpenOffice4-Win64
if exist "%_OpenOffice4_w32%\program\swriter.exe" goto OpenOffice4-Win32
if exist "%_OpenOffice3_w64%\program\swriter.exe" goto OpenOffice3-Win64
if exist "%_OpenOffice3_w32%\program\swriter.exe" goto OpenOffice3-Win32
if exist "%_LibreOffice5_w64%\program\swriter.exe" goto LibreOffice5-Win64
if exist "%_LibreOffice5_w32%\program\swriter.exe" goto LibreOffice5-Win32
if exist "%_LibreOffice6_w64%\program\swriter.exe" goto LibreOffice6-Win64
if exist "%_LibreOffice6_w32%\program\swriter.exe" goto LibreOffice6-Win32
echo ERROR: No supported version of OpenOffice/LibreOffice found!
echo Installation aborted
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

echo Installing new OpenOffice extension ...

"%_writer%\program\unopkg" add -f program\yW2OO-%_release%.oxt

echo Copying program components to %_user% ...

if not exist "%_user%\yW2OO" mkdir "%_user%\yW2OO"
copy /y program\*.py "%_user%\yW2OO"

echo Creating "writer.bat" ...

echo @echo off > writer.bat
echo if exist "%_user%\yW2OO\yw2oo.py" goto inst_ok >> writer.bat
echo echo ERROR: yW2OO Software is not installed! >> writer.bat
echo pause >> writer.bat
echo goto end >> writer.bat
echo :inst_ok >> writer.bat
echo echo yW2OO v%_release% >> writer.bat
echo echo Starting yWriter to OpenOffice conversion ... >> writer.bat
echo if not exist "Exported Project.html" goto error >> writer.bat
echo copy "Exported Project.html" "Exported Project.html.bak" ^> NUL >> writer.bat
echo "%_writer%\program\python.exe" "%_user%\yW2OO\yw2oo.py" >> writer.bat
echo if errorlevel 1 goto end >> writer.bat
echo if exist ..\Auto_Descriptions.txt move /Y ..\Auto_Descriptions.txt .\ >> writer.bat
echo "%_writer%\program\python.exe" "%_user%\yW2OO\sceti.py" >> writer.bat
echo echo Running Office Writer ... >> writer.bat
echo "%_writer%\program\swriter.exe" "macro:///yW2OO.Convert.main" "Exported Project.html"  >> writer.bat
echo goto end >> writer.bat
echo :error >> writer.bat
echo echo ERROR: "Exported Project.html" does not exist! >> writer.bat
echo pause >> writer.bat
echo :end >> writer.bat
echo exit >> writer.bat

call genCopyWriter.bat
call CopyWriter.bat

popd

echo Creating template install scripts
echo copy /-y StandardPages.ott "%_user%\template\" > template\StandardPages_A4\Install.bat
echo copy /-y StandardPages.ott "%_user%\template\" > template\StandardPages_Letter\Install.bat

echo -----------------------------------------------------------------
echo #
echo # Installation of yW2OO software package v%_release% finished.
echo #
echo # Now look for "standard pages" template in  "template" folder
echo #
echo # Operation: 
echo # Export your yWriter project as HTML,
echo # Go into your yWriter Project "Export" folder,
echo # then run "writer.bat"
echo #
echo -----------------------------------------------------------------

:end
pause