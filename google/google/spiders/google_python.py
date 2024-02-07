import scrapy
import time
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class GooglePythonSpider(scrapy.Spider):
    name = "google_python"
    # allowed_domains, start_urlsは削除

    # Scrapyが最初にリクエストを送るstart_requests()メソッドを上書き
    def start_requests(self):
        yield SeleniumRequest(
            url='https://www.google.com/?hl=ja',
            wait_time=3,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver'] # ブラウザ操作のためのオブジェクトをdriverに格納
        driver.save_screenshot('01.png') # スクショをとる
        search_ber = driver.find_element(By.CSS_SELECTOR, 'textarea[name="q"]')
        search_ber.send_keys('Python')
        search_ber.send_keys(Keys.ENTER) # Enterキーを押す
        time.sleep(1)
        driver.save_screenshot('02.png')
        wide   = driver.execute_script('return document.body.scrollWidth')  # 画面の横幅をフルに設定
        height = driver.execute_script('return document.body.scrollHeight') # 画面の高さをフルに設定
        driver.set_window_size(wide, height)                                # 設定値の適用
        driver.save_screenshot('03.png')
        # 検索結果のタイトルとURLを取得
        titles = driver.find_elements(By.CSS_SELECTOR, 'h3.LC20lb.MBeuO.DKV0Md')
        urls   = driver.find_elements(
            By.CSS_SELECTOR, 'div > div > div > div > div > div > div > div > span > a[jsname="UWckNb"]'
        )
        for title_elem, url_elem in zip(titles, urls, strict=True):
            if title_elem.text == "": # 「関連する質問」に含まれるデータURLを除外
                continue
            yield {
                't': title_elem.text,
                'u': url_elem.get_attribute('href')
            }