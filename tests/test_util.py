from unittest import TestCase

from pyqt_spellcheck.util import find_word_bounds


class TestUtil(TestCase):  # noqa: D101
    def test_find_word_bounds(self):
        self.assertEqual((0, 5), find_word_bounds("hello", 0))
        self.assertEqual((0, 5), find_word_bounds("hello", 1))
        self.assertEqual((0, 5), find_word_bounds("hello", 2))
        self.assertEqual((0, 5), find_word_bounds("hello", 4))
        self.assertEqual((6, 11), find_word_bounds("hello again world", 7))
        self.assertEqual((12, 17), find_word_bounds("hello again world", 13))
