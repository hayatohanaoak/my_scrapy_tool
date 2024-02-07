import scrapy
import re

class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/catalogue/category/books/fantasy_19/index.html"]

    def parse(self, response):
        "category:fantasyの全冊に対し、一冊一冊詳細ページをたどる"
        urls   = response.css('h3 > a::attr(href)').getall()
        for detail_url in urls:
            yield response.follow(url=detail_url, callback=self.scrape_detail_page)
        
        next_page = response.css('li.next > a::attr(href)').get()
        if next_page:
            yield response.follow(url=next_page, callback=self.parse)
    
    def scrape_detail_page(self, response):
        "詳細ページから、本の情報を取得"
        review = response.css('div.product_main > p.star-rating::attr(class)').get()
        stock  = response.css('tr:nth-child(6) > td::text').get()
        yield {
            'tilte'            : response.css('div.product_main > h1::text').get(),
            'price'            : response.css('div.product_main > p.price_color::text').get(),
            'stock'            : re.search('([0-9]+)', stock).group(1), # 数だけ取得
            'review'           : review.replace('star-rating ', ''),    # 星の数だけ取得
            'upc'              : response.css('tr:nth-child(1) > td::text').get(),
            'number of reviews': response.css('tr:nth-child(7) > td::text').get()
        }
