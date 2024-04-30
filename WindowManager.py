
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
