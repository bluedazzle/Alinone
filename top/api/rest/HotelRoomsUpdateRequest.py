'''
Created by auto_sdk on 2014-11-09 14:51:18
'''
from top.api.base import RestApi
class HotelRoomsUpdateRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.gid_room_quota_map = None
		self.multi_room_quotas = None

	def getapiname(self):
		return 'taobao.hotel.rooms.update'
