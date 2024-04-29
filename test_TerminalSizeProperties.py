import unittest
import TerminalSizeProperties


class TerminalSizePropertiesTest(unittest.TestCase):
    def test_key_box_window_basic(self):
        properties = TerminalSizeProperties.TerminalSizeProperties()
        properties.max_valid_cols = 10
        properties.max_valid_rows = 10
        properties.crunch_numbers()
        self.assertEqual(properties.key_box_window_y, 0)  # add assertion here
        self.assertEqual(properties.key_box_window_x, 0)  # add assertion here
        self.assertEqual(properties.key_box_window_cols, 5)  # add assertion here
        self.assertEqual(properties.key_box_window_rows, 10)  # add assertion here
        self.assertEqual(properties.key_window_cols, 3)  # add assertion here
        self.assertEqual(properties.key_window_rows, 8)  # add assertion here

    def test_key_box_window_odd(self):
        properties = TerminalSizeProperties.TerminalSizeProperties()
        properties.max_valid_cols = 11
        properties.max_valid_rows = 11
        properties.crunch_numbers()
        self.assertEqual(properties.key_box_window_y, 0)  # add assertion here
        self.assertEqual(properties.key_box_window_x, 0)  # add assertion here
        self.assertEqual(properties.key_box_window_cols, 5)  # add assertion here
        self.assertEqual(properties.key_box_window_rows, 11)  # add assertion here
        self.assertEqual(properties.key_window_cols, 3)  # add assertion here
        self.assertEqual(properties.key_window_rows, 9)  # add assertion here

    def test_data_box_window_basic(self):
        properties = TerminalSizeProperties.TerminalSizeProperties()
        properties.max_valid_cols = 10
        properties.max_valid_rows = 10
        properties.crunch_numbers()
        self.assertEqual(properties.data_box_window_x, 5)  # add assertion here
        self.assertEqual(properties.data_box_window_y, 0)  # add assertion here
        self.assertEqual(properties.data_box_window_cols, 5)  # add assertion here
        self.assertEqual(properties.data_box_window_rows, 10)  # add assertion here
        self.assertEqual(properties.data_window_cols, 3)  # add assertion here
        self.assertEqual(properties.data_window_rows, 8)  # add assertion here

    def test_data_box_window_odd(self):
        properties = TerminalSizeProperties.TerminalSizeProperties()
        properties.max_valid_cols = 11
        properties.max_valid_rows = 11
        properties.crunch_numbers()
        self.assertEqual(properties.data_box_window_x, 5)  # add assertion here
        self.assertEqual(properties.data_box_window_y, 0)  # add assertion here
        self.assertEqual(properties.data_box_window_cols, 6)  # add assertion here
        self.assertEqual(properties.data_box_window_rows, 11)  # add assertion here
        self.assertEqual(properties.data_window_cols, 4)  # add assertion here
        self.assertEqual(properties.data_window_rows, 9)  # add assertion here


if __name__ == '__main__':
    unittest.main()
