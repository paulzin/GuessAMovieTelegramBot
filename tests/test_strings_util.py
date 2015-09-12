import strings_util
import unittest


class StringsUtilTest(unittest.TestCase):
    def test_get_hint(self):
        print(strings_util.get_hint("The Great Gatsby", None))
        print(strings_util.get_hint("The Great Gatsby", "*** Great Gatsby"))
        print(strings_util.get_hint("The Great Gatsby", "*** ***** Gatsby"))
        print(strings_util.get_hint("Guardians of the Galaxy", "Guardians ** *** Galaxy"))

if __name__ == '__main__':
    unittest.main()
