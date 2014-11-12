'''
Created by auto_sdk on 2014-11-09 14:51:18
'''
from top.api.base import RestApi
class ItemGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.fields = None
		self.num_iid = None
		self.track_iid = None

	def getapiname(self):
		return 'taobao.item.get'
