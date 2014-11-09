'''
Created by auto_sdk on 2014-11-09 14:51:18
'''
from top.api.base import RestApi
class PictureGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.client_type = None
		self.deleted = None
		self.end_date = None
		self.modified_time = None
		self.order_by = None
		self.page_no = None
		self.page_size = None
		self.picture_category_id = None
		self.picture_id = None
		self.start_date = None
		self.title = None
		self.urls = None

	def getapiname(self):
		return 'taobao.picture.get'
