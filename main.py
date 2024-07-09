import curses
import curses.ascii
import os
import sys

import InputManager
import TerminalSizeProperties
import WindowManager
import helperFunctions
import loadFile
from InputManager import InputActions

MAX_VALID_DISPLAY_COLS = 10
MAX_VALID_DISPLAY_ROWS = 10


def main(stdscr):
    # Bail if not a file
    if not os.path.isfile(sys.argv[1]):
        print("This does not appear to be a file, exiting: " + sys.argv[1])
        exit(1)

    # Since it's a valid file, try to load it and populate the flat list. For now just bail if we can't parse
    app_data_dictionary = loadFile.populate_app_data_yaml(sys.argv[1])
    flat_list = helperFunctions.get_flat_key_list(app_data_dictionary)

    # Initialize GUI with curses
    size_properties = TerminalSizeProperties.TerminalSizeProperties(curses.LINES, curses.COLS)
    window_manager = WindowManager.WindowManager(size_properties, flat_list)

    # Initial printing of Key_Window
    window_manager.update_key_window_view(size_properties, "", 0)

    cur_char_x = 0
    cur_string = ''
    arrow_key_index = 0
    loop = True
    while loop:
        # Start the loop simply: refresh updated screens to user, then wait on chracter input
        window_manager.refresh_and_draw_boxes()
        in_char = window_manager.key_window.getch(size_properties.key_window_rows - 1, cur_char_x)

        # Strictly unnecessary and frankly wasteful, but hey, nothing here is crucial enough for this level of
        #  work. TODO maybe clean it up and only refresh when necessary when feature complete
        window_manager.clear_all_windows()
        if curses.LINES <= MAX_VALID_DISPLAY_ROWS or curses.COLS <= MAX_VALID_DISPLAY_COLS:
            continue

        # Updating the arrow key index (if it's changed) and grabbing the input action to work off of.
        arrow_key_index, input_action = InputManager.process_input(in_char, arrow_key_index, flat_list)

        flat_list_element = []
        # Processing our state based on incoming key
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

        matching_searches = []
        for data_path in flat_list:
            if cur_string in data_path[-1]:
                matching_searches.append(data_path)

        # Adding the current text string to the key window. Might encapsulate the "cur_string" data into the key_window
        window_manager.key_window.addnstr(size_properties.key_window_rows - 1, 0, cur_string,
                                          size_properties.key_window_cols - 2)

        # Refreshing the keys in the KeyWindow
        window_manager.update_key_window_view(size_properties, cur_string, 0)

        if len(matching_searches) == 1:
            found_element = helperFunctions.get_element_from_flat_index(app_data_dictionary, matching_searches[0])
            window_manager.update_data_window_view(found_element, window_manager, size_properties)

        if "exit" in cur_string:
            sys.exit(1)


if __name__ == "__main__":
    curses.wrapper(main)
