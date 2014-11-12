'''
Created by auto_sdk on 2014-11-09 14:51:18
'''
from top.api.base import RestApi
class DdAuctionRuleQueryRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.current_date = None
		self.day_time = None
		self.id = None
		self.is_diandian = None
		self.is_takeout = None
		self.name = None
		self.status_array = None
		self.store_id = None
		self.weekly = None

	def getapiname(self):
		return 'taobao.dd.auction.rule.query'
