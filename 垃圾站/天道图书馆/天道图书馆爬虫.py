# coding=utf-8
import requests
from lxml import etree
import re

url = "http://www.biqukan.com/17_17957/"
res = requests.get(url)
# print(res.text)
html = etree.HTML(res.text)
datas = html.xpath('//dd/a')
n = 1
with open("天道图书馆.txt",'a') as f:
    for data in datas[12:]:
        chapter_url = data.xpath('@href')
        chapter_url = "http://www.biqukan.com/"+"".join(chapter_url)
        content = requests.get(chapter_url)
        reg = r'<h1>(.*?)</h1>.*<div id="content" class="showtxt">(.*?)http://www.biqukan.com'
        list = re.findall(reg,content.text,re.S)
        content_ = list[0][0]+"\n"+list[0][1]+"\n"
        content_ = re.sub(r'[<br /><br />]*[&nbsp;]+','\n\n        ',content_)
        content_ = re.sub(r'\n\s*天才壹秒記住.*?為您提供精彩小說閱讀。','',content_)
        content_ = re.sub(r'\n*\s*手机用户请浏览阅读，更优质的阅读体验.*?>','',content_,flags=re.S)
        content_ = re.sub(r'r />\s*','',content_)
        content_ = content_.lstrip()
        f.write(content_)
        print(n)
        n += 1
