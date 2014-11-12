'''
Created by auto_sdk on 2014-11-09 14:51:18
'''
from top.api.base import RestApi
class WlbItemConsignmentQueryRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.authorize_end_time = None
		self.authorize_start_time = None
		self.owner_user_nick = None
		self.page_no = None
		self.page_size = None

	def getapiname(self):
		return 'taobao.wlb.item.consignment.query'
