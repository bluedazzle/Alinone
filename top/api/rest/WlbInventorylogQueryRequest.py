'''
Created by auto_sdk on 2014-11-09 14:51:18
'''
from top.api.base import RestApi
class WlbInventorylogQueryRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.gmt_end = None
		self.gmt_start = None
		self.item_id = None
		self.op_type = None
		self.op_user_id = None
		self.order_code = None
		self.page_no = None
		self.page_size = None
		self.store_code = None

	def getapiname(self):
		return 'taobao.wlb.inventorylog.query'
