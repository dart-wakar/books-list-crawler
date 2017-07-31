import scrapy
import json

with open('books.json') as data_file:
    data = json.load(data_file)

class BooksDetailsSpider(scrapy.Spider):
    name = 'booksdetails'
    start_urls = [
        'https://goodreads.com'+data[0]['goodreads_book_url']
    ]

    def nextparse(self,response):
        yield {
            'title': response.css('h1.bookTitle::text').extract_first()
        }

    def parse(self,response):
        for i in range(0,len(data)):
            
            next_page = data[i]['goodreads_book_url']
            if next_page is not None:
                yield response.follow(next_page, callback=self.nextparse)
