@echo off
rem Generate a batchfile to remove "writer.bat" on confirmation from all yWriter projects.
rem If necessary, modify parameter "_docroot".

set _docroot="%userprofile%\Documents"

set _rmfile=removeWriter.bat
pushd %_docroot%
echo rem Remove "writer.bat" from all yWriter project "Export" folders > %_rmfile%
echo @echo on >> %_rmfile%
for /F "tokens=*" %%l in ('dir /s /b Export') do echo del /q "%%l\writer.bat"  >> %_rmfile%
echo @echo off >> %_rmfile%
popd
move /Y  %_docroot%\%_rmfile% .\