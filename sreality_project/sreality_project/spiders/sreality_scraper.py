import scrapy

class SrealityScraper(scrapy.Spider):
    name = 'sreality_scraper'
    start_urls = ['https://www.sreality.cz/hledani/prodej/byty']

    def parse(self, response):
        ads = response.css('.c-list-products .c-product')

        for ad in ads[:500]:
            title = ad.css('.c-product__title .c-product__title-link::text').get()
            image_url = ad.css('.c-product__image img::attr(src)').get()

            yield {
                'title': title,
                'image_url': image_url,
            }
