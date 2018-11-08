# -*- coding: UTF-8 -*-
import json


def json_to_dict(filename):
    with open(filename, 'r') as source:
        data = json.load(source)
    return data


def list_to_string(array):
    string = ''.join(array)
    return string


def reverse_list_search(db, target):
    for _ in db:
        if _ in target:
            return True


def strip_whitespace(string):
    string.split()
    new_string = ''.join(string.split())
    return new_string
