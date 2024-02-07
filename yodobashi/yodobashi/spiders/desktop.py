import scrapy
import logging


class DesktopSpider(scrapy.Spider):
    name = "desktop"
    allowed_domains = ["www.yodobashi.com"]
    start_urls = ["https://www.yodobashi.com/category/19531/?searchbtn=true&word=%E3%83%87%E3%82%B9%E3%82%AF%E3%83%88%E3%83%83%E3%83%97%E3%83%91%E3%82%BD%E3%82%B3%E3%83%B3"]

    def parse(self, response):
        #products = response.xpath('//div[contains(@class, "productListTile")]') # 講座方式
        #products = response.xpath('//*[@id="listContents"]/div[4]/div')         # 花岡方式
        products = response.css('div.productListTile')                          # 花岡・講座方式共通
        for product in products:
            # もしselectorオブジェクト（）
            #maker = product.xpath('//div[contains(@class, "pName")]/p[1]/text()').get() # 講座方式
            #maker = product.xpath('//a/div[2]/p[1]/text()').get()                       # 花岡方式
            maker = product.css('div.pName > p:nth-child(1)::text').get()               # 花岡・講座方式共通
            
            #name = product.xpath('//div[contains(@class, "pName")]/p[2]/text()').get() # 講座方式
            #name = product.xpath('//a/div[2]/p[2]/text()').get()                       # 花岡方式
            #name = product.css('div.pName > p + p::text').get()                         # 講座方式
            name = product.css('div.pName > p:nth-child(2)::text').get()               # 花岡方式
            
            #price = product.xpath('//span[@class="productPrice"]').get()                            # 講座方式
            #price = product.xpath('//*[@id="listContents"]/div/div/div/ul/li[2]/span/text()').get() # 花岡方式
            #price = product.css('span.productPrice::text').get()                                    # 講座方式
            price = product.css('div.pInfo > ul > li:nth-child(2) > span::text').get()              # 花岡方式
            
            #next = response.xpath('//a[@class="next"]/@href').get()                # 講座方式
            #next = response.xpath('//li[9]/a/span/@href').get()                    # 花岡方式
            next = response.css('a.next::attr(href)').get()                        # 講座方式

            yield{
                'maker': maker,
                'name' : name,
                'price': price,
            }
        # 次のページへ遷移
        next_page = response.css('a.next::attr(href)').get()   # タグのリンク（相対）
        #url       = f'https://www.yodobashi.com/{next_page}'   # 絶対URLに変換
        #next_page = response.css('a.next')
        if next_page:
            #yield scrapy.Request(url=url, callback=self.parse)           # 絶対URLを引数に渡す
            #yield response.follow(url=next_page[0], callback=self.parse) # aタグを引数に渡す
            yield response.follow(url=next_page, callback=self.parse)    # 相対URLを引数に渡す