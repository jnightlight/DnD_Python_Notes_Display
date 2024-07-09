class KeyWindowManager:
    def __init__(self, key_window, key_box_window):
        self.cur_string = ""
        self.key_window = key_window
        self.key_box_window = key_box_window

    # Takes an ORDERED list of elements, and attempts to display them given the size restrictions.
    def print_key_window(self, ordered_element_list, size_properties, print_start_index=0):
        printed_lines = 0
        for element in ordered_element_list[print_start_index:len(ordered_element_list)]:
            # TODO: This only has a -2 to work in the pycharm debugger. There's a better way to do this, lol
            if printed_lines >= size_properties.max_valid_rows - 2:
                # TODO: Log a warning to an error file
                return
            display_string = element.path_list[-1]
            minimized_indicator = ("+" if element.minimized else "-")
            line_string = (" " * element.indent) + display_string + " " + minimized_indicator
            max_line_size = size_properties.max_valid_cols - 2
            line_string = line_string[0:max_line_size]
            self.key_window.addstr(printed_lines, element.indent, line_string, element.formatting)
            printed_lines += 1
