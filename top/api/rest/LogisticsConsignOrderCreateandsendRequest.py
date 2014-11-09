'''
Created by auto_sdk on 2014-11-09 14:51:18
'''
from top.api.base import RestApi
class LogisticsConsignOrderCreateandsendRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.company_id = None
		self.item_json_string = None
		self.logis_type = None
		self.mail_no = None
		self.order_source = None
		self.order_type = None
		self.r_address = None
		self.r_area_id = None
		self.r_city_name = None
		self.r_dist_name = None
		self.r_mobile_phone = None
		self.r_name = None
		self.r_prov_name = None
		self.r_telephone = None
		self.r_zip_code = None
		self.s_address = None
		self.s_area_id = None
		self.s_city_name = None
		self.s_dist_name = None
		self.s_mobile_phone = None
		self.s_name = None
		self.s_prov_name = None
		self.s_telephone = None
		self.s_zip_code = None
		self.shipping = None
		self.trade_id = None
		self.user_id = None

	def getapiname(self):
		return 'taobao.logistics.consign.order.createandsend'
