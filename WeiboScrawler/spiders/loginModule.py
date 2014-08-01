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
        self.server_url = "http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.11)&_=1379834957683"
        self.login_url = "http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.11)"
        self.post_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20100101 Firefox/24.0'}

    def login(self, username, password):
        # 获取一个保存cookie的对象
        # Get an object to save cookie
        cj = cookielib.LWPCookieJar()
        # 将一个保存cookie对象，和一个HTTP的cookie的处理器绑定
        # Bind the object to save cookie with a HTTP cookie processor
        cookie_support = urllib2.HTTPCookieProcessor(cj)
        # 创建一个opener，将保存了cookie的http处理器，还有设置一个handler用于处理http的URL的打开
        # Create an opener to save the HTTP processor, and at the same time set an handler to process http url
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        # 将包含了cookie、http处理器、http的handler的资源和urllib2对象板顶在一起
        # install this opener in urllib2
        urllib2.install_opener(opener)

        # First Step: get the server data to encode the post information (username and password, etc)
        server_data = self.get_server_time()

        # Second Step: encode the post information
        post_data = self.post_encode(username, password, server_data)

        # Third Step: post the data to get response which contains the login url
        req = urllib2.Request(
            url=self.login_url,
            data=post_data,
            headers=self.post_header
        )
        result = urllib2.urlopen(req)
        text = result.read()

        # Fourth Step: analyze the response to get login url and cookie will save in cj object automatically
        try:
            login_url = self.get_redirect_data(text)  # 解析重定位结果
            login_data = urllib2.urlopen(login_url).read()
        except Exception as e:
            print('Login Error:'+str(e))
            return None, False

        # Fifth Step: check the login-state
        patt_feedback = 'feedBackUrlCallBack\((.*)\)'
        p = re.compile(patt_feedback, re.MULTILINE)
        feedback = p.search(login_data).group(1)
        feedback_json = json.loads(feedback)
        if not feedback_json['result']:
            print('Login Error!')
            return False, None

        # Transform the cookie saved in cj object into string
        #cs = ['%s=%s' % (c.name, c.value) for c in cj]
        #cookie = '; '.join(cs)

        cookie=[]
        for c in cj:
            cookie.append({'name': c.name, 'value': c.value})
        return True, cookie

    def get_server_time(self):
        server_data = urllib2.urlopen(self.server_url).read()
        return server_data

    def analyze_server_time(self, data):
        p = re.compile('\((.*)\)')
        json_data = p.search(data).group(1)
        data = json.loads(json_data)
        server_time = str(data['servertime'])
        nonce = data['nonce']
        pubkey = data['pubkey']#
        rsakv = data['rsakv']#

        return {'servertime': server_time, 'nonce': nonce, 'pubkey': pubkey, 'rsakv': rsakv}

    def post_encode(self, username, password, server_data):
        data = self.analyze_server_time(server_data)
        encoded_username = self.get_username(username)  # 用户名使用base64加密
        encoded_password = self.get_password(password, data['servertime'], data['nonce'], data['pubkey'])#目前密码采用rsa加密
        post_para = {
            'entry': 'weibo',
            'gateway': '1',
            'from': '',
            'savestate': '7',
            'userticket': '1',
            'ssosimplelogin': '1',
            'vsnf': '1',
            'vsnval': '',
            'su': encoded_username,
            'service': 'miniblog',
            'servertime': data['servertime'],
            'nonce': data['nonce'],
            'pwencode': 'rsa2',
            'sp': encoded_password,
            'encoding': 'UTF-8',
            'prelt': '115',
            'rsakv': data['rsakv'],
            'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype': 'META'
        }
        post_data = urllib.urlencode(post_para)  # 网络编码
        return post_data

    def get_username(self, username):
        quote_user_name = urllib.quote(username)
        user_name_encoded = base64.encodestring(quote_user_name)[:-1]
        return user_name_encoded

    def get_password(self, password, server_time, nonce, pubkey):
        rsa_public_key = int(pubkey, 16)
        key = rsa.PublicKey(rsa_public_key, 65537)  # 创建公钥
        message = str(server_time) + '\t' + str(nonce) + '\n' + str(password)  # 拼接明文js加密文件中得到
        rsa_password = rsa.encrypt(message, key)  # 加密
        post_password = binascii.b2a_hex(rsa_password)  # 将加密信息转换为16进制。
        return post_password

    def get_redirect_data(self, text):
        p = re.compile('location\.replace\([\'"](.*?)[\'"]\)')
        login_url = p.search(text).group(1)
        return login_url
