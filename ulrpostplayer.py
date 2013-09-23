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

	#self.flags = {'����': False, '�츳': False, '����': False, '����': False, '�ٶ�': False}
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
	if "����" == data:
		self.flags[0] = True
	elif "�츳" == data:
		self.flags[1] = True
	elif "����" == data:
		self.flags[2] = True
	elif "����" == data:
		self.flags[3] = True
	elif "�ٶ�" == data:
		self.flags[4] = True



def doParse(lock, text, tid):
	typeEncode = sys.getfilesystemencoding()##ϵͳĬ�ϱ���
	infoencode = chardet.detect(text).get('encoding','utf-8')##ͨ����3��ģ�����Զ���ȡ��ҳ�ı���
	html = text.decode(infoencode,'ignore').encode('gb18030')##��ת����unicode���룬Ȼ��ת��ϵͳ�������

	parser = MyHTMLParser(tid, lock)
	parser.feed(html) 


if __name__ == "__main__":
	#��¼����ҳ��  
	hosturl = 'http://www.rockingsoccer.com/' 
	#post���ݽ��պʹ����ҳ�棨����Ҫ�����ҳ�淢�����ǹ����Post���ݣ�  
	posturl = 'http://rockingsoccer.com/zh/soccer/info/player-' #�����ݰ��з�����������post�����url  
	  
	post2url = 'http://rockingsoccer.com/zh/soccer'
	#����һ��cookie��������������ӷ���������cookie�����أ������ڷ�������ʱ���ϱ��ص�cookie  
	cj = cookielib.LWPCookieJar()  
	cookie_support = urllib2.HTTPCookieProcessor(cj)  
	opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)  
	urllib2.install_opener(opener)  
	  
	#�򿪵�¼��ҳ�棨����Ŀ���Ǵ�ҳ������cookie����������������post����ʱ����cookie�ˣ������Ͳ��ɹ���  
	h = urllib2.urlopen(hosturl)  
	  
	#����header��һ��header����Ҫ����һ������������Ǵ�ץ���İ�������ó��ġ�  
	headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',  
	           'Referer' : '******'}  
	#����Post���ݣ���ץ��İ�������ó��ġ�  
	postData = {'login' : '',  
	            'username' : 'nimitzlin',
	            'password' : 'n1111111',
	            }  
	  
	#��Ҫ��Post���ݱ���  
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
		#typeEncode = sys.getfilesystemencoding()##ϵͳĬ�ϱ���
		#infoencode = chardet.detect(text).get('encoding','utf-8')##ͨ����3��ģ�����Զ���ȡ��ҳ�ı���
		#html = text.decode(infoencode,'ignore').encode('gb18030')##��ת����unicode���룬Ȼ��ת��ϵͳ�������

		#parser = MyHTMLParser(i)
		#parser.feed(html) 
