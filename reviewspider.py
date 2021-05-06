from urllib import response

import scrapy


class ReviewspiderSpider(scrapy.Spider):
    name = 'reviewspider'
    allowed_domains = ['www.amazon.com']
    start_urls = ['https://www.amazon.com/Apple-iPhone-256GB-Silver-T-Mobile/product-reviews/B07RV52TRF/ref=cm_cr_dp_d_show_all_btm?/']

    def  parse(self, response):
        star_rating = response.xpath('//span[@class="a-icon-alt"]/text()').extract()

        comments = response.xpath('//span[@class="a-size-base review-text review-text-content"]/span/text()').extract()

        count = 0

        for item in zip(star_rating, comments):
            # create a dictionary to store the scraped info

            scraped_data = {

                'Star Rating': item[0],

                'Rating Text': item[1],

            }

            # yield or give the scraped info to scrapy
            #In the above code, we are adding each item to the Python dictionary.
            #The yield statement returns the scraped data for Scrapy to process and store.
            yield scraped_data

            #next page we use css as a selector t help spider to identifey button of next page
            #class="a-last" a (href=new url for the next page)
            next_page = response.css('.a-last a ::attr(href)').extract_first()
            # if exist
            if next_page:
                #Return multiple Requests and items from a single callback
                yield scrapy.Request(
            #Scrapy allows crawling multiple URLs simultaneously. For this, identify the Base URL and then identify the part of the other URLs that need to join the base URL and append them using urljoin()
                    response.urljoin(next_page),
            # we call the self.parse method for the new URL.
                    callback=self.parse

                )

