'''
Created by auto_sdk on 2014-11-09 14:51:18
'''
from top.api.base import RestApi
class FenxiaoProductcatUpdateRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.agent_cost_percent = None
		self.dealer_cost_percent = None
		self.name = None
		self.product_line_id = None
		self.retail_high_percent = None
		self.retail_low_percent = None

	def getapiname(self):
		return 'taobao.fenxiao.productcat.update'
