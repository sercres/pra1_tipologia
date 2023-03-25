import scrapy
import time
import csv

# Es crea la classe SteamSpider per a scrapejar fent servir scrapy
class SteamSpider(scrapy.Spider):
    name = 'steam'
    start_urls = ['https://store.steampowered.com/search/?sort_by=_ASC&category1=998&page=1']

# Es defineix l'user agent per a camuflar que s'està scrapejant
# Revisar si l'user agent és vàlid o no 
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
            title = game.css('.title::text').get().strip()
            price = game.css('.search_price::text').get().strip()
            review = game.css('.search_review_summary::text').get().strip()
            released = game.css('.search_released::text').get().strip()
            discount = game.css('.search_discount::text').get()
            if discount:
                discount = discount.strip()

            item = {
                'title': title,
                'price': price,
                'discount': discount,
                'review': review,
                'released': released
            }
            yield item
            self.write_to_csv(item)

# S'esperen 5 segons entre peticions de diferents pàgines
        time.sleep(5) # Wait for 5 seconds between requests

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
            writer = csv.DictWriter(f, fieldnames=['title', 'price', 'discount', 'review', 'released'])
            if f.tell() == 0:
                writer.writeheader()
            writer.writerow(item)

# Es defineix una funció per a que el crawler s'aturi i indiqui la raó de l'aturada
    def closed(self, reason):
        self.log('Spider closed: ' + reason)