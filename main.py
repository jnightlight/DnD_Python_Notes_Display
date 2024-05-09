import curses
import curses.ascii
import os
import sys

import DataWindow
import KeyWindow
import TerminalSizeProperties
import WindowManager
import helperFunctions
import loadFile

MAX_VALID_DISPLAY_COLS = 10
MAX_VALID_DISPLAY_ROWS = 10


def create_windows(size_properties):
    window_manager = WindowManager.WindowManager()
    window_manager.key_box_window, window_manager.key_window = KeyWindow.create_key_window(size_properties)
    window_manager.data_box_window, window_manager.data_window = DataWindow.create_data_window(size_properties)
    return window_manager


def process_input(in_char, cur_char_x, cur_string, size_properties, window_manager, arrow_key_index, flat_list):
    should_search = False
    # Replace current search string
    flat_list_element = []
    #Backspace back a character
    if in_char == curses.ascii.BS or in_char == curses.ascii.DEL or in_char == curses.KEY_BACKSPACE or in_char == curses.KEY_DC:
        if cur_char_x > 0:
            cur_string = cur_string[:-1]
            cur_char_x -= 1
            should_search = True
    # Screen resize
    elif in_char == curses.KEY_RESIZE:
        TerminalSizeProperties.resize_screens(size_properties, window_manager)
        window_manager.clear_all_windows()
    # Incoming arrow keys for navigating key window
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
        should_search = True
    return cur_char_x, cur_string, arrow_key_index, flat_list_element, should_search


def main(stdscr):
    # Bail if not a file
    if not os.path.isfile(sys.argv[1]):
        exit(1)

    #Since it's a valid file, try to load it and populate the flat list. For now just bail if we can't parse
    app_data_dictionary = loadFile.populate_app_data_yaml(sys.argv[1])
    flat_list = helperFunctions.get_flat_key_list(app_data_dictionary)

    #Initialize GUI with curses
    size_properties = TerminalSizeProperties.TerminalSizeProperties(curses.LINES, curses.COLS)
    window_manager = create_windows(size_properties)

    #Initial printing of data
    KeyWindow.print_advanced_keys_recursive(window_manager.key_box_window, app_data_dictionary, [], size_properties, 0, 1)

    cur_char_x = 0
    cur_string = ''
    arrow_key_index = 0
    loop = True
    while loop:
        window_manager.refresh_and_draw_boxes()
        in_char = window_manager.key_window.getch(size_properties.key_window_rows - 1, cur_char_x)
        window_manager.clear_all_windows()
        if curses.LINES <= MAX_VALID_DISPLAY_ROWS or curses.COLS <= MAX_VALID_DISPLAY_COLS:
            continue

        # MODIFYING:
        cur_char_x, cur_string, arrow_key_index, flat_list_element, should_search = process_input(in_char, cur_char_x,
                                                                                                   cur_string,
                                                                                                   size_properties,
                                                                                                   window_manager,
                                                                                                   arrow_key_index,
                                                                                                   flat_list)
        window_manager.key_window.addnstr(size_properties.key_window_rows - 1, 0, cur_string,
                                          size_properties.key_window_cols - 2)

        KeyWindow.print_advanced_keys_recursive(window_manager.key_box_window, app_data_dictionary, flat_list_element, size_properties,
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
