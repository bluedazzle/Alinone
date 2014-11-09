'''
Created by auto_sdk on 2014-11-09 14:51:18
'''
from top.api.base import RestApi
class DeliveryTemplateAddRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.assumer = None
		self.consign_area_id = None
		self.name = None
		self.template_add_fees = None
		self.template_add_standards = None
		self.template_dests = None
		self.template_start_fees = None
		self.template_start_standards = None
		self.template_types = None
		self.valuation = None

	def getapiname(self):
		return 'taobao.delivery.template.add'
