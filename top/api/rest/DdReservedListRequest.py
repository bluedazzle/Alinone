'''
Created by auto_sdk on 2014-11-09 14:51:18
'''
from top.api.base import RestApi
class DdReservedListRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.buyer_nick = None
		self.buyer_phone = None
		self.create_end = None
		self.create_start = None
		self.ends = None
		self.option = None
		self.pn = None
		self.ps = None
		self.starts = None
		self.status = None
		self.store_id = None

	def getapiname(self):
		return 'taobao.dd.reserved.list'
