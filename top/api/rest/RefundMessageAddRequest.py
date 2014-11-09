'''
Created by auto_sdk on 2014-11-09 14:51:18
'''
from top.api.base import RestApi
class RefundMessageAddRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.content = None
		self.image = None
		self.refund_id = None

	def getapiname(self):
		return 'taobao.refund.message.add'

	def getMultipartParas(self):
		return ['image']
