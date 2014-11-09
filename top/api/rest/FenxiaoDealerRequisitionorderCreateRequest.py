'''
Created by auto_sdk on 2014-11-09 14:51:18
'''
from top.api.base import RestApi
class FenxiaoDealerRequisitionorderCreateRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.address = None
		self.buyer_name = None
		self.city = None
		self.district = None
		self.id_card_number = None
		self.logistics_type = None
		self.mobile = None
		self.order_detail = None
		self.phone = None
		self.post_code = None
		self.province = None

	def getapiname(self):
		return 'taobao.fenxiao.dealer.requisitionorder.create'
