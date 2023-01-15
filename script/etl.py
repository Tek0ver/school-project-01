# selenium 4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# python
import pandas as pd
import time

# sql
from sqlalchemy import create_engine
import config


def main():
    df_le_monde = scrapping_le_monde(nb_page=1) # default = 0 for all
    df_le_monde = convert_date(df_le_monde) # convert date column to datetime format
    export_to_csv(df=df_le_monde, file_name="le_monde.csv") # export to csv file
    export_to_database(df=df_le_monde, table="le_monde") # export to postgresql database


def scrapping_le_monde(nb_page: int=0):
    # scrap website to df

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
    if nb_page == 0:
        nb_page = last_page

    # create list of dict of title and date for each article about ukraine
    articles = []

    for page in range(1, nb_page+1):
        url = f"https://www.lemonde.fr/recherche/?search_keywords=ukraine&start_at=19/12/1994&end_at=15/12/2022&search_sort=date_desc&page={page}"
        driver.get(url)
        driver_title = driver.find_elements(by=By.XPATH, value='/html/body/main/article/section/section[1]/section[2]/section[3]/section/a/h3')
        driver_date = driver.find_elements(by=By.XPATH, value='/html/body/main/article/section/section[1]/section[2]/section[3]/section/p/span[1]')
        for title, date in zip(driver_title, driver_date):
            articles.append({"title": title.text, "date": date.text})

    driver.quit()

    # create dataframe from dict
    df = pd.DataFrame.from_dict(articles)

    return df


def convert_date(df: pd.DataFrame):
    # convert date column to datetime format
    df["date"] = df["date"].str.findall(r"\d{2} [a-zéèû]* \d{4} à \d{2}h\d{2}").str[0]
    df["date"] = df["date"].str.replace("à ", "").str.replace("h", " ")
    df[['day', 'month', 'year', 'hour', 'minute']] = df['date'].str.split(' ', expand=True)

    month_dict = {
        'janvier': '01',
        'février': '02',
        'mars': '03',
        'avril': '04',
        'mai': '05',
        'juin': '06',
        'juillet': '07',
        'août': '08',
        'septembre': '09',
        'octobre': '10',
        'novembre': '11',
        'décembre': '12'
        }

    df['month'] = df["month"].replace(month_dict)
    df['date'] = df['year'] + '/' + df['month'] + '/' + df['day'] + ' ' + df["hour"] + ':' + df["minute"]
    df['date'] = pd.to_datetime(df['date'])
    df.drop(columns = ['day', 'month', 'year', 'hour', 'minute'], inplace=True)

    return df


def export_to_csv(df: pd.DataFrame, file_name: str):
    # export data to csv
    df.to_csv(f'data/{file_name}', index=False)


def export_to_database(df: pd.DataFrame, table: str):
    # export to postgresql database
    conn_string = f"postgresql://{config.user}:{config.password}@{config.host}/{config.database}"
    conn = create_engine(conn_string).connect()
    df.to_sql(name=table, con=conn, if_exists="append")


if __name__ == "__main__":
    main()