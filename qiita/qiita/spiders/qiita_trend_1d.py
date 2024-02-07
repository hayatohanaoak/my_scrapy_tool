import scrapy


class QiitaTrend1dSpider(scrapy.Spider):
    name = "qiita_trend_1d"
    allowed_domains = ["qiita.com"]
    start_urls = ["https://qiita.com"]

    def parse(self, response):
        category = response.css('a.style-b0kkq6::text').getall()          # トレンド
        titles   = response.css('article > h2 > a::text').getall()        # 記事タイトル
        urls     = response.css('article > h2 > a::attr(href)').getall()  # 記事URL

        """
        category = response.xpath('//nav/div/a[3]/text()').getall()       # トレンド
        titles   = response.xpath('//article/h2/a/text()').getall()       # 記事タイトル
        urls     = response.xpath('//article/h2/a/@href').getall()        # 記事URL
        """

        yield {
            'category': category,
            'titles'  : titles,
            'urls'    : urls
        }
