import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ProductsSpider(CrawlSpider):
    name = 'products'
    allowed_domains = ['scrapingclub.com']
    start_urls = ['https://scrapingclub.com/exercise/list_basic/']

    rules = (
        Rule(LinkExtractor(
            restrict_xpaths='//div[contains(@class, "row")]/div/div[@class="card"]/a'),
            callback='parse_item',
            follow=True),
        Rule(LinkExtractor(
            restrict_xpaths='//a[contains(string(), "Next")]'),
            follow=True),
    )

    def parse_item(self, response):
        item = {}

        item['title'] = response.xpath('//h3[@class="card-title"]/text()').get()
        item['price'] = response.xpath('//h3[@class="card-title"]/following-sibling::h4/text()').get()
        item['description'] = response.xpath('//p[@class="card-text"]/text()').get()
        item['img'] = response.urljoin(response.xpath('//img[contains(@class, "card-img-top")]/@src').get())

        return item
