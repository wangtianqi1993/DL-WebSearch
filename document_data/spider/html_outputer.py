# !/usr/bin/env python
# -*-coding: utf-8 -*-


class HtmlOutputer(object):
    def __init__(self):
        self.datas = []

    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    # ascii
    def output_html(self):
        fout = open('output.txt', 'w')

        for data in self.datas:

            # write the question
            # fout.write(data['url'])
            # fout.write('\n')
            fout.write(data['title'].encode('utf-8'))
            fout.write('\n')
            for item in data["summary"]:
                fout.write(item.encode('utf-8'))
                fout.write('\n')
            fout.write('\n')
        fout.close()
