'''
Created by auto_sdk on 2014-11-09 14:51:18
'''
from top.api.base import RestApi
class WaimaiItemUpdateRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.auctiondesc = None
		self.auctionstatus = None
		self.categoryid = None
		self.categoryids = None
		self.fields = None
		self.goodsno = None
		self.in_shop_id = None
		self.item_id = None
		self.limitbuy = None
		self.oriprice = None
		self.picurl = None
		self.price = None
		self.quantity = None
		self.rule_id = None
		self.sku_info = None
		self.title = None
		self.viceimage = None

	def getapiname(self):
		return 'taobao.waimai.item.update'
