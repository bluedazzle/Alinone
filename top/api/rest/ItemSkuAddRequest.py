'''
Created by auto_sdk on 2014-11-09 14:51:18
'''
from top.api.base import RestApi
class ItemSkuAddRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.ignorewarning = None
		self.item_price = None
		self.lang = None
		self.num_iid = None
		self.outer_id = None
		self.price = None
		self.properties = None
		self.quantity = None
		self.sku_hd_height = None
		self.sku_hd_lamp_quantity = None
		self.sku_hd_length = None
		self.spec_id = None

	def getapiname(self):
		return 'taobao.item.sku.add'
