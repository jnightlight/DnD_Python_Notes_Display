def print_data_window_data(window_manager, app_data_dictionary, size_properties, data_word):
    if size_properties.max_valid_cols <= MAX_VALID_DISPLAY_COLS or size_properties.max_valid_rows <= MAX_VALID_DISPLAY_ROWS:
        return
    total_size = size_properties.data_window_cols * size_properties.data_window_rows
    current_cursor_y = 0

    window_manager.data_window.addnstr(0, 0, app_data_dictionary[data_word], math.floor(total_size/1.3))
