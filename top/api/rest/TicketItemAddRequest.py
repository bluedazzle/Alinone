'''
Created by auto_sdk on 2014-11-09 14:51:18
'''
from top.api.base import RestApi
class TicketItemAddRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.auction_point = None
		self.auction_status = None
		self.city = None
		self.description = None
		self.etc_association_status = None
		self.etc_auto_refund = None
		self.etc_merchant_id = None
		self.etc_merchant_nick = None
		self.etc_network_id = None
		self.etc_overdue_pay = None
		self.etc_verification_pay = None
		self.have_invoice = None
		self.image_1 = None
		self.image_2 = None
		self.image_3 = None
		self.image_4 = None
		self.image_5 = None
		self.list_time = None
		self.postage_id = None
		self.product_id = None
		self.promoted_status = None
		self.prov = None
		self.shop_cats = None
		self.skus = None
		self.sub_stock_at_buy = None
		self.title = None
		self.video_id = None
		self.vip_promoted = None

	def getapiname(self):
		return 'taobao.ticket.item.add'

	def getTranslateParas(self):
		return {'etc_verification_pay':'etc.verification_pay','etc_merchant_nick':'etc.merchant_nick','etc_network_id':'etc.network_id','etc_overdue_pay':'etc.overdue_pay','etc_auto_refund':'etc.auto_refund','etc_merchant_id':'etc.merchant_id','etc_association_status':'etc.association_status'}
