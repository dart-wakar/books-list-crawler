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
            'title': response.css('h1.bookTitle::text').extract_first(),
            'book_cover_url': response.css('div.bookCoverPrimary img').xpath('@src').extract_first(),
            'author': response.css('a.authorName span::text').extract_first(),
            'book_description': response.css('div[id="description"] span[style="display:none"]::text').extract(),
            'book_format_type': response.css('span[itemprop="bookFormatType"]::text').extract_first(),
            'number_of_pages': response.css('span[itemprop="numberOfPages"]::text').extract_first(),
            'publish_info': response.css('div[id="details"] div.row::text')[1].extract(),

        }

    def parse(self,response):
        for i in range(0,len(data)):
            next_page = data[i]['goodreads_book_url']
            if next_page is not None:
                yield response.follow(next_page, callback=self.nextparse)
