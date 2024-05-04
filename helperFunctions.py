import math


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
    return math.ceil(tab_count + (space_count / 4))


def get_flat_key_list(yaml_list):
    full_list = []
    depth_list = []
    for in_dict in yaml_list:
         full_list += get_flat_key_list_recursive(in_dict, depth_list)
    return full_list


def get_flat_key_list_recursive(cur_dict, current_depth_key_list):
    flat_key_list = []
    for key in cur_dict.keys():
        current_depth_key_list.append(key)
        list_element = current_depth_key_list
        flat_key_list.append(list(list_element))
        inside = cur_dict[key]
        if isinstance(inside[0], dict):
            for deeper_dict in inside:
                new_list = get_flat_key_list_recursive(deeper_dict, current_depth_key_list)
                for element in new_list:
                    flat_key_list.append(element)
        elif isinstance(inside[0], str):
            pass
        current_depth_key_list.remove(key)
    return flat_key_list

def get_element_from_flat_index(list, key_path):
    cur_list = list
    for key in key_path:
        cur_dict = dict[key]
    return cur_dict