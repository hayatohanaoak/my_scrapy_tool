# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Join
import re

def remake_rating(value: str) -> str:
    return value.replace('star-rating ', '')

def convert_int(value: str) -> int:
    return int(value)

def extract_stock(value: str) -> str:
    if re.match('.*[0-9]+.*', value):
        return re.search('.*([0-9]+).*', value).group(1)


class BooksToScrapeItem(scrapy.Item):
    title      = scrapy.Field(
        input_processor  = MapCompose(str.lstrip),
        output_processor = TakeFirst()
    )
    price      = scrapy.Field(
        input_processor  = MapCompose(str.lstrip),
        output_processor = TakeFirst()
    )
    stock      = scrapy.Field(
        input_processor  = MapCompose(str.lstrip, str.strip, extract_stock, convert_int),
        output_processor = TakeFirst()
    )
    rating     = scrapy.Field(
        input_processor  = MapCompose(str.lstrip, remake_rating),
        output_processor = TakeFirst()
    ) # 出力時の整形
    UPC        = scrapy.Field(
        input_processor  = MapCompose(str.lstrip),
        output_processor = TakeFirst()
    )
    review     = scrapy.Field(
        input_processor  = MapCompose(str.lstrip, convert_int),
        output_processor = TakeFirst()
    )
    image_urls = scrapy.Field() # 画像ファイル用
    img_url    = scrapy.Field(
        output_processor = TakeFirst()
    ) # DB格納用
