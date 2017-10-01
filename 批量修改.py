import os
import sys
import getopt


def traversal(path=os.getcwd(), *, isDir=False, isFile=True, isChild=False):
    result_list = set()
    if not isChild:
        for each in os.listdir(path):
            each = os.path.join(path, each)
            if os.path.isfile(each) and isFile:
                result_list.add(each)
            if os.path.isdir(each) and isDir:
                result_list.add(each)
    else:  # 允许遍历子目录
        for root, dictionary, file in os.walk(path):
            if isFile:
                for each in file:
                    each = os.path.join(path, each)
                    result_list.add(each)
            if isDir:
                for each in dictionary:
                    each = os.path.join(path, each)
                    result_list.add(each)
    return result_list


def change(filepath: str, old: str, new: str):
    path, oldname = os.path.split(filepath)
    newname = oldname.replace(old, new)
    os.replace(filepath, os.path.join(path, newname))


if __name__ == "__main__":
    try:
        opts, _ = getopt.getopt(sys.argv[1:], "hFDC", ["help", "path="])
    except getopt.GetoptError:  # TODO
        print("懒得写参数提示嘿嘿嘿")
    # 初始化参数
    path = os.getcwd()
    isDir, isFile, isChild = False, False, False
    # 判断并修改参数
    for key, value in opts:
        if key == "-D":
            isDir = True
        elif key == "-F":
            isFile = True
        elif key == "-C":
            isChild = True
        elif key == "--path":
            path = value
    # 修改名称
    for each in traversal(path, isDir=isDir, isFile=isFile, isChild=isChild):
        try:
            change(each, _[0], _[1])
        except:
            change(each, _[0], "")
