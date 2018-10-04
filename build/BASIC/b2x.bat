@echo off
REM b2x.bat
REM summary: Pack a StarBASIC source file into a StarBASIC XML Library file
REM 
REM author: Peter Triesberger
REM see: https://github.com/peter88213/yW2OO
REM license: The MIT License (https://opensource.org/licenses/mit-license.php)
REM copyright: (c) 2018, Peter Triesberger
REM version: v1.0.0

set _src_path=..\..\src\
set _macro_path=..\OXT\
set _header=header.txt
set _footer=footer.txt
set _source=%_src_path%Convert.BAS
set _xml=%_macro_path%Convert.xba

@echo on

copy /y %_source% temp.txt
sar.py temp.txt b2x.txt
type %_header%  > %_xml%
type temp.txt >> %_xml%
type %_footer% >> %_xml%
del temp.txt