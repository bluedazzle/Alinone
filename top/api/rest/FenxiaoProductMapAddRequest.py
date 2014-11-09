'''
Created by auto_sdk on 2014-11-09 14:51:18
'''
from top.api.base import RestApi
class FenxiaoProductMapAddRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.not_check_outer_code = None
		self.product_id = None
		self.sc_item_id = None
		self.sc_item_ids = None
		self.sku_ids = None

	def getapiname(self):
		return 'taobao.fenxiao.product.map.add'
