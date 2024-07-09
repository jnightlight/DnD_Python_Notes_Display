import curses

import DataWindow
import KeyWindowElement
import KeyWindowManager


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
    def __init__(self, size_properties, data_flat_list):
        self.key_box_window, self.key_window = create_key_window(size_properties)
        self.key_window_manager = KeyWindowManager.KeyWindowManager(self.key_window, self.key_box_window)

        self.data_box_window, self.data_window = create_data_window(size_properties)
        self.data_flat_list = data_flat_list

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

    def update_key_window_view(self, size_properties, search_filter, print_start_index):
        element_list = []
        if search_filter == "":
            for entry in self.data_flat_list:
                element = KeyWindowElement.KeyWindowElement(entry, False)
                element_list.append(element)
        else:
            for entry in self.data_flat_list:
                element = KeyWindowElement.KeyWindowElement(entry, False)
                if search_filter in entry[-1]:
                    element_list = self.ensure_breadcrumbs_present(element_list, element)
                    element.add_formatting(curses.A_STANDOUT)
                    element_list.append(element)
        self.key_window_manager.print_key_window(element_list, size_properties, print_start_index)

    def ensure_breadcrumbs_present(self, element_list, element):
        breadcrumb_path = []
        for breadcrumb in element.path_list[:-1]:
            breadcrumb_path.append(breadcrumb)
            if not any(elem for elem in element_list if elem.path_list == breadcrumb_path):
                # We don't want to pass this by reference and modify it in the Element obj, so we make a copy
                breadcrumb_path_copy = breadcrumb_path[:]
                bread_element = KeyWindowElement.KeyWindowElement(breadcrumb_path_copy, False)
                element_list.append(bread_element)
        return element_list

    def update_data_window_view(self, found_element, window_manager, size_properties):
        DataWindow.print_data_window_text(found_element, window_manager, size_properties)
