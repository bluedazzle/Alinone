'''
Created by auto_sdk on 2014-11-09 14:51:18
'''
from top.api.base import RestApi
class InventoryAdjustTradeRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.biz_unique_code = None
		self.items = None
		self.operate_time = None
		self.tb_order_type = None

	def getapiname(self):
		return 'taobao.inventory.adjust.trade'
