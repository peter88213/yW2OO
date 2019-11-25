""" Python unit tests for the yW2OO project.

Test suite for yw2oo.py (does conversion) and sceti.py (does annotation).

For further information see https://github.com/peter88213/yW2OO
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import unittest

import sceti
import yw2oo


# Test environment

# The paths are relative to the "src" directory,
# where this script is placed and executed

TEST_PATH = os.getcwd()
TEST_DATA_PATH = 'data/'
TEST_EXEC_PATH = 'yWriter5 Sample/Export/'

# To be placed in TEST_DATA_PATH:

# Test data
EXPORT_FILE = 'Exported Project.html'
SCENE_FILE = 'Auto_Descriptions.txt'
CSV_FILE = 'Exported Project.csv'

# Test data for fault conditions
NOT_ENOUGH_SCENES = 'Auto_Descriptions_not_enough.txt'
TOO_MANY_SCENES = 'Auto_Descriptions_too_many.txt'

# Reference data for correct execution
YW2OO_REF_FILE = 'yW2OOreference5.html'
if sceti.CREATE_BOOKMARKS:
    SCETI_REF_FILE = 'SceTiReference5-Bookmarks.html'
    CSV_REF_FILE = 'Exported Project-Bookmarks.csv'
else:
    SCETI_REF_FILE = 'SceTiReference5.html'
    CSV_REF_FILE = 'Exported Project.csv'


def read_file(inputFile):
    with open(inputFile, 'r') as f:
        return(f.read())


def copy_file(inputFile, outputFile):
    myData = read_file(inputFile)
    with open(outputFile, 'w') as f:
        f.write(myData)
    return()


class NormalOperation(unittest.TestCase):
    """ Test case: Normal operation

        Condition: html export and scene descriptions fit together. 
        Expected result: The output files match the reference files. 
    """

    def setUp(self):
        os.chdir(TEST_PATH)
        # Place the correct html Export file.
        copy_file(TEST_DATA_PATH + EXPORT_FILE,
                  TEST_EXEC_PATH + EXPORT_FILE)
        # Place the correct scene descriptions.
        copy_file(TEST_DATA_PATH + SCENE_FILE,
                  TEST_EXEC_PATH + SCENE_FILE)

    def test_data(self):
        """ Verify test data integrity. """
        # Test input data must differ from the reference test output data.
        self.assertNotEqual(
            read_file(TEST_DATA_PATH + EXPORT_FILE),
            read_file(TEST_DATA_PATH + YW2OO_REF_FILE))
        self.assertNotEqual(
            read_file(TEST_DATA_PATH + EXPORT_FILE),
            read_file(TEST_DATA_PATH + SCETI_REF_FILE))
        self.assertNotEqual(
            read_file(TEST_DATA_PATH + YW2OO_REF_FILE),
            read_file(TEST_DATA_PATH + SCETI_REF_FILE))
        # 'Normal operation' test data must differ from the faulty test data.
        self.assertNotEqual(
            read_file(TEST_DATA_PATH + SCENE_FILE),
            read_file(TEST_DATA_PATH + NOT_ENOUGH_SCENES))
        self.assertNotEqual(
            read_file(TEST_DATA_PATH + SCENE_FILE),
            read_file(TEST_DATA_PATH + TOO_MANY_SCENES))

    def test_yw2oo(self):
        """ Test yw2oo without running sceti afterwards. """
        os.chdir(TEST_EXEC_PATH)
        yw2oo.main()
        os.chdir(TEST_PATH)
        # html file must contain all the replacements.
        self.assertEqual(read_file(TEST_EXEC_PATH + EXPORT_FILE),
                         read_file(TEST_DATA_PATH + YW2OO_REF_FILE))

    def test_sceti(self):
        """ Run yw2oo and test sceti. """
        os.chdir(TEST_EXEC_PATH)
        yw2oo.main()
        sceti.main()
        os.chdir(TEST_PATH)
        # html file must contain all the replacements plus annotations.
        self.assertEqual(read_file(TEST_EXEC_PATH + EXPORT_FILE),
                         read_file(TEST_DATA_PATH + SCETI_REF_FILE))
        # csv file to be generated
        self.assertEqual(read_file(TEST_EXEC_PATH + CSV_FILE),
                         read_file(TEST_DATA_PATH + CSV_REF_FILE))

    def tearDown(self):
        os.chdir(TEST_PATH)
        try:
            os.remove(TEST_EXEC_PATH + EXPORT_FILE)
        except:
            pass
        try:
            os.remove(TEST_EXEC_PATH + SCENE_FILE)
        except:
            pass
        try:
            os.remove(TEST_EXEC_PATH + CSV_REF_FILE)
        except:
            pass


class ProjectFileReadOnly(unittest.TestCase):
    """ Test case: File can not be written.

        Condition: Exported html project file is read-only. 
        Expected result: Both yw2oo.py and sceti.py exit with error.
    """

    def setUp(self):
        os.chdir(TEST_PATH)
        # Place the correct html Export file.
        copy_file(TEST_DATA_PATH + EXPORT_FILE,
                  TEST_EXEC_PATH + EXPORT_FILE)
        # Set html Export file read-only.
        os.system('attrib +R "' +
                  os.path.normpath(TEST_EXEC_PATH + EXPORT_FILE) + '"')
        # Place the correct scene descriptions.
        copy_file(TEST_DATA_PATH + SCENE_FILE,
                  TEST_EXEC_PATH + SCENE_FILE)

    def test_all(self):
        """ Test both yw2oo and sceti. """
        os.chdir(TEST_EXEC_PATH)
        # Fault condition must cause 'yw2oo' program termination.
        self.assertRaises(SystemExit, yw2oo.main)
        # Fault condition must cause 'sceti' program termination.
        self.assertRaises(SystemExit, sceti.main)
        os.chdir(TEST_PATH)

    def tearDown(self):
        os.chdir(TEST_PATH)
        # Set html Export file read + write.
        os.system('attrib -R "' +
                  os.path.normpath(TEST_EXEC_PATH + EXPORT_FILE) + '"')
        try:
            os.remove(TEST_EXEC_PATH + EXPORT_FILE)
        except:
            pass
        try:
            os.remove(TEST_EXEC_PATH + SCENE_FILE)
        except:
            pass
        try:
            os.remove(TEST_EXEC_PATH + CSV_REF_FILE)
        except:
            pass


class NotPreprocessed(unittest.TestCase):
    """ Test case: Wrong execution order or unknown preprocessor failure. 

        Condition: sceti.py processes 'raw' html export.
        Expected result: sceti.py exits with error; html file remains unchanged.
    """

    def setUp(self):
        os.chdir(TEST_PATH)
        # Place the correct html Export file.
        copy_file(TEST_DATA_PATH + EXPORT_FILE,
                  TEST_EXEC_PATH + EXPORT_FILE)
        # Place the correct scene descriptions.
        copy_file(TEST_DATA_PATH + SCENE_FILE,
                  TEST_EXEC_PATH + SCENE_FILE)

    def test_sceti(self):
        """ Test sceti without running yw2oo before. """
        os.chdir(TEST_EXEC_PATH)
        # Fault condition must cause 'sceti' program termination.
        self.assertRaises(SystemExit, sceti.main)
        os.chdir(TEST_PATH)
        # html file must remain unchanged.
        self.assertEqual(read_file(TEST_EXEC_PATH + EXPORT_FILE),
                         read_file(TEST_DATA_PATH + EXPORT_FILE))

    def tearDown(self):
        os.chdir(TEST_PATH)
        try:
            os.remove(TEST_EXEC_PATH + EXPORT_FILE)
        except:
            pass
        try:
            os.remove(TEST_EXEC_PATH + SCENE_FILE)
        except:
            pass
        try:
            os.remove(TEST_EXEC_PATH + CSV_REF_FILE)
        except:
            pass


class NoProjectFile(unittest.TestCase):
    """ Test case: Exported html project file is not present.

        Condition: scene descriptions file is present, html file isn't.
        Expected result: Both yw2oo.py and sceti.py exit with error.
    """

    def setUp(self):
        os.chdir(TEST_PATH)
        # Make sure there's no "html Export file" present.
        try:
            os.remove(TEST_EXEC_PATH + EXPORT_FILE)
        except:
            pass
        # Place the correct scene descriptions.
        copy_file(TEST_DATA_PATH + SCENE_FILE,
                  TEST_EXEC_PATH + SCENE_FILE)

    def test_all(self):
        """ Test both yw2oo and sceti. """
        os.chdir(TEST_EXEC_PATH)
        # Fault condition must cause 'yw2oo' program termination.
        self.assertRaises(SystemExit, yw2oo.main)
        # Fault condition must cause 'sceti' program termination.
        self.assertRaises(SystemExit, sceti.main)
        os.chdir(TEST_PATH)

    def tearDown(self):
        os.chdir(TEST_PATH)
        try:
            os.remove(TEST_EXEC_PATH + EXPORT_FILE)
        except:
            pass
        try:
            os.remove(TEST_EXEC_PATH + SCENE_FILE)
        except:
            pass
        try:
            os.remove(TEST_EXEC_PATH + CSV_REF_FILE)
        except:
            pass


class NoDescriptionFile(unittest.TestCase):
    """ Test case: Exported scene descriptions file is not present. 

        Condition: html file is present, scene descriptions file isn't.
        Expected result: yw2oo's output file matches the reference; 
            sceti.py exits with error.      
    """

    def setUp(self):
        os.chdir(TEST_PATH)
        # Make sure there's no "scene descriptions file" present.
        try:
            os.remove(TEST_EXEC_PATH + SCENE_FILE)
        except:
            pass
        # Place the correct html Export file.
        copy_file(TEST_DATA_PATH + EXPORT_FILE,
                  TEST_EXEC_PATH + EXPORT_FILE)

    def test_sceti(self):
        """ Run yw2oo and test sceti. """
        os.chdir(TEST_EXEC_PATH)
        yw2oo.main()
        # Fault condition must cause 'sceti' program termination.
        self.assertRaises(SystemExit, sceti.main)
        os.chdir(TEST_PATH)
        # html file must remain unchanged.
        self.assertEqual(read_file(TEST_EXEC_PATH + EXPORT_FILE),
                         read_file(TEST_DATA_PATH + YW2OO_REF_FILE))

    def tearDown(self):
        os.chdir(TEST_PATH)
        try:
            os.remove(TEST_EXEC_PATH + EXPORT_FILE)
        except:
            pass
        try:
            os.remove(TEST_EXEC_PATH + SCENE_FILE)
        except:
            pass
        try:
            os.remove(TEST_EXEC_PATH + CSV_REF_FILE)
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
        os.chdir(TEST_PATH)
        copy_file(TEST_DATA_PATH + NOT_ENOUGH_SCENES,
                  TEST_EXEC_PATH + SCENE_FILE)
        # Place the correct html Export file.
        copy_file(TEST_DATA_PATH + EXPORT_FILE,
                  TEST_EXEC_PATH + EXPORT_FILE)

    def test_sceti(self):
        """ Run yw2oo and test sceti. """
        os.chdir(TEST_EXEC_PATH)
        yw2oo.main()
        # Fault condition must cause 'sceti' program termination.
        self.assertRaises(SystemExit, sceti.main)
        os.chdir(TEST_PATH)
        # html file must remain unchanged.
        self.assertEqual(read_file(TEST_EXEC_PATH + EXPORT_FILE),
                         read_file(TEST_DATA_PATH + YW2OO_REF_FILE))

    def tearDown(self):
        os.chdir(TEST_PATH)
        try:
            os.remove(TEST_EXEC_PATH + EXPORT_FILE)
        except:
            pass
        try:
            os.remove(TEST_EXEC_PATH + SCENE_FILE)
        except:
            pass
        try:
            os.remove(TEST_EXEC_PATH + CSV_REF_FILE)
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
        os.chdir(TEST_PATH)
        # Place the test scene descriptions.
        copy_file(TEST_DATA_PATH + TOO_MANY_SCENES,
                  TEST_EXEC_PATH + SCENE_FILE)
        # Place the correct html Export file.
        copy_file(TEST_DATA_PATH + EXPORT_FILE,
                  TEST_EXEC_PATH + EXPORT_FILE)

    def test_sceti(self):
        """ Run yw2oo and test sceti. """
        os.chdir(TEST_EXEC_PATH)
        yw2oo.main()
        # Fault condition must cause 'sceti' program termination.
        self.assertRaises(SystemExit, sceti.main)
        os.chdir(TEST_PATH)
        # html file must remain unchanged.
        self.assertEqual(read_file(TEST_EXEC_PATH + EXPORT_FILE),
                         read_file(TEST_DATA_PATH + YW2OO_REF_FILE))

    def tearDown(self):
        os.chdir(TEST_PATH)
        try:
            os.remove(TEST_EXEC_PATH + EXPORT_FILE)
        except:
            pass
        try:
            os.remove(TEST_EXEC_PATH + SCENE_FILE)
        except:
            pass
        try:
            os.remove(TEST_EXEC_PATH + CSV_REF_FILE)
        except:
            pass


def main():
    unittest.main()


if __name__ == '__main__':
    main()
