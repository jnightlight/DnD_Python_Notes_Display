import helperFunctions


def populate_app_data_basic(filename):
    with open(filename) as opened_file:
        lines = opened_file.readlines()
    in_title = False
    current_indent_level = 0
    definition_dict = {}
    current_top_level_definition = ""
    for line in lines:
        # Check to see if we're in a "header"
        if line.startswith("-----"):
            in_title = not in_title
            continue
        if in_title:
            continue
        # Ignore completely empty lines
        if line.isspace() or len(line) <= 0:
            continue
        new_index_level = helperFunctions.get_tab_count(line)
        if not (new_index_level == current_indent_level):
            current_indent_level = new_index_level
        line = line.strip(" ")
        line = line.strip("\n")
        if current_indent_level == 0:
            definition_dict[line] = ""
            current_top_level_definition = line
        elif current_indent_level > 0:
            if len(current_top_level_definition) > 0:
                definition_dict[current_top_level_definition] += line
    return definition_dict
