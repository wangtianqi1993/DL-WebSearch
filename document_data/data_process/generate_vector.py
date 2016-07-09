# !/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'wtq'

import sys
import jieba
import numpy as np
from document_data.data_process.conn_mongo import conn_mongo

reload(sys)
sys.setdefaultencoding("utf-8")
client = conn_mongo()

document_list = ['data1_education.txt', 'data2_shopping_online.txt', 'data3_basketball.txt', 'data4_ware.txt',
                 'data5_life.txt',
                 'data6_economic.txt', 'data7_law.txt', 'data8_culture.txt', 'data9_science.txt',
                 'data10_entertainment.txt']


def is_chinese(uchar):
    """
    判断一个unicode是否是汉字,过滤掉除汉字外的其他字符
    """

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
    vocab_list = list()
    vocab_dict = dict()

    try:

        for item1 in document_list:
            with open('/home/wtq/develop/workspace/github/DL-WebSearch/document_data/train_data/' + item1,
                      'r') as files:
                words = files.read()
                # using jieba to cut words
                words = jieba.cut(words)
                for item2 in words:
                    if is_chinese(item2):
                        if item2 not in vocab_dict:
                            vocab_dict[item2] = 0
                        vocab_dict[item2] += 1

        # 取中vocab_dict出现次数最多的前10000个词作为词表
        for value in sorted(vocab_dict.values(), reverse=True):
            print value
            for key in vocab_dict:
                if vocab_dict[key] == value:
                    vocab_list.append(key)
            if len(vocab_list) > 1000:
                break

        # write vocab_list to mongoDB
        mongo_item = {
            "vocabulary_list": vocab_list
        }
        db.voc_list.insert(mongo_item)

    except Exception, e:
        print 'error', e


def generate_vector(object_words, words_list):
    """
    convert each object_words to feature vector using words_list
    it is the set of words model
    :return:
    """
    feature_vector = [0] * len(words_list)
    for word in object_words:
        if word in words_list:
            feature_vector[words_list.index(word)] += 1
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
    question = []
    answer = []

    try:
        for item1 in document_list:
            with open('/home/wtq/develop/workspace/github/DL-WebSearch/document_data/train_data/' + item1,
                      'r') as files:

                lines = files.readlines()
                for line in lines:
                    line = list(jieba.cut(line))
                    temp = []

                    # 去掉非汉字
                    for item in line:
                        if is_chinese(item):
                            temp.append(item)

                    if len(temp) >= 2:
                        # check if the line is a query
                        if temp[-2] == question_sign[0] and temp[-1] == question_sign[1]:
                            question = generate_vector(temp, voc_list)

                        # else is a answer
                        else:
                            answer = generate_vector(temp, voc_list)
                            # write the query answer pair to mongo
                            mongo_item = {
                                "query": question,
                                "answer": answer
                            }
                            db.query_answer_vector.insert(mongo_item)

    except Exception, e:
        print 'error', e


# get the element index in list
def indices(lst, element):
    result = []
    offset = -1
    while True:
        try:
            offset = lst.index(element, offset+1)
        except ValueError:
            return result
        result.append(offset)


def gen_query_docu_score():
    """
    产生每个query对应的在文档集合中相关分数,such as [0.5, 0.5, 0 , 0 ,......0]
    :return:
    """

    db = client.webSearch
    querys = []
    # 将样本中的问题存储到querys[]中
    for item in db.query_answer_vector.find():
        if item['query'] not in querys:
            querys.append(item['query'])

    documents = []
    for item in db.query_answer_vector.find():
        documents.append(item['query'])

    for item1 in querys:
        # 得到该query对应的所有document在整个集合中的位置
        similar_score = [0]*len(documents)
        indexes = indices(documents, item1)

        # 将该查询（item1）对应的答案位置标为1／sum
        for i in indexes:
            similar_score[i] = 1.0/len(indexes)
            print i
        print 'one'
        mongo_item = {
            "query": item1,
            "similar_score": similar_score
        }
        db.query_doc_similar.insert(mongo_item)


if __name__ == "__main__":
    # get_voc_list()
    # generate_vocabulary_list()
    # create_query_doc_vector()
    gen_query_docu_score()

    # db = client.webSearch
    # a = db.voc_list.find()
    # print len(a[0]['vocabulary_list'])
