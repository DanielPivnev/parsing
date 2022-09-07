import scrapy
from scrapy_splash import SplashRequest


class Lesson6Spider(scrapy.Spider):
    name = 'lesson_6'
    allowed_domains = ['scrapingclub.com']
    # start_urls = ['https://scrapingclub.com/exercise/detail_sign/']

    script = '''
        function main(splash, args)
            assert(splash:go(args.url))
            assert(splash:wait(0.5))
            return {
                html = splash:html()
            }
        end
    '''

    def start_requests(self):
        yield SplashRequest(
            url='https://scrapingclub.com/exercise/detail_sign/',
            callback=self.parse,
            endpoint='execute',
            args={
                'lua_source': self.script
            }
        )

    def parse(self, response):
        img = response.urljoin(response.xpath('//img[contains(@class, "card-img-top")]/@src').get())
        price = response.xpath('//h3[@class="card-title"]/following-sibling::h4/text()').get()
        description = response.xpath('//p[@class="card-text"]/text()').get()
        title = response.xpath('//h3[@class="card-title"]/text()').get()

        item = {
            'img': img,
            'price': price,
            'description': description,
            'title': title
        }

        yield item
