# -*- coding: utf-8 -*-
#from fnmatch import translate
import json
import os
import sys
import uuid
import requests
import hashlib
import time
from imp import reload
import time
reload(sys)



def loadjson(json_name='config.json'):
    try:
        f = open(json_name, 'r')
    except FileNotFoundError:
        f = open(json_name, 'w')
        b = json.dumps({'APP_KEY':'','APP_SECRET':''},sort_keys=True, indent=4)
        f2 = open(json_name, 'w')
        f2.write(b)
        f2.close()
        f.close()
        f = open(json_name, 'r')
    content = f.read()
    a = json.loads(content)
    f.close()
    return a
a=loadjson(json_name='YOUDAOAPI.json')
YOUDAO_URL = 'https://openapi.youdao.com/api'
APP_KEY = a['APP_KEY']
APP_SECRET = a['APP_SECRET']


def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)


class YoudaoTranslate():
    def __init__(self):
        self.data = {}
        self.data['from'] = 'en'
        self.data['to'] = 'zh-CHS'
        self.data['signType'] = 'v3'
        
        
        self.data['appKey'] = APP_KEY
        self.data['vocabId'] = ""#您的用户词表ID
        
        
        '''
        调用youdao API
        type = 0：美音
        type = 1：英音

        判断当前目录下是否存在两个语音库的目录
        如果不存在，创建
        '''

        # 文件根目录
        #print(os.path.abspath(__file__))
        #a=os.path.abspath(__file__)
        
        #self._dirRoot = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        #self._dirSpeech = os.path.join(self._dirRoot, 'TranslateJson')  


        # 判断是否存在库
        if not os.path.exists('TranslateJson'):
            # 不存在，就创建
            os.makedirs('TranslateJson')
            
        self._dirRoot = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self._dirSpeech = os.path.join(self._dirRoot, 'TranslateJson')
        
    def translate(self,q):
        
        #check file
        
        
        path=self.down(q)
        f = open(path, 'r')
        content = f.read()
        text = json.loads(content)
        f.close()
        
        list1=self.formatdata(text)
        return list1
        #print(text.translation)
        #self.formatdata(text)
        #print(.translation)

    def _getWordMp3FilePath(self, word):
        '''
        获取单词的MP3本地文件路径
        如果有MP3文件，返回路径(绝对路径)
        如果没有，返回None
        '''
        word = word.lower()  # 小写
        self._word = word
        self._fileName = self._word + '.json'
        self._filePath = os.path.join(self._dirSpeech, self._fileName)

        # 判断是否存在这个MP3文件
        if os.path.exists(self._filePath):
            # 存在这个mp3
            return self._filePath
        else:
            # 不存在这个MP3，返回none
            return None
    
    def down(self, word):
        '''
        下载单词的MP3
        判断语音库中是否有对应的MP3
        如果没有就下载
        '''
        word = word.lower()  # 小写
        tmp = self._getWordMp3FilePath(word)
        if tmp is None:
            # 调用下载程序，下载到目标文件夹
            print('不存在 %s.json 文件\n将URL:\n' % word, '\n下载到:\n', self._filePath)
            # 下载到目标地址
            self.data['q'] = word
            self.data['from'] = '源语言'
            self.data['to'] = '目标语言'
            self.data['signType'] = 'v3'
            curtime = str(int(time.time()))
            self.data['curtime'] = curtime
            salt = str(uuid.uuid1())
            signStr = APP_KEY + truncate(word) + salt + curtime + APP_SECRET
            sign = encrypt(signStr)
            self.data['appKey'] = APP_KEY
            self.data['salt'] = salt
            self.data['sign'] = sign
            res=self.respone()
            text=json.loads(res.text)
            b = json.dumps(text,sort_keys=True, indent=4)
            #open(self._filePath, 'w')
            f2 = open(self._filePath, 'w')
            f2.write(b)
            f2.close()
            print('%s.json 下载完成' % self._word)
        else:
            print('已经存在 %s.json, 不需要下载' % self._word)

        # 返回声音文件路径
        return self._filePath
    
    
    def respone(self):
        response = do_request(self.data)
        self.contentType = response.headers['Content-Type']
        if self.contentType == "audio/mp3":
            millis = int(round(time.time() * 1000))
            filePath = "合成的音频存储路径" + str(millis) + ".mp3"
            fo = open(filePath, 'wb')
            fo.write(response.content)
            fo.close()
        return response
    #else:
        #print(response.content)
    
    def formatdata(self,text):
        FINDLIST=['n.','v.','adj.','adv.','prep','pron','vi','vt']
        if text['isWord']==False:
            d=[['P'],text['translation'][0]]
            return [['P'],text['translation'][0]]
        explains=text['basic']['explains']
        list1=[[],[]]
        
        for i in explains:
            
            if i[0:4] in FINDLIST:
                list1[0].append(i[0:4])
                count=0
                #d=i[2:].split('，')
                #d=list(map(str.split(','),d))
                for ii in i[4:].split('，'):
                    if count>=2:
                        break
                    list1[1].append(ii)
                    count+=1
                    
            if i[0:3] in FINDLIST:
                list1[0].append(i[0:3])
                count=0
                #d=i[2:].split('，')
                #d=list(map(str.split(','),d))
                for ii in i[3:].split('，'):
                    if count>=2:
                        break
                    list1[1].append(ii)
                    count+=1
            
            if i[0:2] in FINDLIST:
                list1[0].append(i[0:2])
                count=0
                #d=i[2:].split('，')
                #d=list(map(str.split(','),d))
                for ii in i[2:].split('，'):
                    if count>=2:
                        break
                    list1[1].append(ii)
                    count+=1
                    
        if list1==[[],[]]:
            return [['P'],[explains[0]]]

        return list1
                #for ii in 
                #list1[1].append()


if __name__ == '__main__':
    os.chdir('../')
    YT=YoudaoTranslate()
    YT.translate('virtual choir')