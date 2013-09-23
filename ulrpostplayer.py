# -*- coding: gbk -*- 
#!/usr/bin/python  
  
from HTMLParser import HTMLParser
import urlparse  
import urllib  
import urllib2  
import cookielib  
import string  
import re  
import sys
import chardet
  
import threading

class MyHTMLParser(HTMLParser):

    def __init__(self, tid, lock=None):

	HTMLParser.__init__(self)

	self.tid = tid
	self.credit = False
	self.computer = False
	self.lock = lock

	#self.flags = {'年龄': False, '天赋': False, '耐力': False, '力量': False, '速度': False}
	self.flags = [False for i in xrange(5)]


    def handle_starttag(self, tag, attrs):
        #print "Encountered a start tag:", tag, attrs
	#Encountered a start tag: span [('title', '2.98'), ('class', 'balls-skill'), ('style', 'width : 36px')]
	if self.flags[1] and tag == "span":
		self.flags[1] = False
		self.telent = attrs[0][1]
	elif self.flags[2] and tag == "span":
		self.flags[2] = False
		self.con = attrs[0][1]
	elif self.flags[3] and tag == "span":
		self.flags[3] = False
		self.strong = attrs[0][1]
	elif self.flags[4] and tag == "span":
		self.flags[4] = False
		self.speed = attrs[0][1]
		
		f = open('player.txt', "a+")
		print "%s 	http://rockingsoccer.com/zh/soccer/info/player-%d 	%s 	%s 	%s 	%s 	 %s" % (
			self.tid, self.tid, self.age, self.telent, self.con, self.strong, self.speed)
		f.writelines("%s 	http://rockingsoccer.com/zh/soccer/info/player-%d 	 %s 	 %s 	 %s 	 %s 	 %s\r\n"% (
				self.tid, self.tid, self.age, self.telent, self.con, self.strong, self.speed))
		f.flush()
		f.close()

    def handle_endtag(self, tag):
        #print "Encountered an end tag :", tag
	pass
    def handle_data(self, data):
        #print "Encountered some data  :", data
	if self.flags[0] == True:
		self.age = data[0:2]
		self.flags[0] = False
	if "年龄" == data:
		self.flags[0] = True
	elif "天赋" == data:
		self.flags[1] = True
	elif "耐力" == data:
		self.flags[2] = True
	elif "力量" == data:
		self.flags[3] = True
	elif "速度" == data:
		self.flags[4] = True



def doParse(lock, text, tid):
	typeEncode = sys.getfilesystemencoding()##系统默认编码
	infoencode = chardet.detect(text).get('encoding','utf-8')##通过第3方模块来自动提取网页的编码
	html = text.decode(infoencode,'ignore').encode('gb18030')##先转换成unicode编码，然后转换系统编码输出

	parser = MyHTMLParser(tid, lock)
	parser.feed(html) 


if __name__ == "__main__":
	#登录的主页面  
	hosturl = 'http://www.rockingsoccer.com/' 
	#post数据接收和处理的页面（我们要向这个页面发送我们构造的Post数据）  
	posturl = 'http://rockingsoccer.com/zh/soccer/info/player-' #从数据包中分析出，处理post请求的url  
	  
	post2url = 'http://rockingsoccer.com/zh/soccer'
	#设置一个cookie处理器，它负责从服务器下载cookie到本地，并且在发送请求时带上本地的cookie  
	cj = cookielib.LWPCookieJar()  
	cookie_support = urllib2.HTTPCookieProcessor(cj)  
	opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)  
	urllib2.install_opener(opener)  
	  
	#打开登录主页面（他的目的是从页面下载cookie，这样我们在再送post数据时就有cookie了，否则发送不成功）  
	h = urllib2.urlopen(hosturl)  
	  
	#构造header，一般header至少要包含一下两项。这两项是从抓到的包里分析得出的。  
	headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',  
	           'Referer' : '******'}  
	#构造Post数据，从抓大的包里分析得出的。  
	postData = {'login' : '',  
	            'username' : 'nimitzlin',
	            'password' : 'n1111111',
	            }  
	  
	#需要给Post数据编码  
	postData = urllib.urlencode(postData)  
	  
	request = urllib2.Request(post2url, postData, headers)  
	
	playerurl = "http://rockingsoccer.com/zh/soccer/info/player-"
	lock = threading.Lock() 
	for i in xrange(378000,1,-1):
		request = urllib2.Request(playerurl+str(i), postData, headers)  
		try:
			response = urllib2.urlopen(request)  
		except urllib2.HTTPError:
			continue
		text = response.read()  
		
		threading.Thread(target = doParse, args = (lock, text, i), name = 'thread-' + str(i)).start()  
		#typeEncode = sys.getfilesystemencoding()##系统默认编码
		#infoencode = chardet.detect(text).get('encoding','utf-8')##通过第3方模块来自动提取网页的编码
		#html = text.decode(infoencode,'ignore').encode('gb18030')##先转换成unicode编码，然后转换系统编码输出

		#parser = MyHTMLParser(i)
		#parser.feed(html) 
