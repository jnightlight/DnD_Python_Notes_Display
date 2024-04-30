import helperFunctions


def populate_app_data_basic(filename):
    with open(filename) as opened_file:
        lines = opened_file.readlines()
    in_title = False
    current_indent_level = 0
    definition_dict = {}
    current_top_level_definition = ""
    changed_indent = False
    for line in lines:
        # Check to see if we're in a "header"
        if line.startswith("-----"):
            in_title = not in_title
            continue
        if in_title:
            continue
        # Use empty lines as a linebreak
        if line.isspace() or len(line) <= 0:
            if in_title:
                continue
            line = "\n"
        else:
            new_index_level = helperFunctions.get_tab_count(line)
            changed_indent = new_index_level != current_indent_level
            current_indent_level = new_index_level
            line = line.strip(" ")
            line = line.strip("\n")
        if current_indent_level == 0:
            definition_dict[line] = ""
            current_top_level_definition = line
        elif current_indent_level > 0:
            if len(current_top_level_definition) > 0:
                indent_string = ""
                if changed_indent:
                    indent_string = "  "*current_indent_level
                definition_dict[current_top_level_definition] += indent_string + line
    return definition_dict
