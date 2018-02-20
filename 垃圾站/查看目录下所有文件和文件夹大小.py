# coding=utf-8
import os


def getdirsize(dir):
    size = 0
    for root, dirs, files in os.walk(dir):
        try:
            size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
        except Exception as e:
            pass
    return size/1024/1024


def get_sorted_size(root):
    dict = {}
    list = []
    for r in os.listdir(root):
        abs_p = os.path.join(root,r)
        if os.path.isdir(abs_p):
            s = getdirsize(abs_p)
        else:
            s = os.path.getsize(abs_p)/1024/1024
        list.append(s)
        dict[s] = r
        print("{} complete!".format(r))
    list.sort(reverse=True)
    root_size = sum(list)
    return dict, list, root_size


if __name__ == '__main__':
    root = r"C:\Windows"
    root = r"H:\\"
    dict, list, root_size = get_sorted_size(root)
    print("Total：{:.2f}G".format(root_size / 1024))
    print("-" * 50)
    for i in list:
        if i <= 1024:
            print("{}：{:.2f}M".format(dict[i],i))
        else:
            print("{}：{:.2f}G".format(dict[i], i/1024))


