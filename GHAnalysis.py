import json
import os
import argparse #参数解析模块

class Data:
    def __init__(self, dict_address: int = None, reload: int = 0):
        if reload == 1:
            self.__init(dict_address)
        if dict_address is None and not os.path.exists('1.json') and not os.path.exists('2.json') and not os.path.exists('3.json'): #判断括号里的文件是否存在的意思，括号内的可以是文件路径
            raise RuntimeError('error: init failed')
        x = open('1.json', 'r', encoding='utf-8').read() #open(路径+文件名, 读写模式, 编码) ‘r’为只读模式
        self.__4Events4PerP = json.loads(x)              #用户事件数量
        x = open('2.json', 'r', encoding='utf-8').read() 
        self.__4Events4PerR = json.loads(x)              #项目事件数量
        x = open('3.json', 'r', encoding='utf-8').read()
        self.__4Events4PerPPerR = json.loads(x)          #用户项目事件数量

    def __init(self, dict_address: str):
        json_list = []
        for root, dic, files in os.walk(dict_address):                     #遍历获取文件，遍历文件夹、根目录、目录文件夹、目录里的文件
            for f in files:
                if f[-5:] == '.json':
                    json_path = f                                          #记录下后缀名为json的地址
                    x = open(dict_address+'\\'+json_path,
                             'r', encoding='utf-8').read()                 #打开.json文件，‘r’为只读，readline返回其中一行元素
                    str_list = [_x for _x in x.split('\n') if len(_x) > 0] #split（）对字符串进行分割
                    for i, _str in enumerate(str_list):                    #enumerate函数将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标
                        try:
                            json_list.append(json.loads(_str))             #append() 方法用于在列表末尾添加新的对象，将文件数据由json格式转化为python字典。
                        except:
                            pass
        records = self.__listOfNestedDict2ListOfDict(json_list)
        self.__4Events4PerP = {}
        self.__4Events4PerR = {}
        self.__4Events4PerPPerR = {}
        for i in records:
            if not self.__4Events4PerP.get(i['actor__login'], 0):         #Python 字典 get() 函数返回指定键的值，如果键不在字典中返回默认值，所以0为默认值，用来判断是否有'actor__login'。
                self.__4Events4PerP.update({i['actor__login']: {}})       #update() 方法用于更新字典中的键/值对，可以修改存在的键对应的值，也可以添加新的键/值对到字典中。没有'actor__login'则添加。
                self.__4Events4PerPPerR.update({i['actor__login']: {}})
            self.__4Events4PerP[i['actor__login']][i['type']
                                         ] = self.__4Events4PerP[i['actor__login']].get(i['type'], 0)+1    # 获取到相应type的值+1，type没有为0
            if not self.__4Events4PerR.get(i['repo__name'], 0):
                self.__4Events4PerR.update({i['repo__name']: {}})
            self.__4Events4PerR[i['repo__name']][i['type']
                                       ] = self.__4Events4PerR[i['repo__name']].get(i['type'], 0)+1
            if not self.__4Events4PerPPerR[i['actor__login']].get(i['repo__name'], 0):
                self.__4Events4PerPPerR[i['actor__login']].update({i['repo__name']: {}})
            self.__4Events4PerPPerR[i['actor__login']][i['repo__name']][i['type']
                                                          ] = self.__4Events4PerPPerR[i['actor__login']][i['repo__name']].get(i['type'], 0)+1
        with open('1.json', 'w', encoding='utf-8') as f:   
            json.dump(self.__4Events4PerP,f)               #将序列化的str保存到文件中，存入个人事件。
        with open('2.json', 'w', encoding='utf-8') as f:
            json.dump(self.__4Events4PerR,f)               #存入项目事件。
        with open('3.json', 'w', encoding='utf-8') as f:   
            json.dump(self.__4Events4PerPPerR,f)           #存入每人每项目事件。

    def __parseDict(self, d: dict, prefix: str):
        _d = {}
        for k in d.keys():     #keys() 方法以列表形式返回字典中的所有的键。
            if str(type(d[k]))[-6:-2] == 'dict':
                _d.update(self.__parseDict(d[k], k))
            else:
                _k = f'{prefix}__{k}' if prefix != '' else k
                _d[_k] = d[k]
        return _d

    def __listOfNestedDict2ListOfDict(self, a: list):
        records = []
        for d in a:
            _d = self.__parseDict(d, '')
            records.append(_d)     # 字典放入列表，列表存所有项目
        return records

    def getEventsUsers(self, username: str, event: str) -> int:
        if not self.__4Events4PerP.get(username,0):
            return 0
        else:
            return self.__4Events4PerP[username].get(event,0)

    def getEventsRepos(self, reponame: str, event: str) -> int:
        if not self.__4Events4PerR.get(reponame,0):
            return 0
        else:
            return self.__4Events4PerR[reponame].get(event,0)

    def getEventsUsersAndRepos(self, username: str, reponame: str, event: str) -> int:
        if not self.__4Events4PerP.get(username,0):
            return 0
        elif not self.__4Events4PerPPerR[username].get(reponame,0):
            return 0
        else:
            return self.__4Events4PerPPerR[username][reponame].get(event,0)


class Run:
    def __init__(self):
        self.parser = argparse.ArgumentParser()         #创建一个 ArgumentParser 对象
        self.data = None
        self.argInit()
        print(self.analyse())

    def argInit(self):
        self.parser.add_argument('-i', '--init')        #添加参数
        self.parser.add_argument('-u', '--user')        
        self.parser.add_argument('-r', '--repo')
        self.parser.add_argument('-e', '--event')

    def analyse(self):
        if self.parser.parse_args().init:               #解析参数
            self.data = Data(self.parser.parse_args().init, 1)
            return 0
        else:
            if self.data is None:
                self.data = Data()
            if self.parser.parse_args().event:
                if self.parser.parse_args().user:      
                    if self.parser.parse_args().repo:
                        res = self.data.getEventsUsersAndRepos(
                            self.parser.parse_args().user, self.parser.parse_args().repo, self.parser.parse_args().event)  # 查询某用户在某项目某事件
                    else:
                        res = self.data.getEventsUsers(
                            self.parser.parse_args().user, self.parser.parse_args().event)                                 #查询某用户某事件
                elif self.parser.parse_args().repo:
                    res = self.data.getEventsRepos(
                        self.parser.parse_args().reop, self.parser.parse_args().event)                                     # 查询某项目某事件
                else:
                    raise RuntimeError('error: argument -l or -c are required')
            else:
                raise RuntimeError('error: argument -e is required')
        return res


if __name__ == '__main__':
    a = Run()