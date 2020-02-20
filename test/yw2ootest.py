""" Python unit tests for the yW2OO project.

Test suite for yw2oo.py (does conversion) and sceti.py (does annotation).

For further information see https://github.com/peter88213/yW2OO
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import unittest
import zipfile

import yw2oo


# Test environment

# The paths are relative to the "src" directory,
# where this script is placed and executed

TEST_PATH = os.getcwd()
TEST_DATA_PATH = 'data/'
TEST_EXEC_PATH = 'yw7/'

# To be placed in TEST_DATA_PATH:

# Test data
TEST_FILE = 'yWriter Sample Project.yw7'
EXPORT_FILE = 'yWriter Sample Project.odt'

DOCUMENT_CONTENT = 'content.xml'
DOCUMENT_META = 'meta.xml'
DOCUMENT_STYLES = 'styles.xml'


def read_file(inputFile):
    try:
        with open(inputFile, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        # HTML files exported by a word processor may be ANSI encoded.
        with open(inputFile, 'r') as f:
            return f.read()


def copy_file(inputFile, outputFile):
    with open(inputFile, 'rb') as f:
        myData = f.read()
    with open(outputFile, 'wb') as f:
        f.write(myData)
    return()


class NormalOperation(unittest.TestCase):
    """Test case: Normal operation."""

    def setUp(self):
        os.chdir(TEST_PATH)
        try:
            os.remove(TEST_EXEC_PATH + TEST_FILE)
        except:
            pass
        # Place the correct html Export file.
        copy_file(TEST_DATA_PATH + TEST_FILE,
                  TEST_EXEC_PATH + TEST_FILE)
        try:
            os.remove(TEST_EXEC_PATH + EXPORT_FILE)
        except:
            pass

    def test_yw2oo(self):
        """ Test yw2oo. """
        os.chdir(TEST_EXEC_PATH)

        yw2oo.main()
        # self.assertEqual(, 'SUCCESS: "' + EXPORT_FILE + '" saved.')
        os.chdir(TEST_PATH)

        with zipfile.ZipFile(TEST_EXEC_PATH + EXPORT_FILE, 'r') as myzip:
            myzip.extract(DOCUMENT_CONTENT, TEST_EXEC_PATH)
            myzip.extract(DOCUMENT_STYLES, TEST_EXEC_PATH)

        self.assertEqual(read_file(TEST_EXEC_PATH + DOCUMENT_CONTENT),
                         read_file(TEST_DATA_PATH + DOCUMENT_CONTENT))
        self.assertEqual(read_file(TEST_EXEC_PATH + DOCUMENT_STYLES),
                         read_file(TEST_DATA_PATH + DOCUMENT_STYLES))


class NoProjectFile(unittest.TestCase):
    """Test case: yWriter project file is not present."""

    def setUp(self):
        os.chdir(TEST_PATH)
        # Make sure there's no yWriter project file present.
        try:
            os.remove(TEST_EXEC_PATH + TEST_FILE)
        except:
            pass

    def test_all(self):
        """ Test both yw2oo and sceti. """
        os.chdir(TEST_EXEC_PATH)
        self.assertEqual(yw2oo.main(), 'ERROR: No yWriter 7 project found.')
        os.chdir(TEST_PATH)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
