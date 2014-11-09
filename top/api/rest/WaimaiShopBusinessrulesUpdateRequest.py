'''
Created by auto_sdk on 2014-11-09 14:51:18
'''
from top.api.base import RestApi
class WaimaiShopBusinessrulesUpdateRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.area_range = None
		self.delivery_amount = None
		self.delivery_area = None
		self.delivery_time = None
		self.early_minutes = None
		self.full_amount = None
		self.minimum_amount = None
		self.mobile = None
		self.shopid = None
		self.support_days = None

	def getapiname(self):
		return 'taobao.waimai.shop.businessrules.update'
