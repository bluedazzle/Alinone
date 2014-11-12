'''
Created by auto_sdk on 2014-11-09 14:51:18
'''
from top.api.base import RestApi
class WaimaiOrderIndexGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.end_time = None
		self.interval = None
		self.order_status = None
		self.order_type = None
		self.page_no = None
		self.page_size = None
		self.shop_id = None
		self.start_time = None

	def getapiname(self):
		return 'taobao.waimai.order.index.get'
