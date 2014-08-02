##Introduce
This is an crawler for Sina Weibo, based on Scrapy.
##Dependency
* pyqt: to parse javascript
* rsa: to encode when posting

##Install Dependency

###How to install rsa

    pip install rsa

###How to install PyQt

####For Mac

    brew install pyqt

####For Ubuntu

    sudo apt-get install python-pip python2.7-dev libxext-dev python-qt4 qt4-dev-tools build-essential
    pip install PyQt
    pip install SIP
    python2.7 configure.py
    make
    sudo make install
    python2.7 configure.py
    make
    sudo make install

####Validation

Excute this code with python:

    from PyQt4 import QtCore, QtGui

If there is no error, we install PyQt successfully. If not, you should visit [this page](http://www.pythoncentral.io/install-pyside-pyqt-on-windows-mac-linux/)

##Reference：
###For login module
* http://www.douban.com/note/201767245/
* http://yoyzhou.github.io/blog/2013/03/18/sina-weibo-login-simulator-in-python/
* http://www.crazyant.net/796.html
* http://www.codeif.com/post/843/

###For js-parsing
* http://webscraping.com/blog/Scraping-JavaScript-webpages-with-webkit/
* http://www.cnblogs.com/asmblog/archive/2013/05/07/3063809.html
