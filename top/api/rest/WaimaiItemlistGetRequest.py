'''
Created by auto_sdk on 2014-11-09 14:51:18
'''
from top.api.base import RestApi
class WaimaiItemlistGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.category_id = None
		self.end_modified = None
		self.fields = None
		self.keyword = None
		self.order_by = None
		self.page_no = None
		self.page_size = None
		self.sales_status = None
		self.shopid = None
		self.start_modified = None

	def getapiname(self):
		return 'taobao.waimai.itemlist.get'
