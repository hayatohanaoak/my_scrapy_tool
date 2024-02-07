import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.books import BooksSpider

process = CrawlerProcess(settings=get_project_settings())
process.crawl(BooksSpider)
process.start()