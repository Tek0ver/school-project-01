# selenium 4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

# driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# python
import pandas as pd
import time


def main():
    # define driver
    driver = webdriver.Chrome()

    # open web page
    url = f"https://www.lemonde.fr/recherche/?search_keywords=ukraine&start_at=19/12/1994&end_at=15/12/2022&search_sort=date_desc&page=1"
    driver.get(url)

    # accept cookies
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="js-body"]/div[6]/div/footer/button'))).click()
    time.sleep(1)

    # get the number of pages for the search
    driver.get(url)
    last_page = int(driver.find_elements(by=By.XPATH, value='/html/body/main/article/section/section[1]/section[2]/section[4]/a[5]')[0].text)

    # create list of dict of title and date for each article about ukraine
    articles = []

    for page in range(1, last_page):
        url = f"https://www.lemonde.fr/recherche/?search_keywords=ukraine&start_at=19/12/1994&end_at=15/12/2022&search_sort=date_desc&page={page}"
        driver.get(url)
        driver_title = driver.find_elements(by=By.XPATH, value='/html/body/main/article/section/section[1]/section[2]/section[3]/section/a/h3')
        driver_date = driver.find_elements(by=By.XPATH, value='/html/body/main/article/section/section[1]/section[2]/section[3]/section/p/span[1]')
        for title, date in zip(driver_title, driver_date):
            articles.append({"title": title.text, "date": date.text})

    driver.quit()

    # create dataframe from dict
    df = pd.DataFrame.from_dict(articles)

    # create csv
    df.to_csv('../data/le_monde.csv')



if __name__ == "__main__":
    main()