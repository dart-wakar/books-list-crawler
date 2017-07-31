import scrapy
import json

with open('allbooks.json') as data_file:
    data = json.load(data_file)

class BooksDetailsSpider(scrapy.Spider):
    name = 'booksdetails'
    start_urls = [
        'https://goodreads.com'+data[0]['goodreads_book_url']
    ]

    def nextparse(self,response):
        row_titles = response.css('div.infoBoxRowTitle::text').extract()
        row_items = response.css('div.infoBoxRowItem')
        info = {}
        for i in range(0,len(row_titles)):
            if row_titles[i] == 'Original Title':
                row_item = row_items[i].css('div::text').extract_first()
                info[row_titles[i]] = row_item
            elif row_titles[i] == 'ISBN':
                x = ''.join([row_items[i].css('span.greyText::text').extract_first(),row_items[i].css('span[itemprop="isbn"]::text').extract_first()])
                y = u')'
                row_item = ''.join([x,y])
                info[row_titles[i]] = row_item
            elif row_titles[i] == 'Edition Language':
                row_item = row_items[i].css('div::text').extract_first()
                info[row_titles[i]] = row_item
            elif row_titles[i] == 'Characters':
                row_item = row_items[i].css('a::text').extract()
                info[row_titles[i]] = row_item
            elif row_titles[i] == 'setting':
                row_item = row_items[i].css('a::text').extract()
                info[row_titles[i]] = row_item
            elif row_titles[i] == 'Literary Awards':
                row_item = row_items[i].css('a::text').extract()
                info[row_titles[i]] = row_item
            elif row_titles[i] == 'Series':
                row_item = row_items[i].css('a::text').extract_first()
                info[row_titles[i]] = row_item
        yield {
            'title': response.css('h1.bookTitle::text').extract_first(),
            'book_cover_url': response.css('div.bookCoverPrimary img').xpath('@src').extract_first(),
            'author': response.css('a.authorName span::text').extract_first(),
            'book_description': response.css('div[id="description"] span[style="display:none"]::text').extract(),
            'book_format_type': response.css('span[itemprop="bookFormatType"]::text').extract_first(),
            'number_of_pages': response.css('span[itemprop="numberOfPages"]::text').extract_first(),
            'publish_info': response.css('div[id="details"] div.row::text')[1].extract(),
            'info': info,
            'genres_info': response.css('a.bookPageGenreLink::text').extract(),
        }

    def parse(self,response):
        for i in range(0,len(data)):
            next_page = data[i]['goodreads_book_url']
            if next_page is not None:
                yield response.follow(next_page, callback=self.nextparse)
