# -*- coding: utf-8 -*-
import pytest
from contextlib import redirect_stdout
import regex
import re
import os
import fnmatch
import sys
import csv
import urllib.request
from urllib.error import HTTPError, URLError
import ast


LOCALHOST = "http://127.0.0.1:1313/docs/"


@pytest.fixture(scope='module', autouse=True)
def md_index(path='.', extension='*.md'):
    index = []
    exclude = ['node_modules']
    for root, dirnames, filenames in os.walk(path):
        dirnames[:] = [d for d in dirnames if d not in exclude]
        for filename in fnmatch.filter(filenames, extension):
            index.append(os.path.join(root, filename))
    return index


@pytest.fixture(params=md_index())
def md_filepaths(request):
    return request.param


@pytest.fixture(params=[open(i) for i in md_index()])
def md_files(request):
    return request.param

class TestFile:

    def setup_method(self):
        pass

    #@pytest.mark.skip(reason="pass")
    def test_filename(self, md_filepaths):
        if any(e in md_filepaths for e in ['README.md', 'CHANGELOG.md']):
            assert True
        else:
            assert md_filepaths.islower() == True,'Filename should be lowercase' 

    def test_404(self):
        f = open('result.csv')
        assert sum([1 for line in f]) == 1,'404 response in HTML - see scraper logs'


class TestLine:

    def setup_method(self, method):
        pass

    def test_whitespace(self, md_files):
        has_whitespace = False
        for line_number, line in enumerate(md_files, 1):
            match = regex.search(r'[\t]+$', line)
            if match:
                has_whitespace = True
                print("Trailing whitespace at " + str(line_number) + ":" + str(match.start()))
        md_files.seek(0)
        assert has_whitespace == False


    def test_alias(self, md_filepaths):
        aliases = []
        f = open(md_filepaths)
        valid_alias = True
        for line in f:
            match = re.match(r'^aliases: \[.*\]', line)
            if match:
                new_line = match.group()
                # Literal evaluation of brackets in alias
                aliases += ast.literal_eval(new_line[new_line.find("["):])
        if md_filepaths.lstrip('./content/')[:-3] in [a.rstrip('/') for a in aliases]:
            valid_alias = False
            print('Circular alias: ' + md_filepaths)
        try:
            for alias in aliases:
                urllib.request.urlopen(LOCALHOST + alias).getcode()
        except HTTPError:
            valid_alias = False
            print('404 alias: ' + alias)
        assert valid_alias == True,'Not a valid alias'




rules = [
    {'rule': '"Open-source" should be hyphenated',
     'regex': 'open source'},
    {'rule': "Avoid the use of 'we', 'our', and 'let\'s'",
     'regex': "([Ww]e\s|\s[Oo]ur\s|[Ll]et's)"},
    {'rule':"No trailing whitespace",
     'regex':"[ \t]+$"},
    {'rule': "Use a single space after a period",
     'regex': "\.  "},
    {'rule':"Prefer the Oxford comma",
     'regex':"(?:\w+,\s+){1,}\w+\s+and\s+\w+."},
]

def main():
    source_dir = '.'
    if len(sys.argv) > 1:
        source_dir = sys.argv[1]
    for root, dirnames, filenames in os.walk(source_dir):
        for filename in fnmatch.filter(filenames,'*.md'):
            with open(os.path.join(root,filename)) as infile:
                for line_number, line in enumerate(infile,1):
                    for rule in rules:
                        reg = regex.compile(rule['regex'])
                        match_obj = regex.search(reg, line)
                        if match_obj:
                            print(str(filename) + ":\t\t" + str(line_number) + ":" + str(match_obj.start()) + "\t\t" + rule['rule'])
    return True


