import unittest

from main import extract_title

class TestMain(unittest.TestCase):
    def test_extract_title(self):
        md = "# This is an 'h1' title."
        results = extract_title(md)
        expected = "This is an 'h1' title."
        self.assertEqual(results, expected)

    def test_extract_title_error(self):
        md = "This is an 'h1' title."
        self.assertRaises(ValueError, lambda: extract_title(md))




if __name__ == "__main__":
    unittest.main()
