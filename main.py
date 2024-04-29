import sys
import os
import math
import curses
import curses.ascii
import TerminalSizeProperties
import loadFile


def print_keys(window, display_dict, selected_key, size_properties):
    row = 1
    matching_words = []
    for key in display_dict.keys():
        if len(key) > size_properties.max_valid_cols:
            key = key[len(key) - (math.fabs(len(key) - size_properties.max_valid_cols))]
        attribute = curses.A_NORMAL
        if selected_key in key:
            attribute = curses.A_STANDOUT
            matching_words.append(key)
        window.addstr(row, 1, key, attribute)
        row += 1
        if row >= size_properties.max_valid_rows - 1:
            break
    return matching_words


def main(stdscr):
    curses.echo()
    size_properties = TerminalSizeProperties.TerminalSizeProperties()

    size_properties.max_valid_rows = curses.LINES - 1
    size_properties.max_valid_cols = curses.COLS - 1
    size_properties.crunch_numbers()

    key_box_window = curses.newwin(size_properties.key_box_window_rows,
                                   size_properties.key_box_window_cols,
                                   0,
                                   0)
    key_window = key_box_window.derwin(size_properties.key_window_rows,
                                       size_properties.key_window_cols,
                                       1,
                                       1)
    key_window.keypad(True)
    data_box_window = curses.newwin(size_properties.data_box_window_rows,
                                    size_properties.data_box_window_cols,
                                    0,
                                    size_properties.data_box_window_x)
    data_window = data_box_window.derwin(size_properties.data_window_rows,
                                         size_properties.data_window_cols,
                                         1,
                                         1)
    TerminalSizeProperties.resize_screens(size_properties, key_box_window, key_window, data_box_window, data_window)

    # Bail if not a file
    if not os.path.isfile(sys.argv[1]):
        # logging.error("invalid file path provided")
        exit(1)
    app_data_dictionary = loadFile.populate_app_data_basic(sys.argv[1])
    loop = True

    print_keys(key_box_window, app_data_dictionary, "intro", size_properties)
    cur_char_x = 0
    cur_string = ''
    arrow_key_index = 0
    while loop:
        TerminalSizeProperties.resize_screens(size_properties, key_box_window, key_window, data_box_window, data_window)

        data_box_window.box()
        data_box_window.refresh()
        key_box_window.box()
        key_box_window.refresh()
        key_window.refresh()
        data_window.refresh()

        in_char = key_window.getch(size_properties.key_window_rows - 1, cur_char_x)

        key_window.clear()
        key_box_window.clear()
        data_box_window.clear()
        data_window.clear()

        # Replace current search string
        if in_char == curses.ascii.BS or in_char == curses.ascii.DEL or in_char == curses.KEY_BACKSPACE or in_char == curses.KEY_DC:
            if cur_char_x > 0:
                cur_string = cur_string[:-1]
                cur_char_x -= 1
        elif in_char == curses.KEY_RESIZE:
            TerminalSizeProperties.resize_screens(size_properties, key_box_window, key_window, data_box_window,
                                                  data_window)
        elif in_char in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
            keys = list(app_data_dictionary.keys())
            if in_char == curses.KEY_UP:
                arrow_key_index -= 1
            if in_char == curses.KEY_DOWN:
                arrow_key_index += 1
                if arrow_key_index < 0:
                    arrow_key_index = len(keys)
            if in_char == curses.KEY_LEFT:
                cur_string = ''
                cur_char_x = 0
            else:
                cur_string = keys[arrow_key_index % len(keys)]
                cur_string = cur_string.strip('\n')
                cur_char_x = len(cur_string)
        elif curses.ascii.isascii(in_char):
            key_window.addch(size_properties.key_window_rows - 1, cur_char_x, in_char)
            cur_string += chr(in_char)
            cur_char_x += 1
        key_window.addnstr(size_properties.key_window_rows - 1, 0, cur_string, size_properties.key_window_cols - 2)

        matching_words = print_keys(key_box_window, app_data_dictionary, cur_string, size_properties)
        if len(matching_words) == 1:
            data_window.addnstr(0, 0, app_data_dictionary[matching_words[0]], 100)
        if "exit" in cur_string:
            sys.exit(1)


if __name__ == "__main__":
    curses.wrapper(main)
