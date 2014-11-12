'''
Created by auto_sdk on 2014-11-09 14:51:18
'''
from top.api.base import RestApi
class ScitemMapQueryRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.item_id = None
		self.sku_id = None

	def getapiname(self):
		return 'taobao.scitem.map.query'
