# selenium 4, scraping library
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
from datetime import date
from datetime import timedelta

# sql
from sqlalchemy import create_engine

# system
from os import environ


def main():
    df_le_monde = scraping_le_monde(nb_page=1)
    # convert date column to datetime format
    if len(df_le_monde) > 0:
        df_le_monde = convert_date(df_le_monde)
    # export to csv file
    export_to_csv(df=df_le_monde, file_name="le_monde.csv", if_exists="replace")
    # export to postgresql database
    export_to_database(df=df_le_monde, table="le_monde", if_exists="append")
    print(f"{len(df_le_monde)} rows added to database")



def scraping_le_monde(nb_page: int=0, driver=driver):
    """
    scrap website until the last article scraped last time\n
    nb_page : int, default 0 for all pages \n
    return dataframe
    """

    # open web page
    url = f"https://www.lemonde.fr/recherche/?search_keywords=ukraine&search_sort=dateCreated_desc&page=1"
    driver.get(url)

    # accept cookies
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="js-body"]/div[6]/div/footer/button'))).click()
    time.sleep(1)

    # get the number of maximum pages for the scrap
    if nb_page == 0:
        driver.get(url)
        last_page = int(driver.find_elements(by=By.XPATH, value='/html/body/main/article/section/section[1]/section[2]/section[4]/a[5]')[0].text)
        nb_page = last_page

    # create list of dict of title and date for each article about ukraine
    articles = []

    # read the save.txt file where are saved last titles scraped from last scraped to define when to stop the current scrap
    with open("script/save.txt") as f:
        stop_title = f.read().splitlines()

    stop = False
    for page in range(1, nb_page+1):
        url = f"https://www.lemonde.fr/recherche/?search_keywords=ukraine&search_sort=dateCreated_desc&page={page}"
        driver.get(url)
        driver_title = []
        driver_content = []
        i = 1
        end = 0
        while end < 5:
            try:
                title_article = driver.find_element(by=By.XPATH, value=f'/html/body/main/article/section/section[1]/section[2]/section[3]/section[{i}]/a/h3')
                if title_article.text in stop_title:
                    # stop title (from the save.txt file) reached, so break the while loop
                    # set stop = True to break the for loop too
                    stop = True
                    break
                else:
                    # get title
                    driver_title.append(title_article.text)

                    # get content
                    title_article.click()
                    contents = driver.find_elements(by=By.XPATH, value="/html/body/main/section[1]/section/section/article/p") # article
                    contents.insert(0, driver.find_element(by=By.CLASS_NAME, value="article__desc")) # article desc                                                               
                    contents = [content.text for content in contents]
                    driver_content.append(contents[0])

                    # back to url for next article
                    driver.get(url)

                    # reinitialize end because we found a new article so it's not end page
                    end = 0
            except:
                # ad or end page: count until 5 to be sure it's the end page and not an ad
                end += 1
            # go to next article
            i += 1

        driver_date = driver.find_elements(by=By.XPATH, value='/html/body/main/article/section/section[1]/section[2]/section[3]/section/p/span[1]')
        # append scraped title, content and date to articles list of dict

        for title, content, date in zip(driver_title, driver_content, driver_date):
            articles.append({"title": title, "content": content, "date": date.text})

        if stop:
            # stop title (from the save.txt file) reached, so break the for loop
            break

    driver.quit()

    # save 5 last title into save.txt file for the next scrap (5 to be sure to don't miss the point cause of an eventual title rename)
    if len(articles) >= 5:
        with open("script/save.txt", "w") as f:
            for i in range(5):
                f.write(f'{articles[i]["title"]}\n')
    # same thing but if less than 5 titles scraped
    elif len(articles) > 0:
        with open("script/save.txt", "w") as f:
            for i in range(len(articles)):
                f.write(f'{articles[i]["title"]}\n')

    # create dataframe from dict
    df = pd.DataFrame.from_dict(articles)

    return df[::-1]


def convert_date(df: pd.DataFrame):
    """
    convert string date column to datetime format
    """
    df["date"] = df["date"].str.findall(r"[^Publié le ].+?(?=\d{2}h\d{2}).{5}").str[0]
    df["date"] = df["date"].str.replace("à ", "")
    today = date.today()
    yesterday = today - timedelta(days = 1)
    df["date"] = df["date"].str.replace("aujourd’hui", today.strftime('%d %m %Y'))
    df["date"] = df["date"].str.replace("hier", yesterday.strftime('%d %m %Y'))
    df["date"] = df["date"].str.replace("h", " ")
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


def export_to_csv(df: pd.DataFrame, file_name: str, if_exists: str="replace"):
    """
    export df to csv
    if_exists : {'replace', 'append'}, default 'replace'
    """
    if if_exists == "replace":
        df.to_csv(f'data/{file_name}', index=False)
    elif if_exists == "append":
        df.to_csv(f'data/{file_name}', mode='a', index=False, header=False)


def export_to_database(df: pd.DataFrame, table: str, if_exists: str="append"):
    """
    export to postgresql database
    if_exists : {'fail', 'replace', 'append'}, default 'append'
    """
    conn_string = f'postgresql://{environ["POSTGRES_USER"]}:{environ["POSTGRES_PASSWORD"]}@{environ["POSTGRES_HOST"]}/{environ["POSTGRES_DB"]}'
    conn = create_engine(conn_string).connect()
    df.to_sql(name=table, con=conn, if_exists=if_exists, index=False)


if __name__ == "__main__":
    main()