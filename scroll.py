import json
import random
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_data(products):
    data = []
    for product in products:
        img = product.find_element(by=By.TAG_NAME, value='img').get_attribute('src')
        link = product.find_element(by=By.TAG_NAME, value='a').get_attribute('href')
        title = product.find_element(by=By.XPATH, value='.//h4/a').text
        price = product.find_element(by=By.TAG_NAME, value='h5').text

        temp_dict = {
            'img': img,
            'link': link,
            'title': title,
            'price': price
        }
        data.append(temp_dict)

    return data


def write_data(data):
    try:
        with open('products.json', 'r') as f:
            content = json.load(f)
    except IOError:
        print('products.json does not exist. It will be created.')
    with open('products.json', 'w') as f:
        try:
            content += data
            json.dump(content, f)
        except UnboundLocalError:
            json.dump(data, f)


def main():
    options = Options()
    options.add_argument('--headless')
    service = Service('./chromedriver')
    driver = webdriver.Chrome(service=service, options=options)
    driver.get('https://scrapingclub.com/exercise/list_infinite_scroll/')

    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "card")]')))

    first_height = 0
    flag = True
    i = 0
    print('Start scroll and scrape.')
    while flag:
        products = driver.find_elements(by=By.XPATH, value='//div[@class="card"]')
        data = scrape_data(products[i:])
        i += len(data)
        print(f'\nScraped {len(data)} products')
        write_data(data)
        print('Wrote this products in products.json.')
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(random.uniform(0, 1))
        
        new_height = driver.execute_script('return document.body.scrollHeight')

        if first_height == new_height:
            print(f'\nEnd scroll and scrape. \n'
                  f'Page height: {new_height}px \n'
                  f'Scraped products amount: {i}')
            flag = False

        first_height = new_height

    driver.quit()


if __name__ == '__main__':
    main()
