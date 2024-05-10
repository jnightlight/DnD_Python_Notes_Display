import curses
import curses.ascii
import os
import sys
from enum import Enum

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


class InputActions(Enum):
    BACKSPACE = 0
    NEW_CHAR = 1
    CHANGE_INDEX = 2
    CLEAR_SEARCH = 3
    RESIZE = 4


def process_input(in_char, size_properties, window_manager, arrow_key_index, flat_list):
    input_action = InputActions.BACKSPACE

    # Backspace back a character
    if in_char == curses.ascii.BS or in_char == curses.ascii.DEL or in_char == curses.KEY_BACKSPACE or in_char == curses.KEY_DC:
        input_action = InputActions.BACKSPACE

    # Screen resize
    elif in_char == curses.KEY_RESIZE:
        input_action = InputActions.RESIZE

    # Incoming arrow keys for navigating key window
    elif in_char in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_RIGHT]:
        input_action = InputActions.CHANGE_INDEX
        if in_char == curses.KEY_UP:
            input_action = InputActions.CHANGE_INDEX
            arrow_key_index -= 1
            # Wraparound
            if arrow_key_index < 0:
                arrow_key_index = len(flat_list)
        elif in_char == curses.KEY_DOWN:
            arrow_key_index += 1
    elif in_char == curses.KEY_LEFT:
        input_action = InputActions.CLEAR_SEARCH
    # Any other ascii char //TODO: enter key breaks this, lol. Good for fast exit
    elif curses.ascii.isascii(in_char):
        input_action = InputActions.NEW_CHAR
    return arrow_key_index, input_action


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
    KeyWindow.print_advanced_keys_recursive(window_manager.key_box_window, app_data_dictionary, [], size_properties, 0,
                                            1)

    cur_char_x = 0
    cur_string = ''
    arrow_key_index = 0
    loop = True
    while loop:
        #Start the loop simply: refresh updated screens to user, then wait on chracter input
        window_manager.refresh_and_draw_boxes()
        in_char = window_manager.key_window.getch(size_properties.key_window_rows - 1, cur_char_x)

        #Strictly unnecessary and frankly wasteful, but hey, nothing here is crucial enough for this level of
        #  work. TODO maybe clean it up and only refresh when necessary when feature complete
        window_manager.clear_all_windows()
        if curses.LINES <= MAX_VALID_DISPLAY_ROWS or curses.COLS <= MAX_VALID_DISPLAY_COLS:
            continue

        # This is where we process the incoming character and update some data
        arrow_key_index, input_action = process_input(in_char,
                                                      size_properties,
                                                      window_manager,
                                                      arrow_key_index,
                                                      flat_list)

        flat_list_element = []
        match input_action:
            case InputActions.BACKSPACE:
                # If we're at the beginning, noop. Otherwise, pop most recent char and queue up an updated search
                if len(cur_string) > 0:
                    cur_string = cur_string[:-1]
                pass
            case InputActions.NEW_CHAR:
                window_manager.key_window.addch(size_properties.key_window_rows - 1, len(cur_string), in_char)
                cur_string += chr(in_char)
                pass
            case InputActions.CHANGE_INDEX:
                flat_list_element = flat_list[arrow_key_index % len(flat_list)]
                cur_string = flat_list_element[-1]
                cur_string = cur_string.strip('\n')
            case InputActions.CLEAR_SEARCH:
                cur_string = ''
                pass
            case InputActions.RESIZE:
                TerminalSizeProperties.resize_screens(size_properties, window_manager)
                # Clearing here in case there's not an out of bounds draw on a future refresh accidentally
                window_manager.clear_all_windows()

        #Adding the current text string to the key window. This can probably be moved to KeyWindow soon
        window_manager.key_window.addnstr(size_properties.key_window_rows - 1, 0, cur_string,
                                          size_properties.key_window_cols - 2)

        #Refreshing the keys in the KeyWindow
        KeyWindow.print_advanced_keys_recursive(window_manager.key_box_window, app_data_dictionary, flat_list_element,
                                                size_properties,
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
