import curses
import math

INDENT_STRING = "    "


def create_data_window(size_properties):
    data_box_window = curses.newwin(size_properties.data_box_window_rows,
                                    size_properties.data_box_window_cols,
                                    0,
                                    size_properties.data_box_window_x)
    data_window = data_box_window.derwin(size_properties.data_window_rows,
                                         size_properties.data_window_cols,
                                         1,
                                         1)
    return data_box_window, data_window


def print_data_window_data(window_manager, app_data_dictionary, size_properties, data_word):
    total_size = size_properties.data_window_cols * size_properties.data_window_rows

    window_manager.data_window.addnstr(0, 0, app_data_dictionary[data_word], math.floor(total_size / 1.3))


def print_data_window_string(window_manager, size_properties, to_print):
    line_list_index = 0
    line_list = []
    cur_line = INDENT_STRING
    word_list = to_print.split(" ")
    for word in word_list:
        if len(word) <= 0:
            continue
        if len(cur_line) + len(word) >= size_properties.data_window_cols:
            line_list.append(cur_line)
            cur_line = word + " "
            line_list_index += 1
        else:
            cur_line += word + " "
        if "\n" in word:
            line_break_split_list = word.split("\n")
            line_list.append(cur_line)
            cur_line = INDENT_STRING + line_break_split_list[1] + " "
            line_list_index += 1

    print_index = 0
    while print_index < len(line_list) and print_index < size_properties.data_window_rows:
        window_manager.data_window.addnstr(print_index, 0, line_list[print_index], size_properties.data_window_cols)
        print_index += 1


def print_data_window_text(found_element, window_manager, size_properties):
    if isinstance(found_element, list):
        to_print = ""
        for element in found_element:
            if isinstance(element, dict):
                to_print += str(element.keys()) + "\n"
                print_data_window_string(window_manager, size_properties, to_print)
    elif isinstance(found_element, str):
        print_data_window_string(window_manager, size_properties, found_element)
