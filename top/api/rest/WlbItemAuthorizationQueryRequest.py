'''
Created by auto_sdk on 2014-11-09 14:51:18
'''
from top.api.base import RestApi
class WlbItemAuthorizationQueryRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.item_id = None
		self.name = None
		self.page_no = None
		self.page_size = None
		self.rule_code = None
		self.status = None
		self.type = None

	def getapiname(self):
		return 'taobao.wlb.item.authorization.query'
