'''
Created by auto_sdk on 2014-11-09 14:51:18
'''
from top.api.base import RestApi
class AppstoreSubscribeGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.nick = None

	def getapiname(self):
		return 'taobao.appstore.subscribe.get'