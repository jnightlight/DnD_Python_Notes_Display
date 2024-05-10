import curses
import math


def create_key_window(size_properties):
    key_box_window = curses.newwin(size_properties.key_box_window_rows,
                                   size_properties.key_box_window_cols,
                                   0,
                                   0)
    key_window = key_box_window.derwin(size_properties.key_window_rows,
                                       size_properties.key_window_cols,
                                       1,
                                       1)
    key_window.keypad(True)
    return key_box_window, key_window


# Display Dict should be defined as a dict with a list of categories. EACH category contains EITHER:
#   A list of more categories OR
#   A list of string:string key value pairs with actual information
def print_advanced_keys_recursive(window, display_list, flat_list_element, size_properties, indent, cur_row):
    for internal_dict in display_list:
        for key in internal_dict.keys():
            inside = internal_dict[key]
            formatting = curses.A_NORMAL
            bold = False
            for path in flat_list_element:
                if key in path[-1]:
                    bold = True
            if len(flat_list_element) > 0 and bold:
                formatting = curses.A_STANDOUT
            if isinstance(inside, str):
                key = (" " * indent) + key
                if len(key) > size_properties.max_valid_cols:
                    key = key[len(key) - (math.fabs(len(key) - size_properties.max_valid_cols))]
                window.addstr(cur_row, 1, key, formatting)
                cur_row += 1
                if cur_row >= size_properties.max_valid_rows - 1:
                    return cur_row
            elif isinstance(inside, list):
                key = (" " * indent) + key
                if len(key) > size_properties.max_valid_cols:
                    key = key[len(key) - (math.fabs(len(key) - size_properties.max_valid_cols))]
                window.addstr(cur_row, 1, key, formatting)
                cur_row += 1
                if cur_row >= size_properties.max_valid_rows - 1:
                    return cur_row
                cur_row = print_advanced_keys_recursive(window, inside, flat_list_element, size_properties, indent + 1,
                                                        cur_row)
    return cur_row


def print_keys(window, display_dict, selected_key, size_properties):
    row = 1
    matching_words = []
    if size_properties.max_valid_cols <= MAX_VALID_DISPLAY_COLS or size_properties.max_valid_rows <= MAX_VALID_DISPLAY_ROWS:
        return matching_words
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
