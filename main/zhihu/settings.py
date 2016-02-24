# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

#请求的头部信息
HEADERS = {
    "Accept": "*/*",
    "Accept-Encoding":"gzip, deflate",
    "Accept-Language": "zh,en-US;q=0.8,en;q=0.6",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Pragma": "no-cache",
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

USER = {
	'phone_num': '',
	'password': '',
}

HOME_URL = 'http://www.zhihu.com'

LOGIN_URL = "https://www.zhihu.com/login/phone_num"