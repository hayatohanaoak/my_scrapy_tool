import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class LuxuryWatchSpider(scrapy.Spider):
    name = "luxury_watch"

    # 初回リクエストのメソッドを上書き
    def start_requests(self):
        yield SeleniumRequest(
            url='https://antenna.jp/',
            wait_time=3,
            screenshot=False,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        # 検索欄に「高級時計」を入力して、検索
        driver.find_element(By.ID, 'search-input').send_keys('高級時計')
        driver.find_element(By.ID, 'search-button').click()
        time.sleep(3)
        
        # 画面スクロールして、WebページのJavaScriptスクロールイベントを発火
        for i in range(15):
            # bodyタグの要素上で、「endキー」を押す（スクロールする）
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            time.sleep(1)
        
        # JavaScriptを使って、画面サイズを変更
        width  = driver.execute_script('return document.body.scrollWidth')
        height = driver.execute_script('return document.body.scrollHeight')
        driver.set_window_size(width, height)
        
        # 検索結果画面のソースコードを、ScrapyのSelectorオブジェクトに変換
        selector = Selector(text=driver.page_source)
        
        # 検索結果にある時計の各フィールドごとに、繰り返し処理
        watches = selector.css('div.article-view.feed-article-view.album-article')
        for watch in watches:
            yield {
                'title': watch.css('div.title::text').get(),
                'url'  : watch.css('a.thumbnail-content::attr("href")').get()
            }