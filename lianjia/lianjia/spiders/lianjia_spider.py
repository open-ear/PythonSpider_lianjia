# -*- coding: utf-8 -*-
import scrapy
import re
from lianjia.items import EsfItem,ZfItem

class LianjiaSpiderSpider(scrapy.Spider):
    name = 'lianjia_spider'
    allowed_domains = ['lianjia.com']
    start_urls = ['https://www.lianjia.com/city/']

    def parse(self, response):
        # 对于列表页的地址进行获取和再构造
        # 1.获取所有的省份信息
        provinces = response.xpath("//div[@class='city_province']")
        for province in provinces:
            # 2.获取省份下的所有城市信息
            province_name = province.xpath(".//div[@class='city_list_tit c_b']//text()").get()
            citys = province.xpath(".//ul//li")
            # 3.获取城市下的具体信息（城市名称和城市的首页连接）
            for city in citys:
                city_name = city.xpath(".//text()").get()
                city_url = city.xpath(".//a//@href").get()
                # print("province:%s"%province_name)
                # print("city:%s"%city_name)
                # print("city_url:%s"%city_url)
                # 4.构建二手房和租房页的链接(新房信息不全）
                city_esf_url = city_url + "ershoufang/"
                city_zf_url  = city_url + "zufang/"
                # print("esf:%s" % city_esf_url)
                # print("zf:%s" % city_zf_url)
                yield scrapy.Request(url=city_esf_url,callback=self.parse_esf,meta={"info":(province_name,city_name)})
                yield scrapy.Request(url=city_zf_url,callback=self.parse_zf,meta={"info":(province_name,city_name)})
                # break
            # break


    def parse_esf(self,response):
        # 获取对于二手房响应并进行数据的提取
        province_name,city_name = response.meta.get("info")

        lis = response.xpath("//ul[@class='sellListContent']//li")
        # 1.获取每一个二手房源信息
        for li in lis:
            # 增加对于动态广告栏的判断
            if li.xpath(".//@class").get() == "list_app_daoliu":
                continue
            # 2.在二手房主页获取具体的房屋信息
            infos = li.xpath(".//div[@class='info clear']")
            esf_name = infos.xpath(".//div[@class='title']//text()").get()
            esf_link = infos.xpath(".//div[@class='title']//a//@href").get()
            esf_addrs = infos.xpath(".//div[@class='address']//text()").getall()
            try:
                esf_addr = esf_addrs[0]
            esf_styles = "".join(esf_addrs[1])
            esf_styles = re.sub(r'\s',"",esf_styles)
            esf_total_price = infos.xpath(".//div[@class='totalPrice']//text()").getall()
            esf_total_price = "".join(esf_total_price)
            esf_unit_price = infos.xpath(".//div[@class='unitPrice']//text()").get()
            esf_unit_price = re.sub(r"单价","",esf_unit_price)
            # 3.将获取的信息保存至item对象中
            item = EsfItem()
            item["province_name"] = province_name
            item["city_name"] = city_name
            item["esf_name"] = esf_name
            item["esf_link"] = esf_link
            item["esf_addr"] = esf_addr
            item["esf_total_price"] = esf_total_price
            item["esf_unit_price"] = esf_unit_price
            item["esf_styles"] = esf_styles
            # 4.返回item对象，交由pipelines文件进行处理
            yield item

        # 5.获取下一页的地址，进行下一页的爬取：
        page = response.xpath("//div[@class='page-box house-lst-page-box']//@page-data").get()
        page = eval(page)
        next_url = response.urljoin("/ershoufang/pg%d/" % (page["curPage"]+1))
        # print(next_url)
        # print(page["curPage"])
        if page["curPage"] <= page["totalPage"]:
            # 6.向下一页发送请求，继续当前方法内的操作
            yield scrapy.Request(url=next_url,callback=self.parse_esf,meta={"info":(province_name,city_name)})

    def parse_zf(self,response):
        """对于租房页面的数据提取"""

        # 创建item对象
        item = ZfItem()
        province_name, city_name = response.meta.get("info")
        item["province_name"] = province_name
        item["city_name"] = city_name
        # 1.获取所有的div标签
        divs = response.xpath("//div[@class='content__list--item']")
        # 2.获取租房房源的细节信息
        for div in divs:
            item["zf_name"] = div.xpath(".//p[@class='content__list--item--title twoline']/a/text()").get()
            zf_link = div.xpath(".//p[@class='content__list--item--title twoline']/a/@href").get()
            # 对于链接的处理，补充域名
            item["zf_link"] = response.urljoin(zf_link)
            item["zf_area"] = div.xpath(".//p[@class='content__list--item--des']//a[1]//text()").get()
            item["zf_club"] = div.xpath(".//p[@class='content__list--item--des']//a[last()]//text()").get()
            zf_style_content = div.xpath(".//p[@class='content__list--item--des']//text()").getall()
            zf_style_content = ("").join(zf_style_content)
            zf_style_contents = zf_style_content.split("/")
            item["zf_size"] = re.sub(r"\s","",zf_style_contents[1])
            item["zf_style"] = re.sub(r"\s","",zf_style_contents[3])
            zf_price = div.xpath(".//span[@class='content__list--item-price']//text()").getall()
            zf_price = "".join(zf_price)
            item["zf_price"] = re.sub(r"\s","",zf_price)
            yield item
        next_url = response.xpath("//div[@class='content__pg']//a[@class='next']//@href").get()
        next_url = response.urljoin(next_url)
        if next_url:
            yield scrapy.Request(url=next_url,callback=self.parse_zf,meta={"info":(province_name,city_name)})
