import scrapy

url = 'https://www.goodreads.com/quotes/tag/success'


class dailyQuotes(scrapy.Spider):
    name = 'getQuotes'
    start_urls = [url]
    def parse(self,response):
        
        filename = f'quotes.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log   (f'Save file {filename}')
        page = response.css('em.current::text').get()
        for q in response.css('div.quote.mediumText'):
            yield{
                'page': int(page),
                'text': q.css('div.quoteText::text').get(),
                'author': q.css('div.quoteText span.authorOrTitle::text').get(),
                'tags': q.css('div.greyText.smallText.left a::text').getall(),
              }
        next_page = response.css('a.next_page::attr(href)').get()
        if int(page)<5:
            yield response.follow(next_page, callback=self.parse)
        else:
            f.close()

