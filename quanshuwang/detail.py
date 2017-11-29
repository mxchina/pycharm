# coding=utf-8
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from spider import Novel, dict_classify,error_log
import threading

# dict_classify = {
#     1:"玄幻魔法",
#     2:"武侠修真",
#     3:"纯爱耽美",
#     4:"都市言情",
#     5:"职场校园",
#     6:"穿越重生",
#     7:"历史军事",
#     8:"网游动漫",
#     9:"恐怖灵异",
#     10:"科幻小说",
#     11:"美文名著",
# }
# 1:1   2,3,5,6,8,9 : 2  4:4  7:7  10,11 : 10 数据库保存map关系，比如2,3,5,6,8,9 对应2号表

engine = create_engine("mysql+pymysql://root:Mx560205@rm-uf692a5q3iml778tdo.mysql.rds.aliyuncs.com:3306/novel?charset=utf8")
# max_overflow=5

Base = declarative_base()

class Novel_detail_2(Base):
    """
    id,小说名name，简介brief，封面img，作者author，字数count？，小说状态（完结or连载中）status,小说分类tag
    """
    __tablename__ = 'novel_detail_2'
    novel_id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(50))
    breif = Column(String(500))
    img = Column(String(100))
    author = Column(String(100))
    count = Column(Integer)
    status = Column(String(10))
    tag = Column(String(20))
    into_url = Column(String(100))

class Novel_content_2(Base):
    """
    id, 章节名，章节对应内容的url,章节对应内容的文章详情
    """
    __tablename__ = 'novel_content_2'
    chapter_id = Column(Integer,primary_key=True,autoincrement=True)
    chapter_name = Column(String(50))
    chapter_content = Column(Text)
    novel_id = Column(Integer,ForeignKey('novel_detail_2.novel_id'))

#错误处理，添加进日志


#获取一本小说的详情页数据
def get_novel_detail(tag,page):
    global session
    url = "http://www.quanshuwang.com/list/%s_%s.html" % (tag, page)
    try:
        url_list = classify.get_onepage_url(url)
    except Exception as e:
        error_str = "Tag:%s,Page:%s Field，Error Soul is: %s" % (tag,page,classify.get_obj_soul(url))
        print(error_str)
        error_log(save_str=error_str,save_at="detail_error_log.txt")

    for novle_url in url_list:
        if classify.get_novel_detail(novle_url):
            name, brief, img, author, status, contents_url = classify.get_novel_detail(novle_url)
            novle_detail = Novel_detail_2(name=name, breif=brief, img=img, author=author, status=status,
                                    tag=dict_classify[tag], into_url=contents_url)
            try:
                novel_detail_list.append(novle_detail)
                print("Page:%s,Novel_detail_list add name:%s is succesful!" % (page,name))
            except Exception as e:
                print("Page:%s,Field Novel_detail_list Add------------>%s"%(page,name))
                print(e)
        else:
            print("URL:%s ---> is 空列表[]!"%novle_url)
            error_log(save_at="detail_error_log.txt",save_str="URL:%s ---> is 空列表[]!"%novle_url)


if __name__=="__main__":
    Base.metadata.create_all(engine)  #创建表
    Base.metadata.drop_all(engine)   #删除表
    DBSession = sessionmaker(bind=engine)
    novel_list = []
    classify = Novel()
    for tag in range(11,12):
        for index in range(1,674,50):
            session = DBSession()
            thread_list = []
            novel_detail_list = []
            for page in range(index,index+50):
                th = threading.Thread(target=get_novel_detail,args=(tag,page))
                th.start()
                thread_list.append(th)
            for th in thread_list:
                th.join()
            try:
                print("MySQL Session Adding And Commiting，please wait......")
                session.add_all(novel_detail_list)
                # for novel_detail_ in novel_detail_list:          #防止重复的insert方法
                #     session.merge(novel_detail_)
                session.commit()
                print("MySQL Succesful Session Commit!----->Lenth is :"+str(len(novel_detail_list)))
            except Exception as e:
                print("MySQL Field Session Commit!----------------------->")
                print(e)
                error_log(save_str="MySQL Field Session Commit!----------------------->\n" + str(e),
                          save_at="detail_error_log.txt")




