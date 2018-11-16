import scrapy
from spider_ban.items import ProductItem
from spider_ban.utils.helpfunc import clear_html,clear_space_back


class ProductSpider(scrapy.Spider):
    name = "product"

    def start_requests(self):
        url = 'https://www.banggood.com/'
        yield scrapy.Request(url,self.parse)

    def parse(self,response):
        for href in self.parse_cate_link(response):
            yield response.follow(href, self.product_list_parse)

    def parse_cate_link(self, response):
        return response.xpath('//*[@class="cate_sub clothing"]/dl[1]/dd[1]/a[1]/@href').extract()

    def product_list_parse(self, response):
        for href in response.xpath('//*[@class="middle_product_text_170717"]/@href').extract():
            yield response.follow(href, self.product_parse)
        nextpage = response.xpath('//*[@class="bottom_nextPage_button_20161216"]/@href').extract_first()
        if nextpage is not None:
            yield response.follow(nextpage, self.product_list_parse)

    def product_parse(self, response):
        item = ProductItem()
        item['_id'] = response.xpath('//*[@class="productid"]/b/span/text()').extract_first()
        item['url'] = response.request.url
        item['images'] = response.xpath('//*[@class="good_photo_min"]/ul/li/a/@big').extract()
        item['title'] = response.xpath('//*[@itemprop="name"]/text()').extract_first()
        item['rate'] = response.xpath('//*[@itemprop="ratingValue"]/text()').extract_first()
        item['reviews'] = response.xpath('//*[@itemprop="reviewCount"]/text()').extract_first()
        item['sold'] = response.xpath('//*[@id="sold_num"]/text()').extract_first()
        item['price'] = response.xpath('//*[@itemprop="price"]/@content').extract_first()
        item['color'] = response.xpath('//*[@option_id="1"]/a/@title').extract()
        item['size'] = response.xpath('//*[@option_id="2"]/a/@title').extract()
        item['category'] = response.xpath('//*[@property="itemListElement"]/h3/a/span/text()').extract()
        description = response.xpath('//*[@class="good_tabs_box"]/div/ul/li').extract()
        moredes = response.xpath('//*[@class="good_tabs_box"]/div[1]//div//text()').extract()
        item['description'] = clear_html(description) + clear_space_back(moredes)
        yield item

        
        
        