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
@change: 2019-10-23 v1.2.0 General refactoring.
    Organized tests in several different test cases including fault conditions. 
"""
import os
import sys
import unittest

import sceti
import yw2oo


# Test environment

# The paths are relative to the "src" directory,
# where this script is placed and executed

SRC_PATH = os.getcwd()
TEST_DATA_PATH = '../test/data/'
TEST_EXEC_PATH = '../test/yWriter5 Sample/Export/'

# To be placed in TEST_DATA_PATH:

# Test data
EXPORT_FILE = 'Exported Project.html'
SCENE_FILE = 'Auto_Descriptions.txt' 

# Test data for fault conditions 
NOT_ENOUGH_SCENES = 'Auto_Descriptions_not_enough.txt'
TOO_MANY_SCENES = 'Auto_Descriptions_too_many.txt'

# Reference data for correct execution
YW2OO_REF_FILE = 'yW2OOreference5.html'
SCETI_REF_FILE = 'SceTiReference5.html'



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



class NormalOperation(unittest.TestCase):
    """ Test case: Normal operation
    
        Condition: html export and scene descriptions fit together. 
        Expected result: The output files match the reference files. 
    """
    
    def setUp(self):
        os.chdir(SRC_PATH)
        # Place the correct html Export file.
        copy_file(TEST_DATA_PATH + EXPORT_FILE, TEST_EXEC_PATH + EXPORT_FILE)
        # Place the correct scene descriptions.
        copy_file(TEST_DATA_PATH + SCENE_FILE, TEST_EXEC_PATH + SCENE_FILE)


    def test1(self):
        """ Step 1: Test yw2oo conversion only. """
        os.chdir(TEST_EXEC_PATH)
        yw2oo.main()
        os.chdir(SRC_PATH)
        self.assertEqual(read_file(TEST_EXEC_PATH + EXPORT_FILE), read_file(TEST_DATA_PATH + YW2OO_REF_FILE))

    
    def test2(self):
        """ Step 2: Test both yw2oo conversion and sceti annotation. """
        os.chdir(TEST_EXEC_PATH)
        yw2oo.main()
        sceti.main()
        os.chdir(SRC_PATH)
        self.assertEqual(read_file(TEST_EXEC_PATH + EXPORT_FILE), read_file(TEST_DATA_PATH + SCETI_REF_FILE))


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



class NotPreprocessed(unittest.TestCase):
    """ Test case: Wrong execution order or unknown preprocessor failure. 
    
        Condition: sceti.py processes "raw" html export.
        Expected result: sceti.py exits with error; html remains unchanged.
    """
    
    def setUp(self):
        os.chdir(SRC_PATH)
        # Place the correct html Export file.
        copy_file(TEST_DATA_PATH + EXPORT_FILE, TEST_EXEC_PATH + EXPORT_FILE)
        # Place the correct scene descriptions.
        copy_file(TEST_DATA_PATH + SCENE_FILE, TEST_EXEC_PATH + SCENE_FILE)


    def test(self):
        """ Test sceti annotation only. """
        os.chdir(TEST_EXEC_PATH)
        self.assertRaises(SystemExit, sceti.main)
        os.chdir(SRC_PATH)
        self.assertEqual(read_file(TEST_EXEC_PATH + EXPORT_FILE), read_file(TEST_DATA_PATH + EXPORT_FILE))


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
    """ Test case: Exported html project file is not present.
    
        Condition: scene descriptions file is present, html file isn't.
        Expected result: Both yw2oo.py and sceti.py exit with error.
    """
    
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
    """ Test case: Exported scene descriptions file is not present. 
    
        Condition: html file is present, scene descriptions file isn't.
        Expected result: yw2oo's output file matches the reference; 
            sceti.py exits with error.      
    """
    
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
        self.assertEqual(read_file(TEST_EXEC_PATH + EXPORT_FILE), read_file(TEST_DATA_PATH + YW2OO_REF_FILE))


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
    """ Test case: Scene descriptions file has not enough scenes. 
    
        Condition: Scene descriptions file has less scenes 
            than html export file.
        Expected result: yw2oo's output file matches the reference; 
            sceti.py exits with error.      
    """
    
    def setUp(self):
        os.chdir(SRC_PATH)
        copy_file(TEST_DATA_PATH + NOT_ENOUGH_SCENES, TEST_EXEC_PATH + SCENE_FILE)
        # Place the correct html Export file.
        copy_file(TEST_DATA_PATH + EXPORT_FILE, TEST_EXEC_PATH + EXPORT_FILE)


    def test(self):
        """ Test yw2oo conversion and sceti annotation. """
        os.chdir(TEST_EXEC_PATH)
        yw2oo.main()
        self.assertRaises(SystemExit, sceti.main)
        os.chdir(SRC_PATH)
        self.assertEqual(read_file(TEST_EXEC_PATH + EXPORT_FILE), read_file(TEST_DATA_PATH + YW2OO_REF_FILE))


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
    """ Test case: Scene descriptions file has too many scenes. 
    
    Condition: Scene descriptions file has more scenes 
        than html export file.
    Expected result: yw2oo's output file matches the reference; 
        sceti.py exits with error.      
    """
    
    def setUp(self):
        os.chdir(SRC_PATH)
        # Place the test scene descriptions.
        copy_file(TEST_DATA_PATH + TOO_MANY_SCENES, TEST_EXEC_PATH + SCENE_FILE)
        # Place the correct html Export file.
        copy_file(TEST_DATA_PATH + EXPORT_FILE, TEST_EXEC_PATH + EXPORT_FILE)


    def test(self):
        """ Test yw2oo conversion and sceti annotation. """
        os.chdir(TEST_EXEC_PATH)
        yw2oo.main()
        self.assertRaises(SystemExit, sceti.main)
        os.chdir(SRC_PATH)
        self.assertEqual(read_file(TEST_EXEC_PATH + EXPORT_FILE), read_file(TEST_DATA_PATH + YW2OO_REF_FILE))


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