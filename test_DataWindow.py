import unittest

import DataWindow
import TerminalSizeProperties
from DataWindow import WordAndFormat


class TerminalSizePropertiesTest(unittest.TestCase):
    def test_splitting_single_line_of_words(self):
        TEST_SIMPLE_STRING = "This is a test"
        expected_list = ["This", "is", "a", "test"]

        properties = TerminalSizeProperties.TerminalSizeProperties(999, 999)
        lines = DataWindow.split_entry_into_formatted_lines_of_words(properties, TEST_SIMPLE_STRING)
        expected_word_and_format_list = []
        for word in expected_list:
            expected_word_and_format_list.append(WordAndFormat(word))
        self.assertEqual([expected_word_and_format_list], lines)

    def test_splitting_2_lines_of_words(self):
        TEST_SIMPLE_STRING = "This is a test\nThis is part 2"
        expected_data = [
            ["This", "is", "a", "test"],
            [DataWindow.INDENT_STRING + "This", "is", "part", "2"]
        ]

        properties = TerminalSizeProperties.TerminalSizeProperties(999, 999)
        lines = DataWindow.split_entry_into_formatted_lines_of_words(properties, TEST_SIMPLE_STRING)
        expected_word_and_format_list = []
        words = []
        for word_list in expected_data:
            for word in word_list:
                words.append(WordAndFormat(word))
            expected_word_and_format_list.append(words)
            words = []

        self.assertEqual(expected_word_and_format_list, lines)

    def test_splitting_multiple_linebreaks_one_word(self):
        TEST_SIMPLE_STRING = "This is a test\nThis\n is line 3"
        expected_data = [
            ["This", "is", "a", "test"],
            [DataWindow.INDENT_STRING + "This"],
            [DataWindow.INDENT_STRING + "is", "line", "3"]
        ]

        properties = TerminalSizeProperties.TerminalSizeProperties(999, 999)
        lines = DataWindow.split_entry_into_formatted_lines_of_words(properties, TEST_SIMPLE_STRING)
        expected_word_and_format_list = []
        words = []
        for word_list in expected_data:
            for word in word_list:
                words.append(WordAndFormat(word))
            expected_word_and_format_list.append(words)
            words = []

        self.assertEqual(expected_word_and_format_list, lines)


if __name__ == '__main__':
    unittest.main()
