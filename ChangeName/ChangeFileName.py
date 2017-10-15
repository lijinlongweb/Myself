import os
import sys
import getopt
import re


class ChangeName():
    def __init__(self):
        self.HELPMESSAGE = '''参数列表:
        -h --help  获取帮助信息
           --path= 设置程序运行的根目录，默认为程序所在目录
        -F         修改根目录下文件名
        -D         修改根目录下文件夹名
        -C         遍历根目录下子目录
        -S         修改后缀名
           --oldn= 使用正则表达式构造的 旧有名称
           --newn= 实现re.sub(oldn,newn,text)的第二个参数
           --clear 清除名称中的空格，会使所有名称参数失效
        '''
        self.path, self.oldn, self.newn = os.getcwd(), str, str
        self.isDir, self.isFile, self.isChild, self.isSuffix = False, False, False, False
        self.isOld, self.isNew, self.isClear = False, False, False
        self.list = set()

    def _setList(self):
        if not self.isChild:
            for each in os.listdir(self.path):
                each = os.path.join(self.path, each)
                if os.path.isfile(each) and self.isFile:
                    self.list.add(each)
                if os.path.isdir(each) and self.isDir:
                    self.list.add(each)
        else:
            for root, dictionary, file in os.walk(self.path):
                if self.isFile:
                    for each in file:
                        each = os.path.join(self.path, each)
                        self.list.add(each)
                if self.isDir:
                    for each in dictionary:
                        each = os.path.join(self.path, each)
                        self.list.add(each)

    def _change(self, filepath:str, old:str, new:str):
        path, oldname = os.path.split(filepath)
        oldname, suffix = oldname.split(".")
        if self.isOld:
            newname = re.sub(r'%s'%(old), r'%s'%(new), oldname)
        elif self.isSuffix:
            newname = oldname
            suffix = suffix.replace(old, new)
        else:
            newname = oldname.replace(old, new)
        os.rename(filepath, os.path.join(path, "{0}.{1}".format(newname, suffix)))
    
    def run(self):
        if self.isNew^self.isOld == True:
            sys.exit("不能单独使用--oldn 或--newn ")
        if self.isClear:
            self.oldn = " "
            self.newn = ""
        self._setList()
        for each in self.list:
            self._change(each, self.oldn, self.newn)
        
    

if __name__ == "__main__":
    try:
        opts, _ = getopt.getopt(sys.argv[1:], "hFDCS", ["help", "path=", "oldn=", "newn=", "clear"])
    except getopt.GetoptError:
        sys.exit("您输入了一个错误的参数，请使用-h或--help来获取参数列表")
    Main = ChangeName()
    try:
        Main.oldn = _[0]
        Main.newn = _[1]
    except IndexError:
        try:
            Main.oldn = _[0]
            Main.newn = ""
        except IndexError:
            pass
    for key, value in opts:
        if key == "-D":
            Main.isDir = True
        elif key == "-F":
            Main.isFile = True
        elif key == "-C":
            Main.isChild = True
        elif key == "-S":
            Main.isSuffix = True
        elif key == "--path":
            Main.path = value
        elif key == "--oldn":
            Main.isOld = True
            Main.oldn = value
        elif key == "--newn":
            Main.isNew = True
            Main.newn = value
        elif key == "--clear":
            Main.isClear = True
        elif key == "--help" or key == "-h":
            sys.exit(Main.HELPMESSAGE)
    Main.run()
