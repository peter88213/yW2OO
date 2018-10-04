'''
Created on 27.07.2016

SAR -- Search and Replace Text 
Replaces all occurrences of "old Text[0..n]" in "fileToSearch" by "new Text[0..n]".
Old Text and new Text are input from searchList.

Structure of searchList: 

old Text[0]|new Text[0]|
old Text[1]|new Text[1]|
...
old Text[n]|new Text[n]|

Syntax: sar.py <fileToSearch><searchList>

@author: Peter Triesberger
'''
#!/usr/bin/env python3
import sys

try:
    searchList = open(sys.argv[2],'r')
    fileToSearch = open(sys.argv[1],'r')
    dataToSearch = fileToSearch.read()
    fileToSearch.close()
    for line in searchList:
        splitLine = line.split("|") 
        # splitLine[0] = old Text 
        # splitLine[1] = new Text
        dataToSearch = dataToSearch.replace(splitLine[0],splitLine[1])
    fileToSearch = open(sys.argv[1],'w')
    fileToSearch.write(dataToSearch)
    fileToSearch.close()
    searchList.close()
except:
    print("Syntax: sar.py <fileToSearch><searchList>")
