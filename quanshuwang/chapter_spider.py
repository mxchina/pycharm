# coding=utf-8
from spider import Novel_contents
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from detail import Novel_detail_2, Novel_content_2, error_log
import threading

"""
chapter_id, chapter_name, chapter_content, novle_id
"""
def download_novel(url_and_id):
    global session
    obj_novel_list = []
    url = url_and_id[0]
    novel_id = url_and_id[1]
    dict_chapter = novel_contents.get_chapterUrlAndchapterName_list(url=url, novel_id=novel_id)
    for chapter_name, chapter_content in dict_chapter.items():
        obj_novel = Novel_content_2(chapter_name=chapter_name, chapter_content=chapter_content, novel_id=novel_id)
        obj_novel_list.append(obj_novel)
    if tLock.acquire():
        try:
            #session.add_all(obj_novel_list)
            for obj_novel_ in obj_novel_list:          #防止重复的insert方法
                session.merge(obj_novel_)
            session.commit()
            print("Successful Session Commit Novel_id is %d!" % novel_id)
            error_log(save_at="chapter_Commit_Successful_log",save_str="Successful Session Commit Novel_id is %d!" % novel_id)
            tLock.release()
        except Exception as e:
            tLock.release()
            print("---->Field Session Commit Novel_id is %d!\n" % novel_id+str(e))
            error_log(save_str="---->Field Session Commit Novel_id is %d!\n" % novel_id+str(e),save_at="chapter_error_log.txt")

engine = create_engine("mysql+pymysql://root:Mx560205@rm-uf692a5q3iml778tdo.mysql.rds.aliyuncs.com:3306/novel?charset=utf8")
DBSession = sessionmaker(bind=engine)
session = DBSession()

if __name__=="__main__":
    novel_contents = Novel_contents()
    for index in range(1000,1101,100):  #tag1 一共28990本小说
          # 初始化提交mysql的对象列表，每次index开始更新为空
        query = session.query(Novel_detail_2.into_url, Novel_detail_2.novel_id)[index:index+100]  # 要爬取的小说[:9]表示数据库Novel_detail表中1-9的小说
        thread_list = []
        tLock = threading.Lock()
        for url_and_id in query:
            th = threading.Thread(target=download_novel,args=(url_and_id,))
            thread_list.append(th)
        for th in thread_list:
            th.start()
        for th in thread_list:
            th.join()





