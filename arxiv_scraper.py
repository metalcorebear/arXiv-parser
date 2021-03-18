# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 10:50:11 2021

@author: metalcorebear
"""

# Parser for arXiv

#pip install xmltodict
import xmltodict
import requests
import time
import json
import os


# Global parameters

# For possible categories, see arXiv API documentation.
category = 'cs.AI'

# data_start and data_range are pagination parameters.
data_start = 0
data_range = 100


# This will search for all articles of category.
def get_url_list(category, data_start, data_range):
    iterations = int((data_range-data_start)/10)
    query_range = [i+iterations for i in range(data_start, data_range, iterations)]
    query_range.insert(0,data_start)
    url_list = []
    for i in range(len(query_range)-1):
        url = 'http://export.arxiv.org/api/query?search_query=cat:' + category + '&start=' + str(query_range[i]) + '&max_results=10'
        url_list.append(url)
    return url_list


# This will get all the urls and save a list of XML documents
def get_xml(url_list):
    xml_list = []
    for url in url_list:
        try:
            data = requests.get(url)
            xml_list.append(data.text)
        except:
            continue
        print('Waiting for 30 seconds...')
        time.sleep(30)
    return xml_list


# This will convert xml to json
def get_json(xml_list):
    dict_list = []
    if not os.path.isdir('json_files'):
        os.mkdir('json_files')
    for item in xml_list:
        data_dict = xmltodict.parse(item)
        json_data = json.dumps(data_dict)
        dict_list.append(json_data)
    for i in range(len(dict_list)):
        filename = 'arXiv' + str(i) + '.json'
        file_path = os.path.join('json_files', filename)
        with open(file_path, 'w') as json_file:
            json_file.write(dict_list[i])
        json_file.close()
    return dict_list


if __name__ == '__main__':
    print('Building URL list...')
    url_list = get_url_list(category, data_start, data_range)
    print('Pinging API...')
    xml_list = get_xml(url_list)
    print('Saving json files...')
    _ = get_json(xml_list)
    print('You are a great American!!')
    