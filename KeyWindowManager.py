import curses
import math


class KeyWindowManager:
    def __init__(self, key_window, key_box_window):
        self.cur_string = ""
        self.key_window = key_window
        self.key_box_window = key_box_window

    # Display Dict should be defined as a dict with a list of categories. EACH category contains EITHER:
    #   A list of more categories OR
    #   A list of string:string key value pairs with actual information
    def print_advanced_keys_recursive(self, display_list, flat_list_element, size_properties, indent, cur_row):
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
                    self.key_window.addstr(cur_row, 1, key, formatting)
                    cur_row += 1
                    if cur_row >= size_properties.max_valid_rows - 1:
                        return cur_row
                elif isinstance(inside, list):
                    key = (" " * indent) + key
                    if len(key) > size_properties.max_valid_cols:
                        key = key[len(key) - (math.fabs(len(key) - size_properties.max_valid_cols))]
                    self.key_window.addstr(cur_row, 1, key, formatting)
                    cur_row += 1
                    if cur_row >= size_properties.max_valid_rows - 1:
                        return cur_row
                    cur_row = self.print_advanced_keys_recursive(inside, flat_list_element, size_properties, indent + 1,
                                                                 cur_row)
        return cur_row
