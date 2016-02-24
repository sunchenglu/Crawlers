# coding=utf-8
import sys,os
reload(sys)
sys.setdefaultencoding('utf-8')
import sys,pdb,thread,datetime
import requests

class Crawler_Base(object):

	def __init__(self,**args):

		self.name = args['name']

		self.home_url = args['home_url']

		self.thread_stop = False

		self.s = requests.Session()

	def start_task(self):

		thread.start_new_thread(self.task_run,())

	def task_run(self):

		print self.name + '爬取线程运行中...'

		self.login()

		while self.thread_stop != True:

			self.thread_stop = self.download_page()

		print '爬取线程已停止,按ctrl+c退出'

		thread.exit_thread()

	def login(self):
		pass

	def download_page(self):
		pass
		return True
		
test = 5