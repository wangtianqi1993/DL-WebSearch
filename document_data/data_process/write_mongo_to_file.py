# !/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from document_data.data_process.conn_mongo import conn_mongo

__author__ = 'wtq'

client = conn_mongo()
db = client.webSearch


def write_mongo_to_file():
    """

    :return:
    """
    all_document = []
    for item in db.query_answer_vector.find():
        all_document.append(item['answer'])

    json_doc = json.dumps(all_document)
    with open('/home/wtq/document', 'w') as f:
        f.write(json_doc)

    all_query_doc_score = []
    for item in db.query_doc_similar.find():
        temp_score = []
        temp_score.append(item['query'])
        temp_score.append(item['similar_score'])
        all_query_doc_score.append(temp_score)

    json_score = json.dumps(all_query_doc_score)
    with open('/home/wtq/query_doc_score', 'w') as f:
        f.write(json_score)


def read_file():
    """

    :return:
    """
    with open('/home/wtq/document', 'r') as f:
        a_json = f.read()
        a = json.loads(a_json)
        j = 0
        for i in a:
            j += 1
            print i[1:20]
            if j > 20:
                break

if __name__ == '__main__':
    write_mongo_to_file()
    # read_file()

