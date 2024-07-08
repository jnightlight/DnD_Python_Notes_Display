class KeyWindowElement:
    def __init__(self, path_list, minimized=False, formatted=False, formatting=0):
        self.path_list = path_list
        self.indent = max(0, len(self.path_list) - 1)

        self.formatted = formatted
        self.formatting = formatting

        self.minimized = minimized

    def add_formatting(self, formatting_value):
        self.formatting = formatting_value
        self.formatted = True

    def strip_formatting(self, formatting_value):
        self.formatting = 0
        self.formatted = False

    def set_path_list(self, path_list):
        self.path_list = path_list
        self.indent = max(0, len(self.path_list) - 1)
