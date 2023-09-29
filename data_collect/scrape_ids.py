from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from responses import Response
from db import DB
from utils import item_type_convert

class Scraper:

    def __init__(self, url:str) -> None:
        self.responses = Response()
        self.driver = webdriver.Firefox()
        self.db = DB()
        self.url = url
        self.page = 1
        self.c = 0
        self.recorded_ids = self.db.get_ids()

    def get_url(self):
        self.driver.get(self.url)

    def accept_cookies(self):
        self.driver.find_element(
            By.XPATH, '//*[@id="js-btn-save"]/button[2]'
        ).click()

    def get_items_table_rows(self):
        table = self.driver.find_element(
            By.XPATH, '/html/body/div[2]/center/table/tbody/tr/td/div/form/table[1]/tbody/tr/td/table'
        )
        table_rows = table.find_elements(By.TAG_NAME, 'tr')[1:]
        return table_rows
    
    def parse_rows(self, rows:list[WebElement]):
        for row in rows:
            item_id = row.find_element(By.TAG_NAME, 'a').text
            if item_id in self.recorded_ids:
                continue
            self.c += 1
            print(self.c, item_id)
            info = self.get_item_data(item_id)
            self.insert_to_database(info)

    def next_page(self):
        current_page = self.page
        self.page += 1
        next_page = self.page
        self.url = self.url.replace(f'pg={current_page}', f'pg={next_page}')

    def get_item_data(self, item_id:str):
        info = self.responses.get_response(f'items/SET/{item_id}')
        return info
    
    def insert_to_database(self, info:dict):
        info['type'] = item_type_convert(info['type'])
        self.db.insert_item(info)

        
scraper = Scraper(f'https://www.bricklink.com/catalogList.asp?pg=1&catType=S&catString=65')
scraper.get_url()
scraper.accept_cookies()
while True:
    rows = scraper.get_items_table_rows()
    scraper.parse_rows(rows)

    if len(rows) != 50:
        scraper.driver.close()
        break

    next_page = scraper.next_page()
    scraper.get_url()


