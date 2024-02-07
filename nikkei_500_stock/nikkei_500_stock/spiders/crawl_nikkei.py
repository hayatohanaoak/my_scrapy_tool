import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from nikkei_500_stock.items import NikkeiItem


class CrawlNikkeiSpider(CrawlSpider):
    name = "crawl_nikkei"
    allowed_domains = ["www.nikkei.com"]
    start_urls = ["https://www.nikkei.com/markets/kabu/nidxprice/?StockIndex=N500"]

    rules = (
        # 詳細ページのリンクにアクセスしてスクレイピング。
        Rule(LinkExtractor(restrict_css='td.left > a[href*="/nkd/company"]'), callback="parse_item", follow=False),
        # 「次へ」のボタンを再帰的にたどる
        Rule(LinkExtractor(restrict_css='a:contains("次へ")'), follow=True),
    )
    
    def parse_item(self, response):
        price_detail = response.css('dd.m-stockPriceElm_value::text').getall()
        stock_prices = response.css(
            'div.m-stockInfo_detail.m-stockInfo_detail_01 > div > ul > li > span.m-stockInfo_detail_value::text').getall()
        
        # ItemLoaderに格納
        loader = ItemLoader(item=NikkeiItem(), response=response)
        loader.add_css('code', 'span.m-companyCategory_text::text')
        loader.add_css('name' , 'h1.m-headlineLarge_text::text')
        loader.add_value('now', price_detail[0])
        loader.add_value('yen_comp', price_detail[1])
        loader.add_value('start', stock_prices[0])
        loader.add_value('sup', stock_prices[1])
        loader.add_value('inf', stock_prices[2])
        loader.add_value('sell', stock_prices[3])
        loader.add_value('per', stock_prices[4])
        loader.add_value('dividend', stock_prices[5])
        # Itemsに格納
        return loader.load_item()


