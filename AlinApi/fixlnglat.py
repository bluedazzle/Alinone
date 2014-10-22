import math

class GpsCorrect(object):
    def __init__(self):
        self.__pi = 3.14159265358979324
        self.__a = 6378245.0
        self.__ee = 0.00669342162296594323

    def outofchina(self, lat, lng):
        if lng < 72.004 and lng > 137.8347:
            return True
        if lat < 0.8293 and lat > 55.8271:
            return True
        return False

    def transformLat(self, x, y):
        ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x))
        ret += (20.0 * math.sin(6.0 * x * self.__pi) + 20.0 * math.sin(2.0 * x * self.__pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(y * self.__pi) + 40.0 * math.sin(y / 3.0 * self.__pi)) * 2.0 / 3.0
        ret += (160.0 * math.sin(y / 12.0 * self.__pi) + 320 * math.sin(y * self.__pi / 30.0)) * 2.0 / 3.0
        return ret

    def transformLng(self, x, y):
        ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x))
        ret += (20.0 * math.sin(6.0 * x * self.__pi) + 20.0 * math.sin(2.0 * x * self.__pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(x * self.__pi) + 40.0 * math.sin(x / 3.0 * self.__pi)) * 2.0 / 3.0
        ret += (150.0 * math.sin(x / 12.0 * self.__pi) + 300.0 * math.sin(x / 30.0 * self.__pi)) * 2.0 / 3.0
        return ret

    def transform(self, wglat, wglng):
        latlng = []
        if self.outofchina(wglat, wglng):
            latlng.append(wglat)
            latlng.append(wglng)
            return 0
        dLat = self.transformLat(wglng - 105.0, wglat - 35.0)
        dLon = self.transformLng(wglng - 105.0, wglat - 35.0)
        radLat = wglat / 180.0 * self.__pi
        magic = math.sin(radLat)
        magic = 1 - self.__ee * magic * magic
        sqrtMagic = math.sqrt(magic)
        dLat = (dLat * 180.0) / ((self.__a * (1 - self.__ee)) / (magic * sqrtMagic) * self.__pi)
        dLon = (dLon * 180.0) / (self.__a / sqrtMagic * math.cos(radLat) * self.__pi)
        latlng.append((wglat + dLat))
        latlng.append((wglng + dLon))
        return latlng
