def get_tab_count(line_string):
    space_count = 0
    tab_count = 0
    for char in line_string:
        if char == ' ':
            space_count += 1
        elif char == '\t':
            tab_count += 1
        else:
            break
    return tab_count + (space_count / 4)
