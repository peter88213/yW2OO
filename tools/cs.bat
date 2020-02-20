REM cs.bat
REM Collects everything for a yW2OO release
REM and puts it the "dist" setup directory to be zipped.
REM 
REM See: https://github.com/peter88213/yW2OO
REM License: The MIT License (https://opensource.org/licenses/mit-license.php)
REM Copyright: (c) 2020, Peter Triesberger

set _release=2.2.0

set _project=yW2OO

set _root=..\

rem --------------------------------------------------------
rem Set up directory structure
rem --------------------------------------------------------

set _target=%_root%dist\yW2OO_v%_release%

if exist %_target% rd /s /q %_target%

mkdir %_target%
mkdir %_target%\setup
mkdir %_target%\setup\program
mkdir %_target%\fonts

rem --------------------------------------------------------
rem Generate release info
rem --------------------------------------------------------

rem echo v%_release%>%_target%\VERSION

rem --------------------------------------------------------
rem Copy release items 
rem --------------------------------------------------------

set _file=%_root%README.md
set _dest=%_target%\
call :copyFile

set _file=%_root%LIESMICH.md
set _dest=%_target%\
call :copyFile

set _file=%_root%src\yw2oo.py
set _dest=%_target%\setup\program\
call :copyFile

set _file=%_root%src\findyw7.py
set _dest=%_target%\setup\
call :copyFile

set _file=%_root%odt\template.zip
set _dest=%_target%\setup\program\
call :copyFile

set _file=%_root%LICENSE
set _dest=%_target%\
call :copyFile

set _file=%_root%tools\Install.bat
set _dest=%_target%\
call :copyFile

set _file=%_root%tools\Uninstall.bat
set _dest=%_target%\
call :copyFile

set _file=%_root%fonts\CourierPrime.zip
set _dest=%_target%\fonts\
call :copyFile

exit /b


:copyFile

rem --------------------------------------------------------
rem Copy a file
rem --------------------------------------------------------

if not exist %_file% goto error
copy /y  %_file% %_dest%
exit /b


:error

rmdir /s /q %_target%
echo ERROR: %_file% does not exist!
pause
exit 1

:end