import math

def print_data_window_data(window_manager, app_data_dictionary, size_properties, data_word):
    total_size = size_properties.data_window_cols * size_properties.data_window_rows
    current_cursor_y = 0

    window_manager.data_window.addnstr(0, 0, app_data_dictionary[data_word], math.floor(total_size/1.3))


def print_data_window_string(window_manager, size_properties, to_print):
    line_list_index = 0
    line_list = []
    cur_line = "    "
    word_list = to_print.split(" ")
    for word in word_list:
        if len(cur_line) + len(word) >= size_properties.data_window_cols:
            line_list.append(cur_line)
            cur_line = word + " "
            line_list_index += 1
        else:
            cur_line += word + " "
        if "\n" in word:
            line_break_split_list = word.split("\n")
            line_list.append(cur_line)
            cur_line = "    " + line_break_split_list[1] + " "
            line_list_index += 1
    total_size = size_properties.data_window_cols * size_properties.data_window_rows
    current_cursor_y = 0

    print_index = 0
    while print_index < len(line_list) and print_index < size_properties.data_window_rows:
        window_manager.data_window.addnstr(print_index, 0, line_list[print_index], size_properties.data_window_cols)
        print_index += 1
