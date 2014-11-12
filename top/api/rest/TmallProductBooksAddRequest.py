'''
Created by auto_sdk on 2014-11-09 14:51:18
'''
from top.api.base import RestApi
class TmallProductBooksAddRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.abstract_msg = None
		self.app_info = None
		self.author = None
		self.author_area = None
		self.bar_code = None
		self.book_bind = None
		self.book_size = None
		self.book_version = None
		self.catalog = None
		self.category_id = None
		self.china_classify_no = None
		self.cip = None
		self.commentator = None
		self.custom_id = None
		self.deputy_name = None
		self.drawor = None
		self.editor = None
		self.graphor = None
		self.image = None
		self.isbn = None
		self.item_ids = None
		self.narrator = None
		self.part_name = None
		self.part_no = None
		self.plottor = None
		self.price = None
		self.publish_company = None
		self.publish_ym = None
		self.regin_year = None
		self.scholisat = None
		self.series_books_name = None
		self.spu_img = None
		self.summary = None
		self.translator = None

	def getapiname(self):
		return 'tmall.product.books.add'

	def getMultipartParas(self):
		return ['image']
