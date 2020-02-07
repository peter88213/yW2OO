@echo off 
if exist "C:\Users\Peter\AppData\Roaming\LibreOffice\4\user\yW2OO\yw2oo.py" goto inst_ok 
echo ERROR: yW2OO Software is not installed! 
pause 
goto end 
:inst_ok 
echo yW2OO v2.0.0 
echo Starting yWriter to OpenOffice conversion ...

for /F "tokens=*" %%l in ('dir /b *.yw7') do "c:\Program Files\LibreOffice\program\python.exe" "C:\Users\Peter\AppData\Roaming\LibreOffice\4\user\yW2OO\yw2oo.py" "%%l"
if errorlevel 1 goto end 
echo Running Office Writer ... 
for /F "tokens=*" %%l in ('dir /b *_manuscript.html') do "c:\Program Files\LibreOffice\program\swriter.exe" "macro:///yW2OO.Convert.main" "%%l" 
goto end 
:error 
echo ERROR: "Exported Project.html" does not exist! 
pause 
:end 
 
