'''
Created by auto_sdk on 2014-11-09 14:51:18
'''
from top.api.base import RestApi
class FenxiaoCooperationTerminateRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.cooperate_id = None
		self.end_remain_days = None
		self.end_remark = None

	def getapiname(self):
		return 'taobao.fenxiao.cooperation.terminate'
