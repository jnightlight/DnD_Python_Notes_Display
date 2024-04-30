import math
import curses


class TerminalSizeProperties:
    max_valid_cols = 0
    max_valid_rows = 0

    # Left box with keys definitions
    key_box_window_y = 0  # (never changes, lol)
    key_box_window_x = 0  # (never changes, lol)
    key_box_window_cols = 0
    key_box_window_rows = 0
    key_window_cols = 0
    key_window_rows = 0

    # Right box with definition
    data_box_window_x = 0
    data_box_window_y = 0
    data_box_window_cols = 0
    data_box_window_rows = 0
    data_window_cols = 0
    data_window_rows = 0

    def crunch_numbers(self):
        self.key_box_window_cols = math.floor(self.max_valid_cols / 2)
        self.key_box_window_rows = self.max_valid_rows
        self.key_window_cols = self.key_box_window_cols - 2  # 2, 1 on each side
        self.key_window_rows = self.key_box_window_rows - 2

        self.data_box_window_x = self.key_box_window_cols
        self.data_box_window_cols = math.ceil(self.max_valid_cols / 2)
        self.data_box_window_rows = self.max_valid_rows
        self.data_window_cols = self.data_box_window_cols - 2
        self.data_window_rows = self.data_box_window_rows - 2


def resize_screens(size_properties, window_manager):
    curses.update_lines_cols()
    size_properties.max_valid_rows = curses.LINES - 1
    size_properties.max_valid_cols = curses.COLS - 1
    size_properties.crunch_numbers()

    window_manager.key_box_window.resize(size_properties.key_box_window_rows, size_properties.key_box_window_cols)
    window_manager.key_window.resize(size_properties.key_window_rows, size_properties.key_window_cols)

    window_manager.data_box_window.mvwin(0, size_properties.data_box_window_x)
    window_manager.data_box_window.resize(size_properties.data_box_window_rows, size_properties.data_box_window_cols)
    window_manager.data_window.mvwin(1, size_properties.data_box_window_x + 1)
    window_manager.data_window.resize(size_properties.data_window_rows, size_properties.data_window_cols)
