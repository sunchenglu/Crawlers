# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import urllib2,pdb,re,requests,json,time,os

from urlparse import urlsplit
from os.path import basename
from bs4 import BeautifulSoup

import settings
sys.path.append("../../src")
from crawler_obj import Crawler_Base



class Crawler(Crawler_Base):

	#返回True时停止线程,程序结束
	def download_page(self):
		home_rspn = self.s.get(settings.HOME_URL)
		soup = BeautifulSoup(home_rspn.content)
		link_tags = soup.find_all(attrs={"class":"question_link"})

		for tag in link_tags:
			question_id = tag['href'].split('#')[0]
			url = settings.HOME_URL + question_id
			self.deal_question(url)
			time.sleep(2)

		return True

	def deal_question(self,url):
		qst_rspn = self.s.get(url)
		soup = BeautifulSoup(qst_rspn.content)

		try:
			question_detail = {}
			question_detail['title'] = soup.h2.text.strip()
			tag_list = soup.find_all(attrs={"class":"zm-item-tag"})
			labels = ''
			for tag in tag_list:
				labels += tag.text.strip() + ' '
			question_detail['labels'] = labels
			question_detail['answers_num'] = soup.h3['data-num']
			question_detail['followers'] = soup.strong.text
			question_detail['detail'] = soup.find(id='zh-question-detail').text.strip()
			q_dir = question_detail['title']
			if not os.path.exists(q_dir):
				os.mkdir(q_dir)
			output = open(q_dir+'/question_detail.txt', 'w')
			output.write("地址:"+url+'\n')
			output.write("标题:"+question_detail['title']+'\n')
			output.write("标签:"+question_detail['labels']+'\n')
			output.write("回答数:"+question_detail['answers_num']+'\n')
			output.write("关注人数:"+question_detail['followers']+'\n')
			output.write("内容:"+question_detail['detail']+'\n')
			output.close()
		except Exception, e:
			print "获取问题详情时出错..."



		


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