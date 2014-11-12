'''
Created by auto_sdk on 2014-11-09 14:51:18
'''
from top.api.base import RestApi
class TradeShippingaddressUpdateRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.receiver_address = None
		self.receiver_city = None
		self.receiver_district = None
		self.receiver_mobile = None
		self.receiver_name = None
		self.receiver_phone = None
		self.receiver_state = None
		self.receiver_zip = None
		self.tid = None

	def getapiname(self):
		return 'taobao.trade.shippingaddress.update'
