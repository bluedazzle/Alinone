'''
Created by auto_sdk on 2014-11-09 14:51:18
'''
from top.api.base import RestApi
class FenxiaoDealerRequisitionorderGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.end_date = None
		self.fields = None
		self.identity = None
		self.order_status = None
		self.page_no = None
		self.page_size = None
		self.start_date = None

	def getapiname(self):
		return 'taobao.fenxiao.dealer.requisitionorder.get'
