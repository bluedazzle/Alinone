'''
Created by auto_sdk on 2014-11-09 14:51:18
'''
from top.api.base import RestApi
class DdMenuDetailRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.menu_id = None
		self.order_id = None
		self.out_store_id = None
		self.store_id = None

	def getapiname(self):
		return 'taobao.dd.menu.detail'
