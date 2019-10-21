'''

yW2OOtest.py

@summary: Test suite for yW2OO.py (does conversion) and SceTi.py (does annotation)
@author: Peter Triesberger
@see: https://github.com/peter88213/yW2OO
@license: The MIT License (https://opensource.org/licenses/mit-license.php)
@copyright: (c) 2019, Peter Triesberger
@precondition: This script is to be placed in "<project dir>/test"
@precondition: The subjects to testing must exist in "<project dir>/src"
@precondition: A test environment as specified below must exist.
@precondition: "<project dir>/test/yWriter5 Sample/Auto_Descriptions.txt" must exist.
@since: 2019-10-21
@change: 2019-10-21 v1.0.0 Adapted subjects' function calls.

'''
import unittest
import os
import sys

# Add source directory to PYTHONPATH

sys.path.insert(1,"../src") 

# modules to be tested

import yW2OO
import SceTi

# Test environment

testDataPath = "yWriter5 Sample/Export/" # yWriter5 sample project export path (precondition)
exportFileName = testDataPath+"Exported Project.html" # to be generated!

testDataFileName = testDataPath+"TestData5.html" # yWriter5 output template (precondition)
yW2OOrefFileName = testDataPath+"yW2OOreference5.html" # OOTyW output reference (precondition)
sceTiRefFileName = testDataPath+"SceTiReference5.html" # SceTi output reference (precondition)


def ReadFile(myFileName):
    myFile = open(myFileName,'r')
    myData = myFile.read()
    myFile.close()
    return(myData)
    
def CopyFile(inputFile,outputFile):
    myData = ReadFile(inputFile)
    myFile = open(outputFile,'w')
    myFile.write(myData)
    myFile.close()
    return()

# "unit to test":

def ConversionIsOK():
    CopyFile(testDataFileName,exportFileName)
    workdir = os.getcwd()
    os.chdir(testDataPath)
    yW2OO.TidyUp()
    os.chdir(workdir)
    return(ReadFile(exportFileName) == ReadFile(yW2OOrefFileName))

def AnnotationIsOK():
    workdir = os.getcwd()
    os.chdir(testDataPath)
    SceTi.AnnotateScenes()
    os.chdir(workdir)
    return(ReadFile(exportFileName) == ReadFile(sceTiRefFileName))


# "unit tests":

class ConversionTests(unittest.TestCase):

    def testOne(self):
        self.failUnless(ConversionIsOK())

    def testTwo(self):
        self.failUnless(AnnotationIsOK())

        
def main():
    unittest.main()

if __name__ == '__main__':
    main()