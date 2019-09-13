# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# 二手房的item文件设置
class EsfItem(scrapy.Item):
    # 省份
    province_name = scrapy.Field()
    # 城市名称
    city_name = scrapy.Field()
    # 房屋标签
    esf_name = scrapy.Field()
    # 房屋地址
    esf_addr = scrapy.Field()
    # 房屋总价
    esf_total_price = scrapy.Field()
    # 房屋单价
    esf_unit_price = scrapy.Field()
    # 房屋链接
    esf_link = scrapy.Field()
    # 房屋样式
    esf_styles = scrapy.Field()


# 租房的item文件设置
class ZfItem(scrapy.Item):
    # 省份
    province_name = scrapy.Field()
    # 城市名称
    city_name = scrapy.Field()
    # 租房标签
    zf_name = scrapy.Field()
    # 租房链接
    zf_link = scrapy.Field()
    # 租房区域位置
    zf_area = scrapy.Field()
    # 租房小区位置
    zf_club = scrapy.Field()
    # 租房价格
    zf_price = scrapy.Field()
    # 租房样式
    zf_style = scrapy.Field()
    # 租房大小
    zf_size = scrapy.Field()