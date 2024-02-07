import scrapy
from scrapy import FormRequest

class LoginSpider(scrapy.Spider):
    name = "login"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/login"]

    def parse(self, response):
        # csrf_tokenの値を取得
        csrf_token = response.css('input[name="csrf_token"]::attr(value)').get()
        # フォームリクエストの送信（フォーム）
        yield FormRequest.from_response(
            response,
            # formxpath='//form'
            formcss='form',
            formdata={
                'csrf_token': csrf_token,
                'username': 'test',
                'password': 'test'
            },
            callback=self.after_login
        )
    
    def after_login(self, response):
        if response.css('a[href="/logout"]::text').get():
            print('Login success')
        else:
            print('Login failed')