# -*- coding:utf-8 -*-

"""
For different ITEM's factory
TODO: Customizable extension Using name=cls.
"""
import re

__all__ = ["regex"]

# PoiList
class PoiId:
    id = '(?<=poiId":)[0-9]+'

    def __init__(self, source):
        self.__pattern = re.compile(PoiId.id)
        self.source = source
    
    @property
    def get(self)-> list:
        return re.findall(self.__pattern, self.source)

class Title:
    title = '(?<=title":")[^"]+'

    def __init__(self, source):
        self.__pattern = re.compile(Title.title)
        self.source = source

    @property
    def get(self)-> list:
        return re.findall(self.__pattern, self.source)

class AvgScore:
    avgScore = '(?<="avgScore":)\d[.\d]*'

    def __init__(self, source):
        self.__pattern = re.compile(AvgScore.avgScore)
        self.source = source

    @property
    def get(self)-> list:
        return re.findall(self.__pattern, self.source)

class AllcommentNum:
    allcommentNum = '(?<="allCommentNum":)\d+'

    def __init__(self, source):
        self.__pattern = re.compile(AllcommentNum.allcommentNum)
        self.source = source
    
    @property
    def get(self)-> list:
        return re.findall(self.__pattern, self.source)

class Address:
    address = '(?<="address":")(.+?)(?=")'

    def __init__(self, source):
        self.__pattern = re.compile(Address.address)
        self.source = source
    
    @property
    def get(self)-> list:
        return re.findall(self.__pattern, self.source)

class AvgPrice:
    avgPrice = '(?<="avgPrice":)\d+[.\d]*'

    def __init__(self, source):
        self.__pattern = re.compile(AvgPrice.avgPrice)
        self.source = source
    
    @property
    def get(self)-> list:
        return re.findall(self.__pattern, self.source)

# detailInfo
class Phone:
    phone = '(?<="phone":")\d+[-]?\d+[/\d]+'
    
    def __init__(self, source):
        self.__pattern = re.compile(Phone.phone)
        self.source = source
    
    @property
    def get(self)-> list:
        return re.findall(self.__pattern, self.source)

class OpenTime:
    openTime = '(?<="openTime":")(.+?)(?=")'
    
    def __init__(self, source):
        self.__pattern = re.compile(OpenTime.openTime)
        self.source = source
    
    @property
    def get(self)-> list:
        return re.findall(self.__pattern, self.source)

class ExtraInfos:
    extraInfos = '(?<="text":")(.+?)(?="})'
    
    def __init__(self, source):
        self.__pattern = re.compile(ExtraInfos.extraInfos)
        self.source = source
    
    @property
    def get(self)-> list:
        return re.findall(self.__pattern, self.source)

class Longitude:
    longitude = '(?<="longitude":)\d+[.]?\d+'
    
    def __init__(self, source):
        self.__pattern = re.compile(Longitude.longitude)
        self.source = source
    
    @property
    def get(self)-> list:
        return re.findall(self.__pattern, self.source)

class Latitude:
    latitude = '(?<="latitude":)\d+[.]?\d+'
    
    def __init__(self, source):
        self.__pattern = re.compile(Latitude.latitude)
        self.source = source
    
    @property
    def get(self)-> list:
        return re.findall(self.__pattern, self.source)

class BrandId:
    brandId = '(?<="phone":")\d+[-]?\d+[/\d]+'
    
    def __init__(self, source):
        self.__pattern = re.compile(BrandId.brandId)
        self.source = source
    
    @property
    def get(self)-> list:
        return re.findall(self.__pattern, self.source)

class BrandName:
    brandName = '(?<="phone":")\d+[-]?\d+[/\d]+'
    
    def __init__(self, source):
        self.__pattern = re.compile(BrandName.brandName)
        self.source = source
    
    @property
    def get(self)-> list:
        return re.findall(self.__pattern, self.source)

class ReFactory():
    """ 
    @param id title score comnum addr price 
            phone optime exinfo longitude latitude brandid brandname
    """

    def __init__(self, name, source):
        self.__d = {\
            'ID': PoiId,
            'TITLE': Title,
            'SCORE': AvgScore,
            'COMNUM': AllcommentNum,
            'ADDR': Address,
            'PRICE': AvgPrice,
            'PHONE': Phone,
            'OPTIME': OpenTime,
            'EXINFO': ExtraInfos,
            'LONGITUDE': Longitude,
            'LATITUDE': Latitude,
            'BRANDID': BrandId,
            'BRANDNAME': BrandName
            }
        self.name = name
        self.source = source

    def __parse(self):
        try:
            if  self.name in self.__d.keys():
                return self.__d[ self.name](self.source).get
            else:
                raise ValueError("Name was not found!")
        except: # ifnot parse sucessfully, just ignore
            pass

    @classmethod
    def process(cls, name: str, source, *args, **kwargs) -> list:
        #""" TODO: 可自定义处理函数的扩充"""
        """ 
            @item:  proId title  avgScore  address allCommentNum avgPrice 

            @param: id    title  score     addr    comnum        price    

            @item: phone openTime extraInfos longitude latitude brandId brandName

            @param phone optime   exinfo     longitude latitude brandid brandname
        """
        name = name.upper()
        self = cls(name, source)
        return self.__parse()

regex = ReFactory.process