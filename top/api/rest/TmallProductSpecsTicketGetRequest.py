'''
Created by auto_sdk on 2014-11-09 14:51:18
'''
from top.api.base import RestApi
class TmallProductSpecsTicketGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.spec_ids = None

	def getapiname(self):
		return 'tmall.product.specs.ticket.get'
