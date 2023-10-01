import logging
from typing import List, Union
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from datetime import datetime, timedelta
from dataclasses import dataclass


months = {'января': 1, 
          'февраля': 2, 
          'марта': 3, 
          'апреля': 4, 
          'мая': 5, 
          'июня': 6, 
          'июля': 7, 
          'августа': 8, 
          'сентября': 9, 
          'октября': 10, 
          'ноября': 11, 
          'декабря': 12}


@dataclass
class Article:
    title: str
    annotation: str
    publication_time: datetime
    

class YaParser:

    def __init__(self) -> None:
        """
        Запускает браузер Google Chrome с конкретным User Agent, в режиме headless 
        и с отключенными логами
        """
        logging.info('Starting browser...')

        user_agent = '5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        options = webdriver.ChromeOptions()
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument('--headless')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.browser = webdriver.Chrome(options=options)

        logging.info('Browser is started')

    def go_to_page(self, target_url: str) -> None:
        logging.info(f'Going to page {target_url}...')
        self.browser.get(target_url)
        sleep(10)
        logging.info(f'Opened page {self.browser.current_url}')

    def find_all_articles(self) -> Union[List[str], None]:
        """
        Ищет на странице все карточки статей по указанному Xpath, а затем
        для каждого элемента находит дату публикации, заголовок и аннотацию
        и формирует из этого набора датакласс для удобной работы впоследующем.

        Возвращает список из датакласов `Article`
        """
        logging.info('Starting searching for card items...')
        # Пробел после mg-card для того, чтобы найти именно mg-card, а не mg-card_flexible-single
        result = self.browser.find_elements(By.XPATH, "//div[contains(@class, 'mg-card ')]")
        logging.info(f'Finded {len(result)} elements on page. Creating articles...')
        list_of_articles = []
        for element in result:
            publication_time = element.find_element(By.XPATH, ".//div[contains(@class, 'mg-card-footer ')]").text
            title = element.find_element(By.XPATH, ".//h2[@class='mg-card__title']").text
            annotation = element.find_element(By.XPATH, ".//div[@class='mg-card__annotation']").text
            article = Article(title, annotation, create_datetime_from_string(publication_time))
            list_of_articles.append(article)

        logging.info(f'Finished creating articles. First of this: {list_of_articles[0]}')
        return list_of_articles
    
    def close(self) -> None:
        logging.info('Closing browser...')
        self.browser.close()
        logging.info('Browser was closed')
    

def create_datetime_from_string(string_datetime: str) -> datetime:
    """
    Конвертирует дату в текстовом формате в `datetime`

    Пример
    ------
    ```
    test = ['00:29', 'вчера в 09:00', 'вчера в 12:01', '29 сентября в 18:11', '29 сентября в 09:28']
    for a in test:
        print(create_datetime_from_string(a))
    ```

    Вывод (дата теста - 2023-10-01):
    2023-10-01 00:29:00
    2023-09-30 09:00:00
    2023-09-30 12:01:00
    2023-09-29 18:11:00
    2023-09-29 09:28:00
    """

    words = string_datetime.split()
    now = datetime.now()
    if len(words) == 1:
        if ':' in words[0]:
            hour, minute = words[0].split(':')
            dt = datetime(now.year, now.month, now.day, int(hour), int(minute))
    else:
        year, month, day, hour, minute = now.year, now.month, now.day, 0, 0
        for word in words:
            if word == 'вчера':
                yesterday = now - timedelta(days=1)
                day = yesterday.day
                month = yesterday.month
                year = yesterday.year

            elif ':' in word:
                hour, minute = word.split(':')
                hour = int(hour)
                minute = int(minute)

            elif months.get(word):
                month = months.get(word)

            else:
                try:
                    day = int(word)
                    day = day
                except ValueError:
                    continue

        dt = datetime(year, month, day, hour, minute)

    return dt