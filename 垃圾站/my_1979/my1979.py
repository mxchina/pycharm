# coding:utf-8
import re


with open("我的1979.txt",encoding="UTF-8") as f:
    s = f.read()

res = re.sub(r'(?P<value>\d+)、',lambda matched: "第"+matched.group('value')+"章 ", s)
# print(res)

with open("我的1979-1.txt","w",encoding="UTF-8") as f:
    f.write(res)

