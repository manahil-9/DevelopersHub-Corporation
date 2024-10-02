


##  STEP 2: WEB SCRAPING USING SCRAPY ##

import scrapy

class BooksSpider(scrapy.Spider):
    name = 'books'
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        for book in response.css('.product_pod'):
            title = book.css('h3 a::attr(title)').get()
            price = book.css('.price_color::text').get()
            availability = book.css('.availability::text').get().strip()

            # Output the scraped data
            yield {
                'Title': title,
                'Price': price,
                'Availability': availability,
            }

        # Follow pagination links to scrape the next page
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
