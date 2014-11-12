'''
Created by auto_sdk on 2014-11-09 14:51:18
'''
from top.api.base import RestApi
class RefundsApplyGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.fields = None
		self.page_no = None
		self.page_size = None
		self.seller_nick = None
		self.status = None
		self.type = None

	def getapiname(self):
		return 'taobao.refunds.apply.get'
