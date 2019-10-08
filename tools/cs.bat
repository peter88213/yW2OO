rem @echo off
REM cs.bat
REM summary: Collects everything for a yW2OO release
REM          and puts it into localized setup directories to be zipped.
REM author: Peter Triesberger
REM see: https://github.com/peter88213/yW2OO
REM license: The MIT License (https://opensource.org/licenses/mit-license.php)
REM copyright: (c) 2019, Peter Triesberger

set _release=1.12.0

set _project=yW2OO

set _root=..\

rem ********************************************************
rem English/international release
rem ********************************************************

rem --------------------------------------------------------
rem Set up directory structure
rem --------------------------------------------------------

set _source_en=%_root%ott\en-US
set _target_en=%_root%build\yW2OO_en_v%_release%

mkdir %_target_en%
del /s /q %_target_en%

mkdir %_target_en%\program
del /s /q %_target_en%\program

mkdir %_target_en%\add-on
del /s /q %_target_en%\add-on
xcopy /s %_root%\add-on\*.* %_target_en%\add-on\

rem --------------------------------------------------------
rem Generate english README file with release info
rem --------------------------------------------------------

echo # yW2OO (yWriter to OpenOffice/LibreOffice converter) v%_release%>%_target_en%\README.txt
echo Convert yWriter's HTML export file into a neat OpenOffice Writer document, ready to apply templates and styles.>>%_target_en%\README.txt
echo For further information see https://github.com/peter88213/yW2OO/wiki/>>%_target_en%\README.txt

rem --------------------------------------------------------
rem Copy language dependent release items 
rem --------------------------------------------------------

set _file=%_source_en%\StandardPages.ott
set _dest=%_target_en%\program\
call :copyFile

rem --------------------------------------------------------
rem Copy language independent release items 
rem --------------------------------------------------------

set _target=%_target_en%
call :cpInternational

rem --------------------------------------------------------
rem Copy templates for customization
rem --------------------------------------------------------

mkdir %_target_en%\add-on\template-A4
del /s /q %_target_de%\add-on\template-A4

set _file=%_root%ott\de-DE\StandardPages.ott
set _dest=%_target_en%\add-on\template-A4\
call :copyFile

set _file=%_root%ott\de-DE\README.md
set _dest=%_target_en%\add-on\template-A4\
call :copyFile

mkdir %_target_en%\add-on\template-Letter
del /s /q %_target_de%\add-on\template-Letter

set _file=%_root%ott\en-US\StandardPages.ott
set _dest=%_target_en%\add-on\template-Letter\
call :copyFile

set _file=%_root%ott\en-US\README.md
set _dest=%_target_en%\add-on\template-Letter\
call :copyFile



rem --------------------------------------------------------
rem End (english/international release) 
rem --------------------------------------------------------

rem ********************************************************
rem German release
rem ********************************************************

rem --------------------------------------------------------
rem Set up directory structure
rem --------------------------------------------------------

set _source_de=%_root%ott\de-DE
set _target_de=%_root%build\yW2OO_de_v%_release%

mkdir %_target_de%
del /s /q %_target_de%

mkdir %_target_de%\program
del /s /q %_target_de%\program

mkdir %_target_de%\add-on
del /s /q %_target_de%\add-on
xcopy /s %_root%\add-on\*.* %_target_de%\add-on\

rem --------------------------------------------------------
rem Copy english README file
rem --------------------------------------------------------

copy %_target_en%\README.txt %_target_de%\

rem --------------------------------------------------------
rem Copy language dependent release items 
rem --------------------------------------------------------

set _file=%_source_de%\StandardPages.ott
set _dest=%_target_de%\program\
call :copyFile

rem --------------------------------------------------------
rem Copy language independent release items 
rem --------------------------------------------------------

set _target=%_target_de%
call :cpInternational

rem --------------------------------------------------------
rem End (german release) 
rem --------------------------------------------------------

goto end


:cpInternational

rem --------------------------------------------------------
rem Copy language independent release items
rem --------------------------------------------------------
@echo

set _file=%_root%src\yW2OO.py
set _dest=%_target%\program\
call :copyFile

set _file=%_root%src\SceTi.py
set _dest=%_target%\program\
call :copyFile

set _file=%_root%tools\Install.bat
set _dest=%_target%\
call :copyFile

set _file=%_root%tools\Uninstall.bat
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

rmdir /s /q %_target_de%
rmdir /s /q %_target_en%
echo ERROR: %_file% does not exist!
pause
exit

:end