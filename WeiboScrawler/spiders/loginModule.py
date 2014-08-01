#coding:utf-8
import urllib2
import cookielib
import re
import json
import urllib
import base64
import binascii
import rsa


class LoginModule:
    def __init__(self):
        print("This is LoginModule")


class LoginModule:
    def __init__(self):
        print("This is LoginModule")
        self.serverUrl="http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.11)&_=1379834957683"
        self.loginUrl="http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.11)"
        self.postHeader={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20100101 Firefox/24.0'}


    def login(self, username, password):
        self.getServerTime()
        serverData=self.getServerTime()
        postdata=self.postEncode(username, password, serverData)
        print(postdata)


    def getServerTime(self):
        serverData = urllib2.urlopen(self.serverUrl).read()
        return serverData


    def analyzeServerTime(self, data):
        p = re.compile('\((.*)\)')
        jsonData = p.search(data).group(1)
        data = json.loads(jsonData)
        print(data)
        serverTime = str(data['servertime'])
        nonce = data['nonce']
        pubkey = data['pubkey']#
        rsakv = data['rsakv']#
        print "Server time is:", serverTime
        print "Nonce is:", nonce
        print(nonce)
        return {'servertime':serverTime, 'nonce':nonce, 'pubkey':pubkey, 'rsakv':rsakv}


    def postEncode(self, username, password, serverData):
        data=self.analyzeServerTime(serverData)
        encodedUserName=self.get_username(username)#用户名使用base64加密
        encodedPassWord=self.get_password(password, data['servertime'], data['nonce'], data['pubkey'])#目前密码采用rsa加密
        postPara = {
            'entry': 'weibo',
            'gateway': '1',
            'from': '',
            'savestate': '7',
            'userticket': '1',
            'ssosimplelogin': '1',
            'vsnf': '1',
            'vsnval': '',
            'su': encodedUserName,
            'service': 'miniblog',
            'servertime': data['servertime'],
            'nonce': data['nonce'],
            'pwencode': 'rsa2',
            'sp': encodedPassWord,
            'encoding': 'UTF-8',
            'prelt': '115',
            'rsakv': data['rsakv'],
            'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype': 'META'
        }
        postData = urllib.urlencode(postPara)#网络编码
        return postData


    def get_username(self, username):
        userNameTemp = urllib.quote(username)
        userNameEncoded = base64.encodestring(userNameTemp)[:-1]
        return userNameEncoded


    def get_password(self, password, servertime, nonce, pubkey):
        rsaPublickey = int(pubkey, 16)
        key = rsa.PublicKey(rsaPublickey, 65537) #创建公钥
        message = str(servertime) + '\t' + str(nonce) + '\n' + str(password) #拼接明文js加密文件中得到
        passwd = rsa.encrypt(message, key) #加密
        passwd = binascii.b2a_hex(passwd) #将加密信息转换为16进制。
        return passwd

a=LoginModule()
a.login("a","")
