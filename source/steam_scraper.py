import scrapy
import time
import csv

from model.item import ItemSteam
from text_utils import TextUtils
from selenium import webdriver
from selenium.webdriver.common.by import By
from scrapy.selector import Selector




# Es crea la classe SteamSpider per a scrapejar fent servir scrapy
class SteamSpider(scrapy.Spider):
    name = 'steam'
    start_urls = ['https://store.steampowered.com/search/?category1=998&page=1&ndl=1']
    textUtils = TextUtils()

# Es defineix l'user agent per a camuflar que s'està scrapejant
    def __init__(self):
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        self.driver = webdriver.Chrome()


# Es comencen a fer les peticions a cadascuna de les pàgines
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers={
                'User-Agent': self.user_agent,
            })

# Es parsegen cadascun dels elements de la pàgina
    def parse(self, response):
        self.driver.get(response.url)
        for game in response.css('.search_result_row'):
            game_id = game.css('a::attr(data-ds-appid)').get()
            title = game.css('.title::text').get().strip()
            price = game.css('.search_price::text').get().strip()
            try:
                review_data = game.css('.search_review_summary').attrib['data-tooltip-html'].strip()
            except:
                review_data = None
            released = game.css('.search_released::text').get()
            discount = game.css('.search_discount span::text').get()
            platforms = game.css('span.platform_img::attr(class)').extract()

            if released is not None:
                released = released.strip()

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

            item = ItemSteam(game_id, title, price, discount, review_score, n_reviews, released, platforms).json()

            '''
            Crawl inside the game to obtain extra info
            '''

            request_single = scrapy.Request('https://store.steampowered.com/app/' + game_id,
                                            callback=self.get_single_game,
                                headers={'User-Agent': self.user_agent},
                                meta={'item': item})

            time.sleep(3)
            yield request_single

        # S'esperen 5 segons entre peticions de diferents pàgines
        time.sleep(5)


        # Es passa a la següent pagina
        next_page = response.css('.search_pagination_right a:contains(">")::attr(href)').get()
        if next_page is not None:
            yield scrapy.FormRequest(
                url=next_page,
                method='GET',
                headers={
                    'User-Agent': self.user_agent
                },
                callback=self.parse
            )
    def get_single_game(self, response):
        self.driver.get(response.url)
        item = response.meta['item']

        '''
        En el cas que se'ns redirigeixi a la pàgina de verificació d'edat, emprarem Selenium per omplir el formulari
        i fer submit. Un cop s'ha fet aquesta acció, el lloc web ja no la demanarà més. Per això se separen els try-catch
        '''
        try:
            age_year = self.driver.find_element(By.ID, "ageYear")
            age_year.send_keys("1990")
        except:
            pass
        '''
        Un cop completat el formulari, cal clicar el botó per enviar la informació i que es mostri la pàgina del joc
        '''
        try:
            self.driver.find_element(By.ID, "view_product_page_btn").click() #Element on es fa click
            time.sleep(3)
            response = Selector(text=self.driver.page_source) #obtenim tot el contingut de la pàgina
        except:
            pass

        time.sleep(2)

        page = response.css(".tablet_grid")
        item['developers'] = page.css('div.dev_row div#developers_list.summary a::text').getall()
        item['genres'] = page.css('div#genresAndManufacturer.details_block span a::text').getall()
        self.write_to_csv(item)

# Es defineix la funció per a escriure cada element a un arxiu .csv
    def write_to_csv(self, item):
        filename = 'dataset/steam_games.csv'
        with open(filename, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['game_id', 'title', 'price', 'discount', 'review_score', 'number_reviews', 'released', 'platforms'
                                                   ,'developers', 'genres'])
            if f.tell() == 0:
                writer.writeheader()
            writer.writerow(item)

# Es defineix una funció per a que el crawler s'aturi i indiqui la raó de l'aturada
    def closed(self, reason):
        self.driver.quit()
        self.log('Spider closed: ' + reason)
