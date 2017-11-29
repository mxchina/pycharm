# coding=utf-8
import requests
from bs4 import BeautifulSoup
import re
url = "http://www.quanshuwang.com/list/1_1.html"


def error_log(save_at,save_str):
    with open(save_at,'a') as f:
        f.write(save_str)

class My_spider():
    #所有小说
    # def __init__(self,url):
    #     self.url = url

    def get_html(self,url):
        res = requests.get(url)
        try:
            res_html = res.text.encode('iso-8859-1').decode('gbk')
        except Exception as e:
            res_html = res.text
            print("URL：%s Not encode('iso-8859-1').decode('gbk'),Only res.text!" % url)
            error_log(save_str="URL：%s Not encode('iso-8859-1').decode('gbk'),Only res.text!" % url,save_at="spider_error_log.txt")
        return res_html

    def get_obj_soul(self,url):
        res_html = self.get_html(url)
        soul = BeautifulSoup(res_html, 'lxml')
        return soul

    def get_onepage_url(self,url):
        soul = self.get_obj_soul(url)
        soul = soul.find_all('a',class_ = 'readTo')
        url_list = []
        for i in soul:
            i = i['href']
            url_list.append(i)
        return url_list

# n = 1
# url = "http://www.quanshuwang.com/list/1_%s.html"%str(n)
# classify = My_spider()
# for n1 in range(1,11):
#     url = "http://www.quanshuwang.com/list/1_%s.html" % str(n1)
#     classify.get_onepage_url(url)


class Novel(My_spider):
    #单本小说详情
    # def __init__(self,url):
    #     self.url = url

    def get_novel_detail(self,url):
        try:
            soul = self.get_obj_soul(url)
            if not soul==[]:
                try:
                    contents_url = soul.find_all(class_='reader')[0]['href']
                except Exception as e:
                    print("!"*50)
                    print(e)
                    error_log(save_at="spider_error_log.txt",save_str="contents_url = %s--->soul.find_all(class_='reader')[0]['href']-->IndexError: list index out of range"%contents_url)
                #小说名name，简介brief，封面img，作者author，字数count？，小说状态（完结or连载中）status
                name = soul.h1.string
                brief = soul.find(id='waa')
                s= str(brief)
                reg = r'介绍:([\s\S]*)</div>'
                si= re.findall(reg,s)[0]
                si ="".join(si.split())
                brief = si
                img = soul.find(class_='l mr11').img['src']
                author = soul.find(class_='bookso').dd.a.string
                status = soul.dl.dd.string
                return name, brief, img, author, status, contents_url
        except Exception as e:
            print("get_novel_detail eroor,url=%s"%url)
            print(e)
            error_log(save_at="spider_error_log.txt",save_str="get_novel_detail eroor,url=%s\n"%url+str(e))

# novel_detai_url = "http://www.quanshuwang.com/book_140440.html"
# novel = Novel(novel_detai_url)
# print(novel.contents_url)
# print(novel.name)
# print(novel.brief)
# print(novel.img)
# print(novel.author)
# print(novel.status)


class Novel_contents(My_spider):
    #单本小说的内容：章节名，章节内容
    # def __init__(self,url):
    #     self.url = url
        # 章节名chapterName，章节对应内容的url-chapterUrl, 章节对应内容的文章详情
    def get_chapterUrlAndchapterName_list(self,url,novel_id):
        res_html = self.get_html(url)
        reg = r'<li><a href="(.*?)" title=".*?">(.*?)</a></li>'
        reg = re.compile(reg)
        url_name_list = reg.findall(res_html)
        # name_list = []
        # url_list = []
        # content_list = []
        dict_chapter = {}
        reg_content = 'style5\(\);</script>(.*?)<script type="text/javascript">style6'
        reg_content = re.compile(reg_content, re.S)
        num = 1
        for i in url_name_list:
            if i[0].startswith("http"):
                real_url = i[0]
            else:
                real_url = url+'/'+i[0]
            res = requests.get(real_url)
            try:
                content_html = res.text.encode('iso-8859-1').decode('gbk')
            except Exception as e:
                print(e)
                error_log(save_str=str(e),save_at='chapterEncodeGbk_error_log')
            content = reg_content.findall(content_html)
            # content_list.append(content)
            # print(content)
            # url_list.append(real_url)
            # name_list.append(i[1])
            if not content == []:
                dict_chapter[i[1]] = content[0]
                print("Novel_id：%d-----Complite Add Chapter:%d In Dict_chapter" % (novel_id, num))
            else:
                dict_chapter[i[1]] = "爬取失败，章节内容为空"
                print("URL：%s 爬取失败,章节内容为空----------------------->"%real_url)
                error_log(save_at="spider_error_log.txt",save_str="URL：%s 爬取失败,章节内容为空---------------->\n"%real_url)
            num += 1
            if num>1000:
                print("Chapter more than 1500,Novel_id Is：%d" % novel_id)
                error_log(save_at="chapter_morethan1500_log.txt", save_str="Chapter more than 1500,Novel_id Is：%d\n" % novel_id )
                break
        print("Complite All Chapter,Novel_id Is:%d"%novel_id)
        return dict_chapter



# url = "http://www.quanshuwang.com/book/140/140219"
# novel_contents = Novel_contents()
# dict_chapter = novel_contents.get_chapterUrlAndchapterName_list(url,666)
# print(dict_chapter)
dict_classify = {
    1:"玄幻魔法",
    2:"武侠修真",
    3:"纯爱耽美",
    4:"都市言情",
    5:"职场校园",
    6:"穿越重生",
    7:"历史军事",
    8:"网游动漫",
    9:"恐怖灵异",
    10:"科幻小说",
    11:"美文名著",
}


# if __name__=='__main__':
#     classify = Novel()
#     for tag in range(1,2):
#         for page in range(1,11):
#             url = "http://www.quanshuwang.com/list/%s_%s.html"%(tag,page)
#             url_list = classify.get_onepage_url(url)
#             for novle_url in url_list:
#                 name, brief, img, author, status, contents_url = classify.get_novel_detail(novle_url)
#                 novle_detail = Novel_detail(name=name,breif = brief,img = img,author = author,status = status,tag = dict_classify[tag],into_url = contents_url)
#                 db.session.add(novle_detail)
#                 db.session.commit()

