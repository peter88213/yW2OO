@echo off
REM cs.bat
REM summary: Collects everything for a yW2OO release
REM          and puts it into a setup directory to be zipped
REM 
REM author: Peter Triesberger
REM see: https://github.com/peter88213/yW2OO
REM license: The MIT License (https://opensource.org/licenses/mit-license.php)
REM copyright: (c) 2018, Peter Triesberger
REM version: v1.1.0

set _release=v1.1.0

set _project=yW2OO

set _source_path=..\src\
set _macro_path=OXT\
set _root=..\
set _target_path=yW2OO_Installation_files


rem--------------------------------------------------------
rem Create empty folder
rem--------------------------------------------------------


mkdir %_target_path%
del /s /q %_target_path%

rem--------------------------------------------------------
rem Generate README files
rem--------------------------------------------------------

echo # yW2OO (yWriter to OpenOffice converter) %_release%>%_target_path%\README.txt
echo Convert yWriter's HTML export file into a neat OpenOffice Writer document, ready to apply templates and styles.>>%_target_path%\README.txt
echo For further information see https://github.com/peter88213/yW2OO/wiki/>>%_target_path%\README.txt


echo # yW2OO (yWriter to OpenOffice converter) %_release%>%_target_path%\LIESMICH.txt
echo HTML-Exportdatei von yWriter in ein sauberes OpenOffice Writer-Dokument umwandeln, um Dokument- und Formatvorlagen anwenden zu können.>>%_target_path%\LIESMICH.txt
echo Weitere Informationen s. https://github.com/peter88213/yW2OO/wiki/Deutsch>>%_target_path%\LIESMICH.txt


rem--------------------------------------------------------
rem Copy release items
rem--------------------------------------------------------

set _file=%_source_path%Manuscript.ott
call :copyFile
set _file=%_source_path%yW2OO.py
call :copyFile
set _file=%_source_path%Install.bat
call :copyFile
set _file=%_source_path%Uninstall.bat
call :copyFile
set _file=%_macro_path%yW2OO.oxt
call :copyFile
set _file=%_root%LICENSE
call :copyFile

goto end

:copyFile
if not exist %_file% goto error
copy /y  %_file% %_target_path%
exit /b

:error

rmdir /s /q %_target_path%
echo ERROR: %_file% does not exist!
pause
exit

:end