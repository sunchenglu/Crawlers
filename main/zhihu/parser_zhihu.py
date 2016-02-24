# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import urllib2,pdb,re,requests,json,time

from urlparse import urlsplit
from os.path import basename
from bs4 import BeautifulSoup

import settings
sys.path.append("../../src")
from crawler_obj import Crawler_Base



class Crawler(Crawler_Base):

	#返回True时停止线程,程序结束
	def download_page(self):

		

		return True

	def login(self):
		print "登录中..."

		rspn = self.s.get(settings.HOME_URL,headers=settings.HEADERS,verify=True)
		soup = BeautifulSoup(rspn.content)
		_xsrf = soup.input['value']

		post_data = settings.USER
		post_data['_xsrf'] = _xsrf
		post_data['remember_me'] = 'true'

		login_rspn = self.s.post(settings.LOGIN_URL,headers=settings.HEADERS,data=post_data,timeout=10,verify=False)

		json_content = json.loads(login_rspn.text)

		print json_content['msg']

		if int(json_content['r']) == 0:
			print '登录成功,继续...'
		else:
			print '登录失败,情重新试试'
			self.thread_stop = True


if __name__ == '__main__':
	zhihu_crawler = Crawler(name='知乎',home_url= settings.HOME_URL)

	zhihu_crawler.start_task()
	while True:
	    pass