# coding=utf-8
from bs4 import BeautifulSoup
from urlparse import urlsplit
from os.path import basename
import sys,pdb,urllib2,requests,os,json


def main():
	if len(sys.argv) != 2:
		print "\n\tplease input the address!!!\n\n\trun like this: \n\t$python zhihuPic.py https://www.zhihu.com/question/34810002\n\n"
		return
	url = sys.argv[1]
	qst_html = urllib2.urlopen(url).read()
	soup0 = BeautifulSoup(qst_html)

	question_name = soup0.h2.text.strip()
	if not os.path.exists(question_name):
		os.mkdir(question_name)

	answers_num = int(soup0.h3.text.split(' ')[0])

	imgs = soup0.find_all('img')

	for img in imgs:
		try:
			data = urllib2.urlopen(img['src']).read()
			file_name = basename(urlsplit(img['src'])[2])
			print "爬取："+file_name+"..."
			output = open(question_name+'/'+file_name, 'wb')
			output.write(data)
			output.close()
		except Exception, e:
			continue

main()
