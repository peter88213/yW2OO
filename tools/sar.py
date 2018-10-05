'''

sar.py 

@summary: Search and Replace Text (command line)
Replaces all occurrences of "old Text[0..n]" in a text file by "new Text[0..n]".
Old Text and new Text are input from replacements list.

Structure of replacements list: 

old Text[0]|new Text[0]|
old Text[1]|new Text[1]|
...
old Text[n]|new Text[n]|

Syntax: sar.py <text file to modify><replacements list>

@author: Peter Triesberger
@see: https://github.com/peter88213/yW2OO
@version: v1.2.1
@license: The MIT License (https://opensource.org/licenses/mit-license.php)
@copyright: (c) 2018, Peter Triesberger
@since: 2018-05-11

'''
import sys

def searchAndReplace(processData, replaceList):
    '''
    @summary: Modifying a string by looping through a list of search/replacement items.
    @param: processData: string to be modified.
    @param: replaceList: list of strings containing search/replacement items. 
        Structure of each list element: "<search item>|<replacement item>|" 
        The replacement item can be empty.  
    @return: Modified string
    '''   
    for line in replaceList:
        replaceItem = line.split("|") 
        processData = processData.replace(replaceItem[0],replaceItem[1])
    return(processData)


    
    
if __name__ == '__main__':
    try:
        myReplaceList = open(sys.argv[2],'r')
        myTextFile = open(sys.argv[1],'r')
        myProcessData = myTextFile.read()
        myTextFile.close()
        myTextFile = open(sys.argv[1],'w')
        myTextFile.write(searchAndReplace(myProcessData, myReplaceList))
        myTextFile.close()
        myReplaceList.close()
    except:
        print("Syntax: sar.py <text file to modify><replacements list>")
