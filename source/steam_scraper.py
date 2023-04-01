import scrapy
import time
import csv
from text_utils import TextUtils


# Es crea la classe SteamSpider per a scrapejar fent servir scrapy
class SteamSpider(scrapy.Spider):
    name = 'steam'
    start_urls = ['https://store.steampowered.com/search/?sort_by=&sort_order=0&category1=998&supportedlang=spanish&page=1']
    textUtils = TextUtils()

# Es defineix l'user agent per a camuflar que s'està scrapejant
    def __init__(self):
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'

# Es comencen a fer les peticions a cadascuna de les pàgines
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers={
                'User-Agent': self.user_agent
            })

# Es parsegen cadascun dels elements de la pàgina
    def parse(self, response):
        for game in response.css('.search_result_row'):
            game_id = game.css('a::attr(data-ds-appid)').get()
            title = game.css('.title::text').get().strip()
            price = game.css('.search_price::text').get().strip()
            review_data = game.css('.search_review_summary').attrib['data-tooltip-html'].strip()
            released = game.css('.search_released::text').get().strip()
            discount = game.css('.search_discount span::text').get()
            platforms = game.css('span.platform_img::attr(class)').extract()

            if review_data:
                nums = self.textUtils.get_numbers_from_string(review_data)
                review_score = nums[0]
                n_reviews = nums[1]
            else:
                review_score = ''
                n_reviews = ''

            if price is None or len(price) == 0:
                price = game.css('.search_price.discounted::text').extract()
                price = self.textUtils.filter_number_from_array(price, '[0-9]{1,2},[0-9]{1,2}', first=True)

            if platforms:
                platforms = self.textUtils.remove_img_text(platforms)

            item = {
                'game_id': game_id,
                'title': title,
                'price': price,
                'discount': discount,
                'review_score': review_score,
                'number_reviews': n_reviews,
                'released': released,
                'platforms': platforms
            }
            yield item
            self.write_to_csv(item)

# Es passa a la següent pagina
        next_page = response.css('.search_pagination_right a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse, headers={
                'User-Agent': self.user_agent
            })

# Es defineix la funció per a escriure cada element a un arxiu .csv
    def write_to_csv(self, item):
        filename = 'steam_games.csv'
        with open(filename, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['game_id', 'title', 'price', 'discount', 'review_score', 'number_reviews', 'released', 'platforms'])
            if f.tell() == 0:
                writer.writeheader()
            writer.writerow(item)

# Es defineix una funció per a que el crawler s'aturi i indiqui la raó de l'aturada
    def closed(self, reason):
        self.log('Spider closed: ' + reason)
