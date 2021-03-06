# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import urllib2,pdb,re,requests,json,time,os
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

		self.url_list = []

		for tag in link_tags:
			question_id = tag['href'].split('#')[0]
			url = settings.HOME_URL + question_id
			if url not in self.url_list:
				self.deal_question(url)
				self.url_list.append(url)
				# time.sleep(2)

		return True

	def deal_question(self,url):
		qst_rspn = self.s.get(url)
		soup = BeautifulSoup(qst_rspn.content)
		q_dir = self.get_question_about(soup,url)
		self.get_answers_about(soup,q_dir)

	def get_answers_about(self,soup,q_dir):
		answers = soup.find_all(attrs={"class":"zm-item-answer  zm-item-expanded"})
		count = 0
		for answer in answers:
			try:
				answer_detail = {}
				if answer.find(attrs={'class':'author-link'}) == None:
					answer_detail['author'] = "匿名用户" + str(count)
					count += 1
				else:
					answer_detail['author'] = answer.find(attrs={'class':'author-link'}).text
				answer_detail['up_num'] = answer.find(attrs={'class':'count'}).text
				answer_detail['detail'] = answer.find(attrs={'class':'zm-editable-content clearfix'}).text.strip()
				a_dir = answer_detail['author']
				a_dir = q_dir+'/'+a_dir
				if not os.path.exists(a_dir):
					os.mkdir(a_dir)
				output = open(a_dir+'/answer_detail.txt', 'w')
				output.write("作者:"+answer_detail['author']+'\n')
				output.write("赞同数:"+answer_detail['up_num']+'\n')
				output.write("回答内容:"+answer_detail['detail']+'\n')
				output.close()
				img_tag_list = answer.find(attrs={'class':'zm-editable-content clearfix'}).find_all('img')
				if img_tag_list != []:
					if not os.path.exists(a_dir + '/images'):
						os.mkdir(a_dir + '/images')
					img_src_list = []
					if len(img_tag_list) > 10:
						img_tag_list = img_tag_list[:settings.MAX_IMG_NUM*2]
					for img_tag in img_tag_list:
						img_src_list.append(img_tag['src'])
					pic_index = 0
					for img_src in img_src_list:
						try:
							if img_src.startswith('https://'):
								img_data = requests.get(img_src,stream=True,verify=False).content
								file_name = 'pic' + str(pic_index) + '.jpg'
								output = open(a_dir + '/images/' + file_name, 'wb')
								output.write(img_data)
								output.close()
								pic_index += 1
						except Exception, e:
							print "处理图片出现错误..."
			except Exception, e:
				print "处理回答出现错误..."
		print "该问题答案爬取完成..."

	#获取问题的相关信息
	def get_question_about(self,soup,url):
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
			q_dir = 'results/' + question_detail['title']
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

			img_tag_list = soup.find(id='zh-question-detail').find_all('img')
			if img_tag_list != []:
				img_src_list = []
				for img_tag in img_tag_list:
					img_src_list.append(img_tag['src'])
				for img_src in img_src_list:
					try:
						img_data = urllib2.urlopen(img_src).read()
						file_name = basename(urlsplit(img_src)[2])
						output = open(q_dir + '/' + file_name, 'wb')
						output.write(img_data)
						output.close()
					except Exception, e:
						print "处理图片出现错误..."

			print "获取问题  " + question_detail['title'] + "  的详情完成..."
			return q_dir
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