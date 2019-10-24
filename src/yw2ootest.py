""" Python unit tests for the yW2OO project.

@summary: Test suite for yw2oo.py (does conversion) and sceti.py (does annotation)
@author: Peter Triesberger
@see: https://github.com/peter88213/yw2oo
@license: The MIT License (https://opensource.org/licenses/mit-license.php)
@copyright: (c) 2019, Peter Triesberger
@precondition: This script is to be placed in "<project dir>/test"
@precondition: The subjects to testing must exist in "<project dir>/src"
@precondition: A test environment as specified below must exist.
@precondition: "<project dir>/test/yWriter5 Sample/Auto_Descriptions.txt" must exist.
@since: 2019-10-21
@change: 2019-10-21 v1.0.0 Adapted subjects' function calls.
@change: 2019-10-23 v1.1.0 Adapted  to new directory structure and test subjects:
    sceti v1.3.1, yw2oo v1.8.0.
    Further refactoring according to PEP 8 style guide
    (see https://www.python.org/dev/peps/pep-0008/)
"""
import os
import sys
import unittest

import sceti
import yw2oo


# Test environment

# yWriter5 sample project export path (precondition)
TEST_DATA_PATH = "../test/data/"
TEST_EXEC_PATH = "../test/yWriter5 Sample/Export/"
EXPORT_FILE = TEST_EXEC_PATH + "Exported Project.html"  # to be generated!

# yWriter5 export template (precondition)
TEST_DATA_FILE = TEST_DATA_PATH + "TestData5.html"
# oo2yw-processed output reference (precondition)
YW2OO_REF_FILE = TEST_DATA_PATH + "yW2OOreference5.html"
# sceti-processed output reference (precondition)
SCETI_REF_FILE = TEST_DATA_PATH + "SceTiReference5.html"


def read_file(myFileName):
    myFile = open(myFileName, 'r')
    myData = myFile.read()
    myFile.close()
    return(myData)


def copy_file(inputFile, outputFile):
    myData = read_file(inputFile)
    myFile = open(outputFile, 'w')
    myFile.write(myData)
    myFile.close()
    return()


def conversion_is_ok():
    """ Process html Export and compare result with reference file. """
    # Generate a temporary "html Export file" to be processed.
    copy_file(TEST_DATA_FILE, EXPORT_FILE)
    # Change to emulated yWriter "Export" folder.
    workdir = os.getcwd()
    os.chdir(TEST_EXEC_PATH)
    yw2oo.main()
    os.chdir(workdir)
    return(read_file(EXPORT_FILE) == read_file(YW2OO_REF_FILE))


def annotation_is_ok():
    """ Add scenes to html file and compare result with reference file. """
    # Change to emulated yWriter "Export" folder.
    workdir = os.getcwd()
    os.chdir(TEST_EXEC_PATH)
    sceti.main()
    os.chdir(workdir)
    return(read_file(EXPORT_FILE) == read_file(SCETI_REF_FILE))


# "unit tests":

class conversion_tests(unittest.TestCase):

    def test1(self):
        self.assertTrue(conversion_is_ok())

    def test2(self):
        self.assertTrue(annotation_is_ok())


def main():
    unittest.main()


if __name__ == '__main__':
    main()
