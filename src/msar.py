""" Multiple search and replace text in a file (command line).

@summary: Replaces all occurrences of "old Text[0..n]" in a text file 
by "new Text[0..n]". Old Text and new Text are input from replacements list.

    Structure of replacements list: 
    
    old Text[0]|new Text[0]|
    old Text[1]|new Text[1]|
    ...
    old Text[n]|new Text[n]|

    Syntax: msar.py <text file to modify><replacements list>

@author: Peter Triesberger
@see: https://github.com/peter88213/yW2OO
@version: v1.2.1
@license: The MIT License (https://opensource.org/licenses/mit-license.php)
@copyright: (c) 2018, Peter Triesberger
@since: 2018-05-11
@change: 2019-10-23 v1.2.2 Refactoring according to PEP 8 style guide
    (see https://www.python.org/dev/peps/pep-0008/)
"""
import sys


def search_and_replace(processData, replaceList):
    """ Multiple search and replace text in a string

    @summary: Modifying a string by looping through a list of search/replacement items.
    @param: processData: string to be modified.
    @param: replaceList: list of strings containing search/replacement items. 
        Structure of each list element: "<search item>|<replacement item>|" 
        The replacement item can be empty.  
    @return: Modified string
    """
    for line in replaceList:
        replaceItem = line.split('|')
        processData = processData.replace(replaceItem[0], replaceItem[1])
    return(processData)


def main():
    try:
        myReplaceList = open(sys.argv[2], 'r')
        myTextFile = open(sys.argv[1], 'r')
        myProcessData = myTextFile.read()
        myTextFile.close()
        myTextFile = open(sys.argv[1], 'w')
        myTextFile.write(search_and_replace(myProcessData, myReplaceList))
        myTextFile.close()
        myReplaceList.close()
    except:
        print 'Syntax: sar.py <text file to modify><replacements list>'


if __name__ == '__main__':
    main()
