import scrapy

class GetTrendsSpider(scrapy.Spider):
    name = "get_trends"
    allowed_domains = ["news.yahoo.co.jp"]
    start_urls = ["https://news.yahoo.co.jp"]

    def parse(self, response):
        # yahooニュースのトレンドのタイトルとurlを取得
        titles = response.css('#uamods-topics > div > div > div > ul > li > a::text').getall()
        urls   = response.css('#uamods-topics > div > div > div > ul > li > a::attr(href)').getall()
        # 取得した要素1つ1つで繰り返し処理
        for title, url in zip(titles, urls):
            # 返り値は、yieldの後ろにdict型で定める
            yield {
                'trend_text': title,    # トレンドの見出し取得
                'trend_url' : url       # トレンドのURLを取得
            }