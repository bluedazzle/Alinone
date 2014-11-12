'''
Created by auto_sdk on 2014-11-09 14:51:18
'''
from top.api.base import RestApi
class WlbItemBatchQueryRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.item_ids = None
		self.page_no = None
		self.page_size = None
		self.store_code = None

	def getapiname(self):
		return 'taobao.wlb.item.batch.query'
