rem @echo off
REM cs.bat
REM summary: Collects everything for a yW2OO release (en and de localisation)
REM          and puts it into a setup directories to be zipped.
REM author: Peter Triesberger
REM see: https://github.com/peter88213/yW2OO
REM license: The MIT License (https://opensource.org/licenses/mit-license.php)
REM copyright: (c) 2018, Peter Triesberger
REM version: v1.4.1

set _release=v1.4.1

set _project=yW2OO

rem Set up directory structure

set _root=..\
set _source_en=en-US
set _source_de=de-DE
set _macro_path=%_root%build\OXT
set _target_en=%_root%build\yW2OO_en_%_release%
set _target_de=%_root%build\yW2OO_de_%_release%


rem --------------------------------------------------------
rem Create empty target folders
rem --------------------------------------------------------

mkdir %_target_en%
del /s /q %_target_en%

mkdir %_target_en%\program
del /s /q %_target_en%\program

mkdir %_target_en%\add-on
del /s /q %_target_en%\add-on

mkdir %_target_de%
del /s /q %_target_de%

mkdir %_target_de%\program
del /s /q %_target_de%\program

mkdir %_target_de%\add-on
del /s /q %_target_de%\add-on

rem --------------------------------------------------------
rem Generate README files
rem --------------------------------------------------------

echo # yW2OO (yWriter to OpenOffice converter) %_release%>%_target_en%\README.txt
echo Convert yWriter's HTML export file into a neat OpenOffice Writer document, ready to apply templates and styles.>>%_target_en%\README.txt
echo For further information see https://github.com/peter88213/yW2OO/wiki/>>%_target_en%\README.txt


echo # yW2OO (yWriter to OpenOffice converter) %_release%>%_target_de%\LIESMICH.txt
echo HTML-Exportdatei von yWriter in ein sauberes OpenOffice Writer-Dokument umwandeln, um Dokument- und Formatvorlagen anwenden zu können.>>%_target_de%\LIESMICH.txt
echo Weitere Informationen s. https://github.com/peter88213/yW2OO/wiki/Deutsch>>%_target_de%\LIESMICH.txt


rem --------------------------------------------------------
rem Copy release items
rem --------------------------------------------------------

set _file=%_source_en%\Manuscript_en-US.ott
set _dest=%_target_en%\program\
call :copyFile

set _file=%_source_de%\Manuscript_de-DE.ott
set _dest=%_target_de%\program\
call :copyFile

set _file=yW2OO.py
set _dest=%_target_en%\program\
call :copyFile
set _dest=%_target_de%\program\
call :copyFile

set _file=%_source_en%\Install.bat
set _dest=%_target_en%\
call :copyFile

set _file=%_source_de%\Install.bat
set _dest=%_target_de%\
call :copyFile

set _file=%_source_en%\Uninstall.bat
set _dest=%_target_en%\
call :copyFile

set _file=%_source_de%\Uninstall.bat
set _dest=%_target_de%\
call :copyFile

set _file=%_macro_path%\yW2OO.oxt
set _dest=%_target_en%\program\
call :copyFile
set _dest=%_target_de%\program\
call :copyFile

set _file=%_root%LICENSE
set _dest=%_target_en%\
call :copyFile
set _dest=%_target_de%\
call :copyFile

set _file=genCopyWriter.bat
set _dest=%_target_en%\add-on\
call :copyFile
set _dest=%_target_de%\add-on\
call :copyFile

set _file=genRemoveWriter.bat
set _dest=%_target_en%\add-on\
call :copyFile
set _dest=%_target_de%\add-on\
call :copyFile

goto end

:copyFile
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