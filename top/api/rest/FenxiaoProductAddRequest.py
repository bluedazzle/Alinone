'''
Created by auto_sdk on 2014-11-09 14:51:18
'''
from top.api.base import RestApi
class FenxiaoProductAddRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.alarm_number = None
		self.category_id = None
		self.city = None
		self.cost_price = None
		self.dealer_cost_price = None
		self.desc = None
		self.discount_id = None
		self.have_guarantee = None
		self.have_invoice = None
		self.image = None
		self.input_properties = None
		self.is_authz = None
		self.item_id = None
		self.name = None
		self.outer_id = None
		self.pic_path = None
		self.postage_ems = None
		self.postage_fast = None
		self.postage_id = None
		self.postage_ordinary = None
		self.postage_type = None
		self.productcat_id = None
		self.properties = None
		self.property_alias = None
		self.prov = None
		self.quantity = None
		self.retail_price_high = None
		self.retail_price_low = None
		self.sku_cost_prices = None
		self.sku_dealer_cost_prices = None
		self.sku_outer_ids = None
		self.sku_properties = None
		self.sku_quantitys = None
		self.sku_standard_prices = None
		self.spu_id = None
		self.standard_price = None
		self.standard_retail_price = None
		self.trade_type = None

	def getapiname(self):
		return 'taobao.fenxiao.product.add'

	def getMultipartParas(self):
		return ['image']
