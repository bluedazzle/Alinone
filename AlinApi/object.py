class SenderInfo(object):
    """docstring for SenderInfo"""
    def __init__(self):
        self.__merchant_id = ""
        self.__merchant_name = ""
        self.__sended = 0

    """propety"""
    def getMerchantId(self):
        return self.__merchant_id
    def setMerchantId(self, value):
        self.__merchant_id = value
    MerchantId = property(getMerchantId, setMerchantId, "Property MerchantId")

    def getMerchantName(self):
        return self.__merchant_name
    def setMerchantName(self, value):
        self.__merchant_name = value
    MerchantName = property(getMerchantName, setMerchantName, "Property MerchantName")

    def getSended(self):
        return self.__sended
    def setSended(self, value):
        self.__sended = value
    Sended = property(getSended, setSended, "Property Sended")


class Order(object):
    """docstring for Order"""
    def __init__(self):
        self.__order_id = ""

    """propety"""
    def getOrderId(self):
        return self.__order_id
    def setOrderId(self, value):
        self.__order_id = value
    OrderId = property(getOrderId, setOrderId, "Property OrderId")

