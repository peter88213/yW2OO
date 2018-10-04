@echo off
REM b2x.bat
REM summary: Pack a StarBASIC source file into a StarBASIC XML Library file
REM 
REM author: Peter Triesberger
REM see: https://github.com/peter88213/yW2OO
REM license: The MIT License (https://opensource.org/licenses/mit-license.php)
REM copyright: (c) 2018, Peter Triesberger
REM version: v1.0.0
@echo on
set _header=header.txt
set _footer=footer.txt
set _source=Convert.BAS
set _xml=Convert.xba
copy /y %_source% temp.txt
sar.py temp.txt b2x.txt
type %_header%  > %_xml%
type temp.txt >> %_xml%
type %_footer% >> %_xml%
del temp.txt