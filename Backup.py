import os, time, shutil
from multiprocessing import Process
#变量初始化
MonitorPath = r'D:\OSS'
BackupPath = os.getcwd()
Minute = 1
NowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def Copy(file, Cfile):
    if not os.path.exists(Cfile):
        os.makedirs(Cfile)
    log = shutil.copy(file, Cfile)
    print(NowTime, log)


def Monitor(Minute, MonitorPath):
    for root, dirs, files in os.walk(MonitorPath):
        for file in files:
            file = os.path.join(root, file)
            if time.time() - os.path.getmtime(file) < Minute * 60 + 10:
                Cfile = os.path.join(BackupPath,root.replace(os.path.dirname(MonitorPath), ""))
                Copy(file, Cfile)
    print(NowTime, "Done.")


def Run():
    if not os.path.exists(MonitorPath):
        return 0
    else:
        return 1


if __name__ == '__main__':
    while Run():
        p = Process(target=Monitor, args=(Minute, MonitorPath))
        p.start()
        time.sleep(Minute * 60)
    else:
        print("Path Error!")
