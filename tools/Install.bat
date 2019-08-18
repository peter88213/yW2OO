@echo off
REM
REM summary: Installation script for the yW2OO software package.
REM 
REM author: Peter Triesberger
REM see: https://github.com/peter88213/yW2OO
REM license: The MIT License (https://opensource.org/licenses/mit-license.php)
REM copyright: (c) 2018, Peter Triesberger
REM 
REM note: This script is to be executed manually after un-packing the setup file.
REM 
REM precondition: All installation files must exist in the working directory.
REM precondition: OpenOffice.org 3.x or Apache OpenOffice 4.x is installed.
REM postcondition: The yW2OO Python preprocessor is installed in the OpenOffice user profile.
REM postcondition: A standard manuscript page templates is installed in the OpenOffice user profile.
REM postcondition: The yW2OO Office Extension is installed.
REM postcondition: The program starter "writer.bat" is generated in the working directory.
REM 
REM since: 2018-10-01
REM change: 2018-10-03 v1.0.0: Added comments, version number and release info. Update "writer.bat" generator.
REM change: 2018-10-03 v1.1.0: Update release info. Update "writer.bat" generator.
REM change: 2018-10-05 v1.2.0: Update release info. Update "writer.bat" generator.
REM change: 2018-10-09 v1.3.0: Created english localized copy of v1.2.0 "install.bat".
REM change: 2018-10-10 v1.4.0: Update release info.
REM change: 2018-10-13 v1.4.1: Update release info. Apply new directory structure.
REM change: 2018-10-15 v1.4.1: Create target directories if necessary.
REM change: 2018-10-16 v1.4.1: Add LibreOffice 5 suppport.
REM change: 2018-10-17 v1.5.0: Update release info. 
REM change: 2018-10-23 v1.6.0: Update release info. 
REM change: 2018-10-24 v1.7.0: Macro call is language independent; renamed document template.
REM change: 2018-10-24 v1.7.0: Simplify texts for locale-independent use.
REM change: 2018-10-27 v1.7.0: Suppress puzzling installation message and confirm template overwrite.
REM change: 2019-06-22 v1.8.0: StandardPages template is no longer being associated with the converted document.
REM change: 2019-08-15 v1.8.1: Added LibreOffice 6.x support.
REM change: 2019-08-18 v1.9.0: Changed processing of dashes and ellipses (just revert yWriter's mdash conversion). Replace double spaces by single spaces.

set _release=1.9.0

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

echo Copying program components and templates to %_user% ...

if not exist "%_user%\yW2OO" mkdir "%_user%\yW2OO"
copy /y program\yW2OO.py "%_user%\yW2OO"

if not exist "%_user%\template" mkdir "%_user%\template"
copy /-y program\StandardPages.ott "%_user%\template"

echo Creating "writer.bat" ...

echo @echo off > writer.bat
echo if exist "%_user%\yW2OO\yW2OO.py" goto inst_ok >> writer.bat
echo echo ERROR: yW2OO Software is not installed! >> writer.bat
echo pause >> writer.bat
echo goto end >> writer.bat
echo :inst_ok >> writer.bat
echo echo yW2OO v%_release% >> writer.bat
echo echo Starting yWriter to OpenOffice conversion ... >> writer.bat
echo if not exist "Exported Project.html" goto error >> writer.bat
echo copy "Exported Project.html" "Exported Project.html.bak" ^> NUL >> writer.bat
echo "%_writer%\program\python.exe" "%_user%\yW2OO\yW2OO.py" >> writer.bat
echo if errorlevel 1 goto end >> writer.bat
echo echo Running Office Writer ... >> writer.bat
echo "%_writer%\program\swriter.exe" "macro:///yW2OO.Convert.main" "Exported Project.html"  >> writer.bat
echo goto end >> writer.bat
echo :error >> writer.bat
echo echo ERROR: "Exported Project.html" does not exist! >> writer.bat
echo pause >> writer.bat
echo :end >> writer.bat
echo exit >> writer.bat

echo -----------------------------------------------------------------
echo #
echo # Installation of yW2OO software package v%_release% finished.
echo #
echo # Please copy "writer.bat" 
echo # to your yWriter Project "Export" folder!
echo # Export your yWriter project as HTML,
echo # then run "writer.bat"
echo #
echo -----------------------------------------------------------------

:end
pause