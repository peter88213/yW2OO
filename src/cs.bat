rem @echo off
REM cs.bat
REM summary: Collects everything for a yW2OO release en-US and de-DE
REM          and puts it into a setup directories to be zipped.
REM author: Peter Triesberger
REM see: https://github.com/peter88213/yW2OO
REM license: The MIT License (https://opensource.org/licenses/mit-license.php)
REM copyright: (c) 2018, Peter Triesberger
REM version: v1.3.0

set _release=v1.3.0

set _project=yW2OO

rem Set up directory structure

set _root=..\
set _source_en=en-US
set _source_de=de-DE
set _macro_path=%_root%build\OXT
set _target_en=%_root%build\yW2OO_en-US%_release%
set _target_de=%_root%build\yW2OO_de-DE%_release%


rem --------------------------------------------------------
rem clear destination folders
rem --------------------------------------------------------

mkdir %_target_en%
del /s /q %_target_en%
mkdir %_target_de%
del /s /q %_target_de%

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
call :copyFile_en
set _file=%_source_de%\Manuscript_de-DE.ott
call :copyFile_de
set _file=yW2OO.py
call :copyFile_en
call :copyFile_de
set _file=%_source_en%\Install.bat
call :copyFile_en
set _file=%_source_de%\Install.bat
call :copyFile_de
set _file=%_source_en%\Uninstall.bat
call :copyFile_en
set _file=%_source_de%\Uninstall.bat
call :copyFile_de
set _file=%_macro_path%\yW2OO.oxt
call :copyFile_en
call :copyFile_de
set _file=%_root%LICENSE
call :copyFile_en
call :copyFile_de

goto end

:copyFile_en
if not exist %_file% goto error
copy /y  %_file% %_target_en%\
exit /b

:copyFile_de
if not exist %_file% goto error
copy /y  %_file% %_target_de%\
exit /b

:error

rmdir /s /q %_target_de%
rmdir /s /q %_target_en%
echo ERROR: %_file% does not exist!
pause
exit

:end