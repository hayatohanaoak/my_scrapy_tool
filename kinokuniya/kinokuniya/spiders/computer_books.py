import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from kinokuniya.items import KinokuniyaItem
from scrapy.loader import ItemLoader

class ComputerBooksSpider(CrawlSpider):
    name = "computer_books"
    allowed_domains = ["www.kinokuniya.co.jp"]
    start_urls = ["https://www.kinokuniya.co.jp/f/dsd-101001037028005-06-"]

    rules = (
        Rule(   # 本の詳細をたどる
            #LinkExtractor(restrict_xpaths='//h3[@class="heightLine-2"]/a'),    # 本の詳細URLが入ったXpath
            LinkExtractor(restrict_css='h3.heightLine-2 > a'),                  # 本の詳細URLが入ったcssセレクタ
            callback="parse_item",
            follow=False  # 本の詳細ページの先のリンクはたどらない
        ),
        #Rule(   # 次のページをたどる
        #    #LinkExtractor(restrict_xpaths='//a[contains(text(), "次へ")])[1]'),    # 次ページのURLが入ったXpath
        #    LinkExtractor(restrict_css='a:contains("次へ")'),                       # 次ページのURLが入ったcssセレクタ
        #),
    )

    def parse_item(self, response):
        items = ItemLoader(item=KinokuniyaItem(), response = response)
        items.add_css('title', 'h3[itemprop=name]::text')
        items.add_css('author', 'div.infobox.ml10.mt10 > ul > li:nth-child(1) > a::text')
        items.add_css('price', 'span.sale_price::text')
        items.add_css('publisher', 'a[href*="publisher-key="]::text')
        items.add_css('size', 'div.infbox.dotted.ml10.mt05.pt05 > ul > li:nth-child(1)::text')
        items.add_css('page', 'div.infbox.dotted.ml10.mt05.pt05 > ul > li:nth-child(1)::text')
        items.add_css('code', 'li[itemprop="identifier"]::text')
        items.add_value('image_urls',
            response.urljoin(response.css('img[itemprop="image"]::attr(src)').get())
        ) # 画像URLを絶対パスに変換してItemsに格納
        yield items.load_item()