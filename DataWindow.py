import math

def print_data_window_data(window_manager, app_data_dictionary, size_properties, data_word):
    total_size = size_properties.data_window_cols * size_properties.data_window_rows
    current_cursor_y = 0

    window_manager.data_window.addnstr(0, 0, app_data_dictionary[data_word], math.floor(total_size/1.3))


def print_data_window_string(window_manager, app_data_dictionary, size_properties, to_print):
    total_size = size_properties.data_window_cols * size_properties.data_window_rows
    current_cursor_y = 0

    window_manager.data_window.addnstr(0, 0, to_print, math.floor(total_size/1.3))
