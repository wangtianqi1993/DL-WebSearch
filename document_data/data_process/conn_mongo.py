# !/usr/bin/env python
# -*-coding: utf-8 -*-
__author__ = 'wtq'

from pymongo import MongoClient
from document_data.config import MONGODB_HOST, MONGODB_PORT


def conn_mongo(host=MONGODB_HOST, port=MONGODB_PORT):
    """

    :param host:
    :param port:
    :return:
    """
    client = MongoClient(host, port)
    return client
