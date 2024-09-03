import curses.ascii
from enum import Enum


def add_breadcrumbs(found_matching_keys, key):
    breadcrumb_path = []
    for breadcrumb in key[:-1]:
        breadcrumb_path.append(breadcrumb)
        if breadcrumb_path not in found_matching_keys:
            # We don't want to pass this by reference and modify it in the Element obj, so we make a copy
            breadcrumb_path_copy = breadcrumb_path[:]
            found_matching_keys.append(breadcrumb_path_copy)
    return found_matching_keys


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


def get_element_from_flat_index(app_data_dict, key_path):
    if len(key_path) == 0:
        return ""
    cur_list = app_data_dict
    new_cur_list = []
    key_index = 0
    should_continue = True
    while should_continue:
        for element in cur_list:
            if isinstance(element, dict) and key_path[key_index] in element.keys():
                new_cur_list = element[key_path[key_index]]
                key_index += 1
                if key_index == len(key_path):
                    return new_cur_list
                break
            else:
                continue
        if len(new_cur_list) > 0:
            cur_list = new_cur_list
        else:
            return ""


class DataManager:
    def __init__(self, data_dict):
        self.data_dict = data_dict
        self.full_flat_list = get_flat_key_list(self.data_dict)

    def get_matching_keys(self, search_string, include_breadcrumbs=False):
        matching_keys = []
        for key in self.full_flat_list:
            if search_string in key[-1]:
                if include_breadcrumbs:
                    matching_keys = add_breadcrumbs(matching_keys, key)
                matching_keys.append(key)
        return matching_keys
