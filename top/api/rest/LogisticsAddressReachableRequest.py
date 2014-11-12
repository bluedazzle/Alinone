'''
Created by auto_sdk on 2014-11-09 14:51:18
'''
from top.api.base import RestApi
class LogisticsAddressReachableRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.address = None
		self.area_code = None
		self.partner_ids = None
		self.service_type = None
		self.source_area_code = None

	def getapiname(self):
		return 'taobao.logistics.address.reachable'
