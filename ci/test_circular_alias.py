#!/usr/bin/python

import urllib.request
from urllib.error import HTTPError
import re
import os
import ast


def search_for_alias(filename):
    """
    Checks for alias front matter. Returns None if no alias declared

    returns: type:list of strings e.g. ['new/path/','second/path/']
    """
    with open(filename, 'r') as f:
        lines = f.readlines()

    for line in lines:
        match = re.match(r'^alias: \[.*\]', line)
        if match:
            new_line = match.group()
            # Literal evaluation of brackets in alias
            return ast.literal_eval(new_line[new_line.find("["):])


def _check_duplicate_alias(alias_paths, absolute_file_path):
    """
    Checks if alias is matching file path. Prints offending file

    returns: type:None
    """
    duplicate = False
    for alias in alias_paths:
        match = re.search(r'docs/.*\.md$', absolute_file_path)
        if match:
            maybe_duplicate = match.group()
            maybe_duplicate = maybe_duplicate.lstrip('docs/').rstrip('//.md')
            alias = alias.rstrip('//')
            if alias == maybe_duplicate:
                duplicate = True
                print("Circular alias '{}' in file: {}".format(alias, absolute_file_path))
    return duplicate


def gather_images(filename):
    """
    TODO: Parse nested bracket syntax
    """
    total_images = 0
    with open(filename, 'r') as f:
        lines = f.readlines()
    for line in lines:
        match = re.search(r'\(.*docs/.*\.(jpg|png)\)', line)
        if match:
            total_images += 1
    return total_images


def test_circular_alias():
    source_dir = '.'
    alias_paths = []
    alias_ok = True
    for dir_name, subdir, files in os.walk(source_dir):
        for file_name in files:
            if re.match(r'.*\.md$', file_name):
                # images += gather_images(dir_name + "/" + file_name)
                aliases = search_for_alias(dir_name + "/" + file_name)
                if aliases:
                    alias_paths += aliases
                    alias_ok += False
    local_url = "http://127.0.0.1:1313/docs/"
    for alias in alias_paths:
        try:
            urllib.request.urlopen(local_url + alias).getcode()
        except HTTPError:
            print(alias + " is a broken path")
    assert alias_ok == True


if __name__ == '__main__':
    test_circular_alias()

