# !/usr/bin/env python
# -*-coding: utf-8-*-
__author__ = 'wtq'
import jieba
import string
import re
from document_data.data_process.conn_mongo import conn_mongo

client = conn_mongo()


def is_chinese(uchar):

        """判断一个unicode是否是汉字,过滤掉除汉字外的其他字符"""

        if uchar >= u'\u4e00' and uchar<=u'\u9fa5':

                return True
        else:
                return False


def split_document():
    """

    :return:
    """
    db = client.webSearch
    vocab_set = list()
    document_list = ['data1_education.txt', 'data2_shopping_online.txt', 'data3_basketball.txt', 'data4_ware.txt', 'data5_life.txt'
                     'data6_economic.txt', 'data7_law.txt', 'data8_culture.txt', 'data9_science.txt', 'data10_entertainment.txt']
    with open('/home/wtq/develop/workspace/github/DL-WebSearch/document_data/train_data/data1_education.txt', 'r') as files:
        words = files.read()
        for item in words:
            if item not in vocab_set:
                vocab_set.append(item)
    print len(vocab_set)
    mongo_item = {
        "vocabulary_list": str(vocab_set)
    }
    db.voc_list.insert(mongo_item)

    # for i in seg_list1:
    #     if i not in vocab_set:
    #         vocab_set.append(i)
    # for i in vocab_set:
    #     print i
    # vector = [0]*len(vocab_set)
    # for i in seg_list2:
    #     if i in vocab_set:
    #         vector[vocab_set.index(i)] = 1
    # print vector


def get_voc_list():
    """

    :return:
    """
    db = client.webSearch
    voc_list = db.voc_list.find()
    for item in voc_list[0]['vocabulary_list']:
        print item


if __name__ == "__main__":
    # split_document()
    get_voc_list()
