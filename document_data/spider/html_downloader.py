# !/usr/bin/env python
# -*-coding: utf-8 -*-

import urllib2
import httplib

httplib.HTTPConnection._http_vsn = 10
httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'

class HtmlDownloader:
    def download(self, url):
        if url is None:
            return None
        response = urllib2.urlopen(url)
        if response.getcode() != 200:
            return None
        return response.read()
