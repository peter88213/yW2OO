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
TEST_DATA_PATH = '../test/data/'
TEST_EXEC_PATH = '../test/yWriter5 Sample/Export/'

EXPORT_FILE = 'Exported Project.html'
SCENE_FILE = 'Auto_Descriptions.txt' 

NOT_ENOUGH_SCENES = TEST_DATA_PATH + 'Auto_Descriptions_not_enough.txt'
TOO_MANY_SCENES = TEST_DATA_PATH + 'Auto_Descriptions_too_many.txt'

# oo2yw-processed output reference (precondition)
YW2OO_REF_FILE = TEST_DATA_PATH + 'yW2OOreference5.html'
# sceti-processed output reference (precondition)
SCETI_REF_FILE = TEST_DATA_PATH + 'SceTiReference5.html'

SRC_PATH = os.getcwd()


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



class FilesFitTogether(unittest.TestCase):
    """ Test case: html export and scene descriptions fit together. """
    
    def setUp(self):
        os.chdir(SRC_PATH)
        # Place the correct html Export file.
        copy_file(TEST_DATA_PATH + EXPORT_FILE, TEST_EXEC_PATH + EXPORT_FILE)
        # Place the correct scene descriptions.
        copy_file(TEST_DATA_PATH + SCENE_FILE, TEST_EXEC_PATH + SCENE_FILE)


    def test1(self):
        """ Test yw2oo conversion only. """
        os.chdir(TEST_EXEC_PATH)
        yw2oo.main()
        os.chdir(SRC_PATH)
        self.assertEqual(read_file(TEST_EXEC_PATH + EXPORT_FILE), read_file(YW2OO_REF_FILE))

    
    def test2(self):
        """ Test yw2oo conversion and sceti annotation. """
        os.chdir(TEST_EXEC_PATH)
        yw2oo.main()
        sceti.main()
        os.chdir(SRC_PATH)
        self.assertEqual(read_file(TEST_EXEC_PATH + EXPORT_FILE), read_file(SCETI_REF_FILE))


    def tearDown(self):
        os.chdir(SRC_PATH)
        try:
            os.remove(TEST_EXEC_PATH + EXPORT_FILE)
        except:
            pass
        try:
            os.remove(TEST_EXEC_PATH + SCENE_FILE)
        except:
            pass



class NoProjectFile(unittest.TestCase):
    """ Test case: html export is missing in the Export directory. """
    
    def setUp(self):
        os.chdir(SRC_PATH)
        # Make sure there's no "html Export file" present.
        try:
            os.remove(TEST_EXEC_PATH + EXPORT_FILE)
        except:
            pass
        # Place the correct scene descriptions.
        copy_file(TEST_DATA_PATH + SCENE_FILE, TEST_EXEC_PATH + SCENE_FILE)


    def test(self):
        """ Test yw2oo conversion and sceti annotation. """
        os.chdir(TEST_EXEC_PATH)
        self.assertRaises(SystemExit, yw2oo.main)
        self.assertRaises(SystemExit, sceti.main)
        os.chdir(SRC_PATH)

    def tearDown(self):
        os.chdir(SRC_PATH)
        try:
            os.remove(TEST_EXEC_PATH + EXPORT_FILE)
        except:
            pass
        try:
            os.remove(TEST_EXEC_PATH + SCENE_FILE)
        except:
            pass


class NoDescriptionFile(unittest.TestCase):
    """ Test case: Scene descriptions file is missing. """
    
    def setUp(self):
        os.chdir(SRC_PATH)
        # Make sure there's no "scene descriptions file" present.
        try:
            os.remove(TEST_EXEC_PATH + SCENE_FILE)
        except:
            pass
        # Place the correct html Export file.
        copy_file(TEST_DATA_PATH + EXPORT_FILE, TEST_EXEC_PATH + EXPORT_FILE)


    def test(self):
        """ Test yw2oo conversion and sceti annotation. """
        os.chdir(TEST_EXEC_PATH)
        yw2oo.main()
        self.assertRaises(SystemExit, sceti.main)
        os.chdir(SRC_PATH)
        self.assertEqual(read_file(TEST_EXEC_PATH + EXPORT_FILE), read_file(YW2OO_REF_FILE))


    def tearDown(self):
        os.chdir(SRC_PATH)
        try:
            os.remove(TEST_EXEC_PATH + EXPORT_FILE)
        except:
            pass
        try:
            os.remove(TEST_EXEC_PATH + SCENE_FILE)
        except:
            pass


class DescriptionFileTooSmall(unittest.TestCase):
    """ Test case: Scene descriptions file has not enough scenes. """
    
    def setUp(self):
        os.chdir(SRC_PATH)
        copy_file(NOT_ENOUGH_SCENES, TEST_EXEC_PATH + SCENE_FILE)
        # Place the correct html Export file.
        copy_file(TEST_DATA_PATH + EXPORT_FILE, TEST_EXEC_PATH + EXPORT_FILE)


    def test(self):
        """ Test yw2oo conversion and sceti annotation. """
        os.chdir(TEST_EXEC_PATH)
        yw2oo.main()
        self.assertRaises(SystemExit, sceti.main)
        os.chdir(SRC_PATH)
        self.assertEqual(read_file(TEST_EXEC_PATH + EXPORT_FILE), read_file(YW2OO_REF_FILE))


    def tearDown(self):
        os.chdir(SRC_PATH)
        try:
            os.remove(TEST_EXEC_PATH + EXPORT_FILE)
        except:
            pass
        try:
            os.remove(TEST_EXEC_PATH + SCENE_FILE)
        except:
            pass


class DescriptionFileTooBig(unittest.TestCase):
    """ Test case: Scene descriptions file has too many scenes. """
    
    def setUp(self):
        os.chdir(SRC_PATH)
        # Place the test scene descriptions.
        copy_file(TOO_MANY_SCENES, TEST_EXEC_PATH + SCENE_FILE)
        # Place the correct html Export file.
        copy_file(TEST_DATA_PATH + EXPORT_FILE, TEST_EXEC_PATH + EXPORT_FILE)


    def test(self):
        """ Test yw2oo conversion and sceti annotation. """
        os.chdir(TEST_EXEC_PATH)
        yw2oo.main()
        self.assertRaises(SystemExit, sceti.main)
        os.chdir(SRC_PATH)
        self.assertEqual(read_file(TEST_EXEC_PATH + EXPORT_FILE), read_file(YW2OO_REF_FILE))


    def tearDown(self):
        os.chdir(SRC_PATH)
        try:
            os.remove(TEST_EXEC_PATH + EXPORT_FILE)
        except:
            pass
        try:
            os.remove(TEST_EXEC_PATH + SCENE_FILE)
        except:
            pass


def main():
    unittest.main()


if __name__ == '__main__':
    main()
