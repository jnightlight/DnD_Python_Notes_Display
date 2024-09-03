import curses.ascii
from enum import Enum


class InputActions(Enum):
    BACKSPACE = 0
    NEW_CHAR = 1
    CHANGE_INDEX = 2
    CLEAR_SEARCH = 3
    RESIZE = 4


class InputStates(Enum):
    SCROLL = 0
    SEARCH = 1
    EDIT = 2


def process_input(in_char, arrow_key_index, flat_list):
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
