from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def main():
    service = Service('./chromedriver')
    driver = webdriver.Chrome(service=service)
    driver.get('https://scrapingclub.com/exercise/basic_login/')

    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//form')))

    username = driver.find_element(by=By.ID, value='id_name')
    password = driver.find_element(by=By.ID, value='id_password')

    username.send_keys('scrapingclub')
    password.send_keys('scrapingclub')

    login_btn = driver.find_element(by=By.XPATH, value='//form/button')
    login_btn.click()

    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "card")]')))

    congratulations = driver.find_element(by=By.XPATH, value='/html/body/div/div/div[1]/div[2]/p').text
    print(congratulations)

    driver.quit()


if __name__ == '__main__':
    main()
