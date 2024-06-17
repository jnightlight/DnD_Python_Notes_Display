import curses


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


def safe_clear(window):
    if not window == 0:
        window.clear()


def safe_refresh(window):
    if not window == 0:
        window.refresh()


def safe_box_and_refresh(window):
    if not window == 0:
        window.box()
        window.refresh()


class WindowManager:
    key_window = 0
    key_box_window = 0
    data_window = 0
    data_box_window = 0

    def clear_all_windows(self):
        safe_clear(self.key_window)
        safe_clear(self.key_box_window)
        safe_clear(self.data_window)
        safe_clear(self.data_box_window)

    def refresh_and_draw_boxes(self):
        safe_box_and_refresh(self.data_box_window)
        safe_box_and_refresh(self.key_box_window)
        safe_refresh(self.key_window)
        safe_refresh(self.data_window)
