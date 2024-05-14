import unittest

import TerminalSizeProperties


class TerminalSizePropertiesTest(unittest.TestCase):
    def test_key_box_window_basic(self):
        properties = TerminalSizeProperties.TerminalSizeProperties(10, 10)
        properties.crunch_numbers()
        self.assertEqual(properties.key_box_window_y, 0)
        self.assertEqual(properties.key_box_window_x, 0)
        self.assertEqual(properties.key_box_window_cols, 5)
        self.assertEqual(properties.key_box_window_rows, 10)
        self.assertEqual(properties.key_window_cols, 3)
        self.assertEqual(properties.key_window_rows, 8)

    def test_key_box_window_odd(self):
        properties = TerminalSizeProperties.TerminalSizeProperties(11, 11)
        properties.crunch_numbers()
        self.assertEqual(properties.key_box_window_y, 0)
        self.assertEqual(properties.key_box_window_x, 0)
        self.assertEqual(properties.key_box_window_cols, 5)
        self.assertEqual(properties.key_box_window_rows, 11)
        self.assertEqual(properties.key_window_cols, 3)
        self.assertEqual(properties.key_window_rows, 9)

    def test_data_box_window_basic(self):
        properties = TerminalSizeProperties.TerminalSizeProperties(10, 10)
        properties.crunch_numbers()
        self.assertEqual(properties.data_box_window_x, 5)
        self.assertEqual(properties.data_box_window_y, 0)
        self.assertEqual(properties.data_box_window_cols, 5)
        self.assertEqual(properties.data_box_window_rows, 10)
        self.assertEqual(properties.data_window_cols, 3)
        self.assertEqual(properties.data_window_rows, 8)

    def test_data_box_window_odd(self):
        properties = TerminalSizeProperties.TerminalSizeProperties(11, 11)
        properties.crunch_numbers()
        self.assertEqual(properties.data_box_window_x, 5)
        self.assertEqual(properties.data_box_window_y, 0)
        self.assertEqual(properties.data_box_window_cols, 6)
        self.assertEqual(properties.data_box_window_rows, 11)
        self.assertEqual(properties.data_window_cols, 4)
        self.assertEqual(properties.data_window_rows, 9)


if __name__ == '__main__':
    unittest.main()
