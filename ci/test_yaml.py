import pytest

import regex
from dateutil.parser import parse
import sys
import yaml
import json

with open('ci/yaml_rules.json') as json_data:
    requirements = json.load(json_data)
        

def test_yaml(md_files):
    for file in md_files:
        filestring = file.read()
        reg = regex.compile(r'^---(.*)---',flags=regex.DOTALL)
        match = regex.search(reg, filestring)
        assert match
        yaml_text = match.group(1)
        parsed_yaml = yaml.load(yaml_text)
        for requirement in requirements:
            req = requirements[requirement]
            if req['required']:
                assert requirement in parsed_yaml, 'YAML metadata missing required element: ' + requirement
            if req['type'] is 'link':
                regexp = regex.compile(r'\[(.*)\]\((.*)\)')
                assert regex.match(regexp,parsed_yaml[requirement]), 'YAML metadata formatting error: ' + requirement
            if req['type'] is 'date':
                try:
                    parse(str(parsed_yaml[requirement]))
                except ValueError:
                    assert False, 'YAML metadata formatting error: ' + requirement + ' date parse failed.'
