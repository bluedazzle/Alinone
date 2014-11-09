'''
Created by auto_sdk on 2014-11-09 14:51:18
'''
from top.api.base import RestApi
class InventoryIpcInventorydetailGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.biz_order_id = None
		self.biz_sub_order_id = None
		self.page_index = None
		self.page_size = None
		self.sc_item_id = None
		self.status_query = None

	def getapiname(self):
		return 'taobao.inventory.ipc.inventorydetail.get'
