'''
Created by auto_sdk on 2014-11-09 14:51:18
'''
from top.api.base import RestApi
class WaimaiAddressOperateRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.address = None
		self.city = None
		self.defaulted = None
		self.id = None
		self.name = None
		self.phone = None
		self.x = None
		self.y = None

	def getapiname(self):
		return 'taobao.waimai.address.operate'
