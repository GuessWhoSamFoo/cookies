# -*- coding: utf-8 -*-
import pytest
from contextlib import redirect_stdout
import regex
import os
import fnmatch
import sys

def test_whitespace():
    source_dir = '.'
    if len(sys.argv) > 1:
        source_dir = sys.argv[1]
    no_whitespace = True
    for root, dirnames, filenames in os.walk(source_dir):
        for filename in fnmatch.filter(filenames, '*.md'):
            with open(os.path.join(root, filename)) as infile:
                for line_number, line in enumerate(infile,1):
                    match_obj = regex.search(r'[ \t]+$', line)
                    if match_obj:
                        no_whitespace = False
                        with redirect_stdout(open(os.devnull, 'w')):
                            print(str(filename) + ": trailing whitespace at " + str(line_number) + ":" + str(match_obj.start()))
    assert no_whitespace == True

if __name__ == "__main__":
    test_whitespace()
