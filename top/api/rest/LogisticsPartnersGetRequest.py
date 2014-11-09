'''
Created by auto_sdk on 2014-11-09 14:51:18
'''
from top.api.base import RestApi
class LogisticsPartnersGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.goods_value = None
		self.is_need_carriage = None
		self.service_type = None
		self.source_id = None
		self.target_id = None

	def getapiname(self):
		return 'taobao.logistics.partners.get'
