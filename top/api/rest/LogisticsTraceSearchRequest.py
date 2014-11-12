'''
Created by auto_sdk on 2014-11-09 14:51:18
'''
from top.api.base import RestApi
class LogisticsTraceSearchRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.is_split = None
		self.seller_nick = None
		self.sub_tid = None
		self.tid = None

	def getapiname(self):
		return 'taobao.logistics.trace.search'
