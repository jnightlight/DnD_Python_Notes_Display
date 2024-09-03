"""
WindowManager.py
Interfaces with both windows, used to modify the display on either or both windows.
"""
import curses

import DataWindow
import KeyWindowElement
import KeyWindowManager


def create_key_window(size_properties):
    """
    Initialize the windows displaying the key data

    :param size_properties: TerminalSizeProperty object with current display bounds
    :return key_box_window, key_window: Two NCurses window objects, the first holding the display box (the outline
        of the GUI), the second being the windows with the actual text
    """
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
    """
    Initialize the windows displaying the definition data

    :param size_properties: TerminalSizeProperty object with current display bounds
    :return key_box_window, key_window: Two NCurses window objects, the first holding the display box (the outline
        of the GUI), the second being the windows with the actual text
    """
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
    """
    WindowManager class to operate upon member windows and subWindow Managers
    """

    def __init__(self, size_properties):
        self.key_box_window, self.key_window = create_key_window(size_properties)
        self.key_window_manager = KeyWindowManager.KeyWindowManager(self.key_window, self.key_box_window)
        self.data_box_window, self.data_window = create_data_window(size_properties)

    def clear_all_windows(self):
        """
        Call safe_clear on all windows, to make sure they're set to window instances before clearing
        """
        safe_clear(self.key_window)
        safe_clear(self.key_box_window)
        safe_clear(self.data_window)
        safe_clear(self.data_box_window)

    def refresh_and_draw_boxes(self):
        """
        safely (check for unset windows) draw outlines and window data to the screen
        """
        safe_box_and_refresh(self.data_box_window)
        safe_box_and_refresh(self.key_box_window)
        safe_refresh(self.key_window)
        safe_refresh(self.data_window)

    def update_key_window_view(self, data_flat_list, size_properties, search_filter, print_start_index):
        """
        Update the contents of the key window
        Note that this change is not represented on the screen until we refresh_and_draw_boxes()

        :param data_flat_list: The Flat list of our entries to display
        :param size_properties: The up-to-date size properties of the terminal so we know our drawing bounds
        :param search_filter: If non-empty, will only display entries that contain the filter
        :param print_start_index: The offset for starting drawing from the element, will be used to "scroll"
        :return:
        """
        element_list = []
        if search_filter == "":
            for entry in data_flat_list:
                element = KeyWindowElement.KeyWindowElement(entry, False)
                element_list.append(element)
        else:
            for entry in data_flat_list:
                element = KeyWindowElement.KeyWindowElement(entry, False)
                if search_filter in entry[-1]:
                    element_list = self.ensure_breadcrumbs_present(element_list, element)
                    element.add_formatting(curses.A_STANDOUT)
                    element_list.append(element)
        self.key_window_manager.print_key_window(element_list, size_properties, print_start_index)

    def ensure_breadcrumbs_present(self, element_list, element):
        """
        Insert breadcrumbs (entry chain, see "flat_list") to show the category of our found entry
        :param element_list: List of elements to retrieve breadcrumbs from
        :param element: The element for which we are ensuring there are breadcrumbs
        :return: The modified element list with the ordered breadcrumbs
        """
        breadcrumb_path = []
        # Iterate through entries in the flat
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
