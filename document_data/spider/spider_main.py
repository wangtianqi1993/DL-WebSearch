# !/usr/bin/env python
# -*-coding: utf-8 -*-
import test
import url_manager, html_downloader, html_parser, html_outputer

test.sayHello('chm')


class SpiderMain:
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()

    def craw(self, root_url):
        count = 1
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                print 'craw %d: %s' % (count, new_url)
                html_cont = self.downloader.download(new_url)
                new_urls, new_data = self.parser.parse(new_url, html_cont)
                # get new url
                self.urls.add_new_urls(new_urls)
                # get answer and question
                self.outputer.collect_data(new_data)
                if count == 500:
                    break
                count = count + 1
            except IOError, e:
                print e
                print 'craw failed'
        # save the answer and question
        self.outputer.output_html()


print dir(__name__)
if __name__ == '__main__':
    root_url = "http://zhidao.baidu.com/link?url=I8P646857rI63gKIx2xt82_M2XgzrF0xl5CEpz5tDQYGCBhfgrLr2uE0tvtL6CS6bM-KNH5hnnKuSHPvnINdh5SH3smMUo5Opm4DPFYW_oi"
    spider = SpiderMain()
    spider.craw(root_url)
