#!/usr/bin/env  python

"""
Module for grabbing the pages representing the index
 of Curtis's North American Indian
"""

import os
import re
import json
from collections import OrderedDict
import urlparse
import time
import requests

# Assumes script is in the nul-curtis-data directory
BASEPATH = os.path.dirname(os.path.realpath(__file__))
FILE_LIST = [os.path.join(BASEPATH, x) for x in os.listdir(BASEPATH)]


def grab_index(file_obj):
    """
    Filters out the URLs for pages representing the index
    from a json file representing a scanned book
    """

    data = json.loads(file_obj.read(), object_pairs_hook=OrderedDict)
    page_tuples = data['pages'].items()
    for index, page_info in enumerate(page_tuples):
        if re.search('Index', page_info[1]) is not None:
            start = index

    index_pages = [
        p[0] for p in page_tuples[start:]
        if re.search('http:\/\/memory\.loc\.gov', p[0]) is None]

    return index_pages

BOOK_INDEXES = {}
for f in FILE_LIST:
    with open(f, 'r') as infile:
        target_pages = grab_index(infile)
        data_key = os.path.splitext(os.path.basename(infile.name))[0]
        BOOK_INDEXES[data_key] = target_pages

for k in BOOK_INDEXES:
    for v in BOOK_INDEXES[k]:
        outfile = re.sub('\/', '-', urlparse.urlparse(v)[2])[1:]
        r = requests.get(v)
        if r.status_code == 200:
            with open(outfile, 'wb') as oF:
                oF.write(r.content)
        print("{0} saved. Sleeping for 1 second".format(outfile))
        time.sleep(1)
