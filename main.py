import sys
import os
import math
import curses
import curses.ascii
import TerminalSizeProperties
import helperFunctions
import loadFile
import WindowManager
import KeyWindow, DataWindow

KEY_BOX_WINDOW_HASH = "KEY_BOX_WIND"
KEY_WINDOW_HASH = "KEY_WIND"
DATA_BOX_WINDOW_HASH = "DATA_BOX_WIND"
DATA_WINDOW_HASH = "DATA_WIND"
MAX_VALID_DISPLAY_COLS = 20
MAX_VALID_DISPLAY_ROWS = 20


def create_windows(size_properties):
    window_manager = WindowManager.WindowManager()
    window_manager.key_box_window, window_manager.key_window = KeyWindow.create_key_window(size_properties)
    window_manager.data_box_window, window_manager.data_window = DataWindow.create_data_window(size_properties)
    return window_manager


def process_input(in_char, cur_char_x, cur_string, size_properties, window_manager, arrow_key_index, flat_list):
    # Replace current search string
    flat_list_element = []
    if in_char == curses.ascii.BS or in_char == curses.ascii.DEL or in_char == curses.KEY_BACKSPACE or in_char == curses.KEY_DC:
        if cur_char_x > 0:
            cur_string = cur_string[:-1]
            cur_char_x -= 1
    elif in_char == curses.KEY_RESIZE:
        TerminalSizeProperties.resize_screens(size_properties, window_manager)
        window_manager.clear_all_windows()
    elif in_char in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
        if in_char == curses.KEY_UP:
            arrow_key_index -= 1
        elif in_char == curses.KEY_DOWN:
            arrow_key_index += 1
        if arrow_key_index < 0:
            arrow_key_index = len(flat_list)

        # ATM, this is a seperate elif statement. Maybe make this all a switch soon
        if in_char == curses.KEY_LEFT:
            cur_string = ''
            cur_char_x = 0
        else:
            flat_list_element = flat_list[arrow_key_index % len(flat_list)]
            cur_string = flat_list_element[-1]
            cur_string = cur_string.strip('\n')
            cur_char_x = len(cur_string)
    elif curses.ascii.isascii(in_char):
        window_manager.key_window.addch(size_properties.key_window_rows - 1, cur_char_x, in_char)
        cur_string += chr(in_char)
        cur_char_x += 1
    return cur_char_x, cur_string, arrow_key_index, flat_list_element


def main(stdscr):
    size_properties = TerminalSizeProperties.TerminalSizeProperties()

    size_properties.max_valid_rows = curses.LINES - 1
    size_properties.max_valid_cols = curses.COLS - 1
    size_properties.crunch_numbers()

    window_manager = create_windows(size_properties)

    key_box_window = window_manager.key_box_window
    key_window = window_manager.key_window
    TerminalSizeProperties.resize_screens(size_properties, window_manager)

    # Bail if not a file
    if not os.path.isfile(sys.argv[1]):
        # logging.error("invalid file path provided")
        exit(1)
    app_data_dictionary = loadFile.populate_app_data_yaml(sys.argv[1])
    flat_list = helperFunctions.get_flat_key_list(app_data_dictionary)
    loop = True

    KeyWindow.print_advanced_keys_recursive(key_box_window, app_data_dictionary, [], size_properties, 0, 1)

    cur_char_x = 0
    cur_string = ''
    arrow_key_index = 0
    while loop:
        window_manager.refresh_and_draw_boxes()
        in_char = key_window.getch(size_properties.key_window_rows - 1, cur_char_x)
        window_manager.clear_all_windows()
        if curses.LINES <= MAX_VALID_DISPLAY_ROWS or curses.COLS <= MAX_VALID_DISPLAY_COLS:
            continue

        # MODIFYING:
        cur_char_x, cur_string, arrow_key_index, flat_list_element = process_input(in_char, cur_char_x, cur_string,
                                                                                   size_properties, window_manager,
                                                                                   arrow_key_index, flat_list)
        window_manager.key_window.addnstr(size_properties.key_window_rows - 1, 0, cur_string,
                                          size_properties.key_window_cols - 2)

        #matching_words = print_keys(key_box_window, app_data_dictionary, cur_string, size_properties)
        KeyWindow.print_advanced_keys_recursive(key_box_window, app_data_dictionary, flat_list_element, size_properties,
                                                0, 1)
        found_element = helperFunctions.get_element_from_flat_index(app_data_dictionary, flat_list_element)
        if isinstance(found_element, list):
            to_print = ""
            for element in found_element:
                if isinstance(element, dict):
                    to_print += str(element.keys()) + "\n"
                    DataWindow.print_data_window_string(window_manager, size_properties, to_print)
        elif isinstance(found_element, str):
            DataWindow.print_data_window_string(window_manager, size_properties, found_element)
        #        if len(matching_words) == 1:
        #            #data_window.addnstr(0, 0, app_data_dictionary[matching_words[0]], 1500)
        if "exit" in cur_string:
            sys.exit(1)


if __name__ == "__main__":
    curses.wrapper(main)
