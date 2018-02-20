# coding=utf-8
import requests
import re
import time
import yagmail
from lxml import etree


url = "http://www.80txt.com/txtml_66970.html"
res = requests.get(url)
res.encoding="utf-8"
# print(res.text)
html = etree.HTML(res.text)
lis = html.xpath('//li/a')
n = 1
with open('我的1979.txt','a') as f:
    for li in lis:
        chapter_url = "".join(li.xpath('@href'))
        # print(chapter_url)
        if chapter_url.startswith('http'):
            res = requests.get(chapter_url)
            if "charset=gbk" in res.text:
                res.encoding = "gbk"
            else:
                res.encoding = "utf-8"
            # html = etree.HTML(res.text)
            # content = html.xpath('//div[@class="book_content"]')[0].xpath('string(.)')
            reg = r'<h1>(.*?)</h1>.*<div class="book_content" id="content">(.*?)<div class="con_l">'
            contents = re.findall(reg,res.text,re.S)
            content = re.sub(r'<br /><br />\s*','\n\n        ',contents[0][1],flags=re.S)
            content = re.sub(r'<div.*?</div>','',content,flags=re.S)
            content = re.sub(r'<a.*?</a>', '', content, flags=re.S)
            content = re.sub(r'\[.*?\]', '', content, flags=re.S)
            content = re.sub(r'<strong.*?</strong>', '', content, flags=re.S)
            content = re.sub(r'求书网小说qiushu.cc', '', content, flags=re.S)
            content = re.sub(r'txt下载80txt.com', '', content, flags=re.S)
            content = contents[0][0].rstrip() + "\n\n        "+content.lstrip()+"\n"
            try:
                f.write(content)
            except Exception as e:
                pass
            print(n)
            n += 1


# time.sleep(5)
# yag = yagmail.SMTP(user='274819450@qq.com',password='tgrpmxztvvaebijg',host='smtp.qq.com')
# yag.send(to='274819450@qq.com',subject="天道图书馆1.txt", contents=['天道图书馆1.txt','F:\\github-test\\my-first-github\\垃圾站\\天道图书馆1.txt'])
