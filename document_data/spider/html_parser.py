# !/usr/bin/env python
# -*-coding: utf-8 -*-

from bs4 import BeautifulSoup
import urlparse
import re


class HtmlParser:
    """
    use to get new url and data from web page
    """
    def parse(self, page_url, html_cont):

        if page_url is None or html_cont is None:
            return
        # print html_cont
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')

        # print type(soup)
        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data

    def _get_new_urls(self, page_url, soup):
        new_urls = set()
        # 只搜索有答案的问题的超链接
        link = soup.find('div', class_="wgt-topic mod-shadow")
        if link:

            links = link.find_all('a', href=re.compile(r"/question/\d+"))
        # print links
            for item in links:
                new_url = item['href']
                new_full_url = urlparse.urljoin(page_url, new_url)
                new_urls.add(new_full_url)
        return new_urls

    def _get_new_data(self, page_url, soup):
        res_data = {}
        res_data["summary"] = []
        # url
        res_data['url'] = page_url
        # <dd class="lemmaWgt-lemmaTitle-title"><h1>Python</h1>

        # title_node = soup.find('dd', class_='lemmaWgt-lemmaTitle-title').find('h1')
        title_node = soup.find('title')
        res_data['title'] = title_node.get_text()

        # get best answer about the question
        cont_node = soup.find("pre", class_="best-text mb-10")
        if cont_node:
            res_data['summary'].append(cont_node.get_text())
        cont_node = soup.find("pre", class_='recommend-text mb-10')
        if cont_node:
            res_data['summary'].append(cont_node.get_text())

        # get another answer about the question
        cont_node = soup.find_all('div', class_="line ")
        for item in cont_node:
            cont_node_all = item.find('span', class_='con-all')
            if cont_node_all:
                 res_data['summary'].append(cont_node_all.get_text())
            else:
                cont_node_a = item.find("span", class_='con')
                if cont_node_a:
                    res_data['summary'].append(cont_node_a.get_text())

        cont_node = soup.find_all('div', class_="line content")
        for item in cont_node:
            cont_node_all = item.find('span', class_='con-all')
            if cont_node_all:
                 res_data['summary'].append(cont_node_all.get_text())
            else:
                cont_node_a = item.find("span", class_='con')
                if cont_node_a:
                    res_data['summary'].append(cont_node_a.get_text())

        # cont_node = soup.find_all('span', class_='con')
        # if cont_node:
        #     for item in cont_node:
        #         res_data['summary'].append(item.get_text())

        return res_data

