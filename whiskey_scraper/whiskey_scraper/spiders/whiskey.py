import scrapy
from whiskey_scraper.items import WhiskeyItem
from scrapy.loader import ItemLoader
from scrapy_playwright.page import PageMethod


class WhiskeySpider(scrapy.Spider):
    name= "whiskey"

    def log_error(self, failure):
        self.logger.error(repr(failure))

    def start_requests(self):
        yield scrapy.Request("https://bottleraiders.com/archive/?variety=whiskey", meta={"playwright": True}, callback=self.scrape_page_count)

    def scrape_page_count(self, response):
        page_count_string = response.css('span#page-info div::text').extract()
        string_list = page_count_string[1].split(' ')
        pagination_total = string_list[-1]
        print(pagination_total)
        
        start_urls = ["https://bottleraiders.com/archive/?pg=" + str(x) + "&variety=whiskey" for x in range(1, int(pagination_total))]

        for url in start_urls :
            yield scrapy.Request(url, meta={"playwright": True}, callback=self.parse, errback=self.log_error)

    def parse(self, response):
        whiskey_links = response.css('table#table tbody tr.o-archive__table-row a')
        yield from response.follow_all(whiskey_links, callback=self.parse_whiskey, errback=self.log_error)

    def parse_whiskey(self, response):
        i = ItemLoader(item=WhiskeyItem(), selector=response)

        i.add_css('name', '[class="c-spirit-entry__heading o-spirit-entry__heading"]')
        i.add_css('category', '[class="c-article-category-label"]')
        i.add_css('distiller', '[class="o-spirit-stat-list-item o-spirit-stat_distiller"] p')
        i.add_css('bottler', '[class="o-spirit-stat-list-item o-spirit-stat_bottler"] p')
        i.add_css('abv', '[class="o-spirit-stat-list-item o-spirit-stat_abv"] p')
        if not i.get_output_value('abv'):
            i.add_value('abv', '')
        
        i.add_css('age', '[class="o-spirit-stat-list-item o-spirit-stat_age"] p')
        if not i.get_output_value('age'):
            i.add_value('age', '')
        
        
        i.add_css('srp', '[class="o-spirit-stat-list-item o-spirit-stat_price"] span:nth-child(2)')
        if not i.get_output_value('srp'):
            i.add_value('srp', '')

        i.add_css('description', '[class="o-spirit-intro o-spirit-house-review-value"]')
        if not i.get_output_value('description'):
            i.add_value('description', '')

        i.add_value('img', '')

        yield i.load_item()
