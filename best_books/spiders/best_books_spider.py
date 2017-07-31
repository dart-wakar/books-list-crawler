import scrapy

class BestBooksSpider(scrapy.Spider):
    name = 'bestbooks'
    start_urls = [
        'https://www.goodreads.com/list/show/5',
    ]

    def parse(self,response):
        table = response.css('table.tableList')
        for book_row in table.css('tr'):
            sr_no = book_row.css('td.number::text').extract_first()
            td_img = book_row.css('td')[1]
            book_id = td_img.css('div.u-anchorTarget').xpath('@id').extract_first()
            book_url = td_img.css('a').xpath('@href').extract_first()
            book_image_url = td_img.css('img').xpath('@src').extract_first()
            td_book_info = book_row.css('td')[2]
            book_title_link = td_book_info.css('a.bookTitle')
            book_title = book_title_link.css('span::text').extract_first()
            author_link = td_book_info.css('a.authorName')
            author = author_link.css('span::text').extract_first()
            author_url = author_link.xpath('@href').extract_first()
            ratings_info = td_book_info.css('span.minirating::text').extract_first()
            score_info_container = td_book_info.css('div')
            score_text = score_info_container.css('a::text')[0].extract()
            #number_of_user_voted = score_info_container('a::text')[1].extract()
            yield {
                'sl_no': sr_no,
                'goodreads_book_id': book_id,
                'goodreads_book_url': book_url,
                'book_image_url': book_image_url,
                'book_title': book_title,
                'author': author,
                'goodreads_author_url': author_url,
                'goodreads_ratings_info': ratings_info,
                'goodreads_score': score_text,
                #'number_of_user_voted': number_of_user_voted,
            }

        next_page = response.css('a.next_page').xpath('@href').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
