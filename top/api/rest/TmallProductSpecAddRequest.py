'''
Created by auto_sdk on 2014-11-09 14:51:18
'''
from top.api.base import RestApi
class TmallProductSpecAddRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.barcode = None
		self.certified_pic_str = None
		self.certified_txt_str = None
		self.change_prop = None
		self.customer_spec_props = None
		self.image = None
		self.label_price = None
		self.market_time = None
		self.product_code = None
		self.product_id = None
		self.spec_props = None
		self.spec_props_alias = None

	def getapiname(self):
		return 'tmall.product.spec.add'

	def getMultipartParas(self):
		return ['image']
