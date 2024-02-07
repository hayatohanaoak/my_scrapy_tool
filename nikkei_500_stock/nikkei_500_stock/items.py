# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join
import re
import unicodedata

class Nikkei500StockItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def convert_int(val):
    return int(val) if re.match('[0-9]+', val) else 0

def exclusion_str(val):
    return re.sub('円|株|％|倍|,|：|:', '', val)

def sanitize_space(val):
    return re.sub('\s', '', val)

def full_to_half(val):
    return unicodedata.normalize('NFKC', val)

class NikkeiItem(scrapy.Item):
    code     = scrapy.Field(
        input_processor  = MapCompose(sanitize_space, exclusion_str, convert_int),
        output_processor = TakeFirst()
    )
    name     = scrapy.Field(
        input_processor  = MapCompose(full_to_half),
        output_processor = TakeFirst()
    )
    now      = scrapy.Field(
        input_processor  = MapCompose(sanitize_space, exclusion_str),
        output_processor = TakeFirst()
    )
    yen_comp = scrapy.Field(
        input_processor  = MapCompose(sanitize_space, exclusion_str, full_to_half),
        output_processor = TakeFirst()
    )
    start    = scrapy.Field(
        input_processor  = MapCompose(sanitize_space, exclusion_str),
        output_processor = TakeFirst()
    )
    sup      = scrapy.Field(
        input_processor  = MapCompose(sanitize_space, exclusion_str),
        output_processor = TakeFirst()
    )
    inf      = scrapy.Field(
        input_processor  = MapCompose(sanitize_space, exclusion_str),
        output_processor = TakeFirst()
    )
    sell     = scrapy.Field(
        input_processor  = MapCompose(sanitize_space, exclusion_str, convert_int),
        output_processor = TakeFirst()
    )
    per      = scrapy.Field(
        input_processor  = MapCompose(sanitize_space, exclusion_str),
        output_processor = TakeFirst()
    )
    dividend = scrapy.Field(
        input_processor  = MapCompose(exclusion_str),
        output_processor = TakeFirst()
    )