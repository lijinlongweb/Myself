# Myself
一些我自己给自己写的小脚本

### Backup
自动备份某个目录下全部文件的小脚本，本手残两次删掉写好的Django项目之后写的。

### getMeizitu
爬虫初试，留作纪念

### getTranscripts
爬取我校教务系统，并且发送邮件通知

### ChangeFileName
修改某个目录下的被匹配上的文件名称
四个参数：-F 修改文件名 -D 修改目录名 -C 允许查找目录下子目录内容 --path= 设定路径，默认为当前的脚本路径
* 样例：
```python
python ChangeFileName.py -F test newTest
```

### ChangeName
ChangeFileName的增强版，允许批量修改后缀名，或使用正则表达式修改文件名。exe文件是64位

兼容原有使用方法。使用正则表达式需要参数--oldn和--newn
* 样例:
```python
python ChangeFileName.py -F --oldn=Test_(\d+) --newn=TestResult_\1
```
