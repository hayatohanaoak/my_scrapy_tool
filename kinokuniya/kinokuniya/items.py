# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from itemloaders.processors import TakeFirst, MapCompose, Join
import scrapy
import re

# ¥と,を消して、int型に変換
def remake_price(price):
    return int(re.sub('¥|,', '', price)) if re.match('¥|,', price) else 0

# サイズ B5判／ページ数 435p／高さ 24cm から、サイズを取得する
def get_size(text):
    if text:
        return re.search('\s*.*サイズ (.*)判', text).group(1) if re.match('\s*.*サイズ.*判', text) else '抽出失敗'
    return '取得失敗'

# サイズ B5判／ページ数 435p／高さ 24cm から、ページ数を取得する
def get_page(text):
    if text:
        return int(re.search('\s*.*／ページ数 ([0-9]+).*', text).group(1)) if re.match('\s*.*／ページ数 [0-9]+.*', text) else 0
    return 0

# 商品コード 9784297129163から、コードのみを取得する
def get_code(code):
    return code.replace('商品コード ', '') if code else ''

class KinokuniyaItem(scrapy.Item):
    title     = scrapy.Field(
        input_processor  = MapCompose(str.lstrip),  # データ入力時
        output_processor = Join(' ')                # itemフィールド格納時
    )
    author    = scrapy.Field(
        output_processor = TakeFirst()
    )
    price     = scrapy.Field(
        input_processor  = MapCompose(remake_price),
        output_processor = TakeFirst()
    )
    publisher = scrapy.Field(
        output_processor = TakeFirst()
    )
    size      = scrapy.Field(
        input_processor  = MapCompose(get_size),
        output_processor = TakeFirst()
    )
    page      = scrapy.Field(
        input_processor  = MapCompose(get_page),
        output_processor = TakeFirst()
    )
    code      = scrapy.Field(
        input_processor  = MapCompose(get_code),
        output_processor = TakeFirst()
    )
    image_urls = scrapy.Field() # 画像URL格納先