import scrapy

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'https://recipes.lewagon.com/',
    ]

    def parse(self, response):
        for recipe in response.css('div.recipe'):
            yield {
                'name': recipe.xpath('a/div/p/text()').get(),
                'time': recipe.xpath('a/div/div/div/small/span/text()').get(),
                'difficulty': recipe.xpath('a/div/div/div/small[2]/span/text()').get(),
            }
            
        next_page = response.css('ul.pagination li.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
