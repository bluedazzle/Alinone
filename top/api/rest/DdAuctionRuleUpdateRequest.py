'''
Created by auto_sdk on 2014-11-09 14:51:18
'''
from top.api.base import RestApi
class DdAuctionRuleUpdateRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.day_end = None
		self.day_start = None
		self.features = None
		self.id = None
		self.is_diandian = None
		self.is_takeout = None
		self.name = None
		self.rule_end = None
		self.rule_start = None
		self.sort = None
		self.status = None
		self.store_id = None
		self.weeklys = None

	def getapiname(self):
		return 'taobao.dd.auction.rule.update'
