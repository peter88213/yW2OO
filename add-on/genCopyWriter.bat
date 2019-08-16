@echo off
rem Generate a batchfile to spread "writer.bat" over all yWriter projects.
rem If necessary, modify parameter "_docroot".

set _docroot="%userprofile%\Documents"

set _genfile=copyWriter.bat
pushd %_docroot%
echo rem Copy "writer.bat" to all yWriter project "Export" folders > %_genfile%
echo rem "writer.bat" must exist in this directory >> %_genfile%
echo rem >> %_genfile%
for /F "tokens=*" %%l in ('dir /s /b Export') do echo copy /y writer.bat "%%l" >> %_genfile%
popd
move /Y  %_docroot%\%_genfile% ..\