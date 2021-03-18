# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 15:02:38 2021

@author: metalcorebear
"""

import xmltodict
import requests
import time
import json
import os

# Directory is where the json files live.
directory = ''

# Gets json files from directory
def get_files(directory):
    output = []
    for r, d, f in os.walk(directory):
        for file in f:
            if file.endswith(".json"):
                output.append(os.path.join(r, file))
    return output


def open_json(file):
    with open(file, 'r') as json_file:
        output = json.load(json_file)
    entry = output['feed']['entry']
    return entry


def concat_jsons(directory):
    json_files = get_files(directory)
    output = []
    for filepath in json_files:
        try:
            entry = open_json(filepath)
            output.extend(entry)
        except:
            continue
    json_index = list(range(len(output)))
    output_json = dict(zip(json_index,output))
    return output_json


if __name__ == '__main__':
    print('Building JSON...')
    output = concat_jsons(directory)
    print('Saving JSON...')
    if not os.path.isdir('Combined_JSONs'):
        os.mkdir('Combined_JSONs')
    file_name = os.path.join('Combined_JSONs','All_Items.json')
    with open(file_name, 'w') as json_file:
        json.dump(output, json_file)
    print('You are a great American!!')