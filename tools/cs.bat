REM cs.bat
REM summary: Collects everything for a yW2OO release
REM          and puts it the "build" setup directory to be zipped.
REM author: Peter Triesberger
REM see: https://github.com/peter88213/yW2OO
REM license: The MIT License (https://opensource.org/licenses/mit-license.php)
REM copyright: (c) 2019, Peter Triesberger

set _release=1.14.0

set _project=yW2OO

set _root=..\

rem --------------------------------------------------------
rem Set up directory structure
rem --------------------------------------------------------

set _target=%_root%build\yW2OO_v%_release%

if exist %_target% rd /s /q %_target%

mkdir %_target%
mkdir %_target%\program
mkdir %_target%\add-on

xcopy /s %_root%\add-on\*.* %_target%\add-on\

rem --------------------------------------------------------
rem Generate english README file with release info
rem --------------------------------------------------------

echo # yW2OO (yWriter to OpenOffice/LibreOffice converter) v%_release%>%_target%\README.txt
echo Convert yWriter's HTML export file into a neat OpenOffice Writer document, ready to apply templates and styles.>>%_target%\README.txt
echo For further information see https://github.com/peter88213/yW2OO/wiki/>>%_target%\README.txt

rem --------------------------------------------------------
rem Copy release items 
rem --------------------------------------------------------

set _file=%_root%src\yw2oo.py
set _dest=%_target%\program\
call :copyFile

set _file=%_root%src\sceti.py
set _dest=%_target%\program\
call :copyFile

set _file=%_root%tools\Install.bat
set _dest=%_target%\
call :copyFile

set _file=%_root%tools\Uninstall.bat
set _dest=%_target%\
call :copyFile

set _file=%_root%tools\genCopyWriter.bat
set _dest=%_target%\
call :copyFile

set _file=%_root%tools\genRemoveWriter.bat
set _dest=%_target%\
call :copyFile

set _file=%_root%oxt\yW2OO-%_release%.oxt
set _dest=%_target%\program\
call :copyFile

set _file=%_root%LICENSE
set _dest=%_target%\
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
exit

:end