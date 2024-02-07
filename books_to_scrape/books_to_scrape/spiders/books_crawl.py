import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from books_to_scrape.items import BooksToScrapeItem
from scrapy.loader import ItemLoader

class BooksCrawlSpider(CrawlSpider):
    name = "books_crawl"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/catalogue/category/books_1/index.html"]

    rules = (
        # メニューサイドバーのリンクと、その先をたどらない（たどるとしたら、本来たどらない50ページ目までたどってしまう）
        Rule(LinkExtractor(restrict_css='ul.nav.nav-list  li > a[href*=".."]'), follow=False),
        # 各詳細ページにアクセスして、parse_itemでスクレイピング、先はたどらない
        Rule(LinkExtractor(restrict_css='h3 > a'), callback="parse_item", follow=False),
        # 次のページのリンクを、Rulesの頭から再度処理する
        # コールバックなし -> follow=Trueのデフォルト値になっているため
        Rule(LinkExtractor(restrict_css='li.next')),
    )

    def parse_item(self, response):
        items = ItemLoader(item=BooksToScrapeItem(), response=response)
        items.add_css('title', 'div.col-sm-6.product_main > h1::text')
        items.add_css('price', 'div.col-sm-6.product_main > p.price_color::text')
        items.add_css('stock', 'div.col-sm-6.product_main > p.instock.availability::text')
        items.add_css('rating', 'div.col-sm-6.product_main > p.star-rating::attr(class)')
        items.add_css('UPC', 'tr:nth-child(1) > td::text')
        items.add_css('review', 'tr:nth-child(7) > td::text')
        # 画像ファイル用
        items.add_value('image_urls',
            response.urljoin(response.css('div > img::attr(src)').get())
        )
        # DB格納用
        items.add_value('img_url',
            response.urljoin(response.css('div > img::attr(src)').get())
        )
        yield items.load_item()
