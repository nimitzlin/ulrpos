# -*- coding: gbk -*- 
#!/usr/bin/python  
import qianfeng
  
from HTMLParser import HTMLParser
import urlparse  
import urllib  
import urllib2  
import cookielib  
import string  
import re  
import sys
import chardet
  
class MyHTMLParser(HTMLParser):

    def __init__(self, tid):

	HTMLParser.__init__(self)

	self.tid = tid
	self.credit = False
	self.computer = False

    def handle_starttag(self, tag, attrs):
        #print "Encountered a start tag:", tag
	pass
    def handle_endtag(self, tag):
        #print "Encountered an end tag :", tag
	pass
    def handle_data(self, data):
        #print "Encountered some data  :", data
	if "����" == data:
		self.credit = True
		return

	if "���Զ�: ���������ɵ��Թ���" == data:
		self.computer = True

	if self.credit:
		f = open('team.txt', "a+")
		if self.computer:
			#print "http://rockingsoccer.com/zh/soccer/info/team-%s" % self.tid, data, "���Զ�"
			f.writelines("http://rockingsoccer.com/zh/soccer/info/team-%s %s %s \r\n" % (self.tid, data, "���Զ�"))
			f.flush()
		else:
			pass
			#print "http://rockingsoccer.com/zh/soccer/info/team-%s" % self.tid, data, self.computer
			#f.writelines("http://rockingsoccer.com/zh/soccer/info/team-%s %s %s \r\n" % (self.tid, data, "��"))
			#f.flush()
		f.close()
		self.credit = False


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
	
	teamurl = "http://rockingsoccer.com/zh/soccer/info/team-"
	
	for i in xrange(15000):
		request = urllib2.Request(teamurl+str(i), postData, headers)  
		try:
			response = urllib2.urlopen(request)  
		except urllib2.HTTPError:
			continue
		text = response.read()  
	
		typeEncode = sys.getfilesystemencoding()##ϵͳĬ�ϱ���
		infoencode = chardet.detect(text).get('encoding','utf-8')##ͨ����3��ģ�����Զ���ȡ��ҳ�ı���
		html = text.decode(infoencode,'ignore').encode('gb18030')##��ת����unicode���룬Ȼ��ת��ϵͳ�������

		parser = MyHTMLParser(i)
		parser.feed(html) 
