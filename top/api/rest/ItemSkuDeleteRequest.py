'''
Created by auto_sdk on 2014-11-09 14:51:18
'''
from top.api.base import RestApi
class ItemSkuDeleteRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.ignorewarning = None
		self.item_num = None
		self.item_price = None
		self.lang = None
		self.num_iid = None
		self.properties = None

	def getapiname(self):
		return 'taobao.item.sku.delete'
