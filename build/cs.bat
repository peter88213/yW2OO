@echo off
REM cs.bat
REM summary: Collects everything for a yW2OO release
REM          and puts it into a setup directory to be zipped
REM 
REM author: Peter Triesberger
REM see: https://github.com/peter88213/yW2OO
REM license: The MIT License (https://opensource.org/licenses/mit-license.php)
REM copyright: (c) 2018, Peter Triesberger
REM version: v1.0.0

set _release=v1.0.1

set _project=yW2OO

set _source_path=..\src\
set _macro_path=OXT\
set _document_path=..\docs\


mkdir %_project%%_release%
del /s /q %_project%%_release%

set _file=%_source_path%Manuscript.ott
call :copyFile
set _file=%_source_path%yW2OO.py
call :copyFile
set _file=%_source_path%Install.bat
call :copyFile
set _file=%_macro_path%yW2OO.oxt
call :copyFile
set _file=%_document_path%LICENSE.TXT
call :copyFile
set _file=%_document_path%README.TXT
call :copyFile
set _file=%_document_path%LIESMICH.TXT
call :copyFile
goto end

:copyFile
if not exist %_file% goto error
copy /y  %_file% %_project%%_release%
exit /b

:error
del /s /q %_project%%_release%
rmdir %_project%%_release%
echo ERROR: %_file% does not exist!
pause
exit

:end