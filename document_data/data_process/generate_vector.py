# !/usr/bin/env python
# -*-coding: utf-8-*-

__author__ = 'wtq'

import re
import sys
import jieba
import string
from document_data.data_process.conn_mongo import conn_mongo

reload(sys)
sys.setdefaultencoding("utf-8")
client = conn_mongo()


def is_chinese(uchar):

        """判断一个unicode是否是汉字,过滤掉除汉字外的其他字符"""
        if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
                return True
        else:
                return False


def generate_vocabulary_list():
    """
    generate the while words then write to mongoDB
    :return:
    """
    db = client.webSearch
    vocab_set = list()

    document_list = ['data1_education.txt', 'data2_shopping_online.txt', 'data3_basketball.txt', 'data4_ware.txt', 'data5_life.txt',
                     'data6_economic.txt', 'data7_law.txt', 'data8_culture.txt', 'data9_science.txt', 'data10_entertainment.txt']

    for item1 in document_list:
        with open('/home/wtq/develop/workspace/github/DL-WebSearch/document_data/train_data/' + item1, 'r') as files:
            words = files.read()
            # using jieba to cut words in search engine model
            words = jieba.cut_for_search(words)
            for item2 in words:
                if is_chinese(item2):
                    if item2 not in vocab_set:
                        vocab_set.append(item2)
        print len(vocab_set)

    # write vocab_list to mongoDB
    mongo_item = {
        "vocabulary_list": vocab_set
    }
    db.voc_list.insert(mongo_item)


def generate_vector(object_words, words_list):
    """
    convert each object_words to feature vector using words_list
    it is the set of words model
    :return:
    """
    feature_vector = [0]*len(words_list)
    for word in object_words:
        if word in words_list:
            feature_vector[words_list.index(word)] = 1
    return feature_vector


def create_query_doc_vector():
    """
    using generate_vector function to create query vector and document vector
    :return:
    """
    db = client.webSearch
    voc_list = db.voc_list.find()
    voc_list = voc_list[0]['vocabulary_list']
    question_sign = ['百度', '知道']
    frist = 1
    item = []

    question = []
    answer = []

    document_list = ['data1_education.txt', 'data2_shopping_online.txt', 'data3_basketball.txt', 'data4_ware.txt', 'data5_life.txt',
                     'data6_economic.txt', 'data7_law.txt', 'data8_culture.txt', 'data9_science.txt', 'data10_entertainment.txt']
    for item1 in document_list:
        with open('/home/wtq/develop/workspace/github/DL-WebSearch/document_data/train_data/' + item1, 'r') as files:

                lines = files.readlines()
                for line in lines:
                    line = list(jieba.cut_for_search(line))
                    temp = []

                    # 去掉非汉字
                    for item in line:
                        if is_chinese(item):
                            temp.append(item)

                    if len(temp) >= 2:

                        # check if the line is a query
                        if temp[-2] == question_sign[0] and temp[-1] == question_sign[1]:

                            question = generate_vector(temp, voc_list)
                            # question = generate_vector(temp, voc_list)

                        # else is a answer
                        else:
                            answer = generate_vector(temp, voc_list)
                            # write the query answer pair to mongo
                            mongo_item = {
                                   "query": question,
                                   "answer": answer
                            }
                            db.query_answer_vector.insert(mongo_item)
                            # answer.append(generate_vector(temp, voc_list))


if __name__ == "__main__":
    # split_document()
    # get_voc_list()
    # generate_vocabulary_list()
    create_query_doc_vector()

    # db = client.webSearch
    # item = db.query_answer_vector.find()
    # for i in item[0]['answer']:
    #     print i
