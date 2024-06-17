import curses

INDENT_STRING = "    "


class WordAndFormat:
    word = ''
    curses_attributes = curses.A_NORMAL

    def __init__(self, word="", curses_attributes=curses.A_NORMAL):
        self.word = word
        self.format = curses_attributes

    def __str__(self):
        return "(" + self.word + ", " + str(self.format) + ")"

    def __eq__(self, other):
        return self.word == other.word and self.format == other.format


def add_formatting(formatting, format_to_add):
    return formatting | format_to_add


def remove_formatting(formatting, format_to_remove):
    return formatting & ~format_to_remove


def split_entry_into_formatted_lines_of_words(window_manager, size_properties, to_print):
    current_visual_line = INDENT_STRING
    out_line_list = []
    out_line_words = [WordAndFormat(INDENT_STRING, curses.A_NORMAL)]
    in_line_list = to_print.split("\n")
    formatting = curses.A_NORMAL
    for line in in_line_list:
        word_split = line.split(" ")
        for word in word_split:
            if len(word) <= 0:
                continue
            # formatting, need to move this to it's own function or something.
            #   IE: check if starts/ends w/ "<" and ">", then do a formatting check, otherwise fallthrough
            if word.strip() == "<bold>":
                formatting = add_formatting(formatting, curses.A_BOLD)
                continue
            if word.strip() == "</bold>":
                formatting = remove_formatting(formatting, curses.A_BOLD)
                continue
            if word.strip() == "<italic>":
                formatting = add_formatting(formatting, curses.A_ITALIC)
                continue
            if word.strip() == "</italic>":
                formatting = remove_formatting(formatting, curses.A_ITALIC)
                continue
            if word == "<highlight>":
                formatting = add_formatting(formatting, curses.A_STANDOUT)
                continue
            if word == "</highlight>":
                formatting = remove_formatting(formatting, curses.A_STANDOUT)
                continue
            if word == "<blink>":
                formatting = add_formatting(formatting, curses.A_BLINK)
                continue
            if word == "</blink>":
                formatting = remove_formatting(formatting, curses.A_BLINK)
                continue

            fancyWord = WordAndFormat(word, formatting)
            if len(current_visual_line) + len(word) >= size_properties.data_window_cols:
                out_line_list.append(out_line_words)
                current_visual_line = word + " "
                out_line_words = [fancyWord]
            else:
                current_visual_line += word + " "
                out_line_words.append(fancyWord)

        out_line_list.append(out_line_words)
        out_line_words = [WordAndFormat(INDENT_STRING, curses.A_NORMAL)]
        current_visual_line = INDENT_STRING
    if len(out_line_words) > 0:
        out_line_list.append(out_line_words)
    word_index = 0
    line_index = 0
    cur_x = 0
    while line_index < len(out_line_list) and line_index < size_properties.data_window_rows:
        for fancyWord in out_line_list[line_index]:
            window_manager.data_window.addnstr(line_index, cur_x, fancyWord.word, size_properties.data_window_cols,
                                               fancyWord.format)
            word_index += 1
            cur_x += len(fancyWord.word) + 1
        cur_x = 0
        word_index = 0
        line_index += 1


def print_data_window_text(found_element, window_manager, size_properties):
    if isinstance(found_element, list):
        to_print = ""
        for element in found_element:
            if isinstance(element, dict):
                to_print += str(element.keys()) + "\n"
                split_entry_into_formatted_lines_of_words(window_manager, size_properties, to_print)
    elif isinstance(found_element, str):
        split_entry_into_formatted_lines_of_words(window_manager, size_properties, found_element)
