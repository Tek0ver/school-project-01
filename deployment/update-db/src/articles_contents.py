import config
from toolbox import DatabaseInterface

# python
import pandas as pd
import time
from datetime import date
from datetime import timedelta

# sql
import psycopg2

# selenium 4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# init driver
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
if config.headless:
    options.add_argument("--headless")
driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()),
    options=options,
)


databaseInterface = DatabaseInterface()


def main():
    print("starting...")
    start_time = time.time()

    update_database()

    # get execute time
    print(f"{round(time.time() - start_time, 2)} seconds")


def update_database():
    # connection to database
    conn = psycopg2.connect(config.azure_conn_user)
    print("connected")

    # cookies
    accept_cookies("https://www.lemonde.fr")

    # update database
    if config.article:
        update_articles(conn)

    if config.content:
        update_contents(conn)

    # quit selenium driver
    driver.quit()

    # close sql connection
    conn.close()


def update_articles(conn):
    print("start to scrap articles")
    # create df
    df_le_monde = scraping_journal(
        conn,
        journal_name="le monde",
        nb_page=config.nb_page,
        url="https://www.lemonde.fr/recherche/?search_keywords=ukraine&start_at=01%2F01%2F2021&search_sort=dateCreated_desc",
    )
    if len(df_le_monde) > 0:
        # convert date column to datetime format
        df_le_monde = convert_date(df_le_monde)
        # make sure df is in correct format
        df_le_monde = df_le_monde.replace("\n", "", regex=True)
        df_le_monde = df_le_monde.replace(";", "", regex=True)
        if config.csv:
            # export to csv file
            databaseInterface.export_to_csv(df=df_le_monde, file_name="articles.csv", if_exists="append")
        if config.database:
            # export to postgresql database
            databaseInterface.export_to_database(df=df_le_monde, table="articles")

    print(f"{len(df_le_monde)} rows added to articles")


def update_contents(conn):
    scraping = True
    while scraping:
        # get links of each articles
        links = get_content_link(conn, batch_size=config.batch_size)
        if len(links) > 0:
            print(f"start to scrap {len(links)} contents")
            # create df
            df_content = scrap_content(links)
            # make sure df is in correct format
            df_content = df_content.replace("\n", "", regex=True)
            df_content = df_content.replace(";", "", regex=True)
            if config.csv:
                # export to csv file
                databaseInterface.export_to_csv(
                    df=df_content, file_name="content.csv", if_exists="append"
                )
            if config.database:
                # export to postgresql database
                databaseInterface.export_to_database(df=df_content, table="contents")

            print(f"{len(df_content)} rows added to contents")
        else:
            scraping = False

    print("content scraped")


######################################################### scraping #########################################################


def accept_cookies(url):
    # open web page
    driver.get(url)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="js-body"]/div[6]/div/footer/button')
        )
    ).click()
    time.sleep(6)


def scraping_journal(conn, journal_name: str, nb_page: int = 0, url: str = ""):
    """
    scrap website until the last article scraped last time \n
    nb_page : int, default 0 for all pages \n
    return dataframe
    """

    # get the number of maximum pages for the scrap
    if nb_page == 0:
        driver.get(url)
        last_page = int(
            driver.find_elements(
                by=By.XPATH,
                value="/html/body/main/article/section/section[1]/section[2]/section[4]/a[5]",
            )[0].text
        )
        nb_page = last_page

    # create list of dict of title and date for each article about ukraine
    articles = []

    # read the last 5 titles to define when to stop the current scrap
    if config.only_new_articles:
        stop_link = last_links(conn)
    else:
        stop_link = ""

    print(f"stop link: {stop_link}")
    for page in range(1, nb_page + 1):
        print(f"page {page} is scraping...")
        if scrap_page(page, stop_link, articles, url):
            print("stop reached")
            break

    # create dataframe from dict
    df = pd.DataFrame.from_dict(articles)
    df.insert(0, "journal", journal_name)
    df = df[::-1].reset_index(drop=True)

    return df


def last_links(conn):
    query = """
        SELECT link
        FROM articles
        ORDER BY id DESC
        LIMIT 5
        ;
    """

    stop_link = sql_select(conn, query)
    stop_link = [x[0] for x in stop_link]

    return stop_link


def scrap_page(page: int, stop_link, articles, url: str):
    stop = False
    url = f"{url}&page={page}"
    driver.get(url)
    titles = []
    links = []
    i = 1
    end = 0
    while end < 5:
        try:
            title_article = get_title(
                xpath=f"/html/body/main/article/section/section[1]/section[2]/section[3]/section[{i}]/a/h3"
            )
            link_article = get_link(
                xpath=f"/html/body/main/article/section/section[1]/section[2]/section[3]/section[{i}]/a"
            )

            if link_article in stop_link:
                # stop title reached, so break the while loop
                # set stop = True to break the for loop too
                print(
                    f"{title_article.text} + {link_article} already scraped from last run"
                )
                stop = True
                break
            else:
                # get title
                titles.append(title_article)
                # get link
                links.append(link_article)

                # reinitialize end because we found a new article so it's not end page
                end = 0
        except:
            # ad or end page: count until 5 to be sure it's the end page and not an ad
            end += 1
        # go to next article
        i += 1

    dates = get_date(
        xpath="/html/body/main/article/section/section[1]/section[2]/section[3]/section/p/span[1]"
    )

    # append scraped title, content and date to articles list of dict
    for title, date, link in zip(titles, dates, links):
        articles.append({"title": title.text, "date": date.text, "link": link})

    if stop:
        # stop title reached, so break the for loop
        return True


def sql_select(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)

    return cursor.fetchall()


def sql_execute(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()


def get_content_link(conn, batch_size: int):
    query = f"""
        SELECT id, link
        FROM articles
        WHERE id NOT IN (
            SELECT article_id
            FROM contents
            )
        ORDER BY id ASC
        LIMIT {batch_size}
        ;
    """

    links = sql_select(conn, query)

    return links


def get_content(driver, link: str):
    # get content
    driver.get(link)
    contents_desc = driver.find_elements(by=By.CSS_SELECTOR, value=".article__desc")
    contents_paragraph = driver.find_elements(
        by=By.XPATH, value="/html/body/main/section[1]/section/section/article"
    )
    contents_live = driver.find_elements(by=By.XPATH, value='//*[@id="post-container"]')
    contents_post = driver.find_elements(by=By.XPATH, value='//*[@id="main"]/article')
    # concat the 2 list
    contents = contents_desc + contents_paragraph + contents_live + contents_post
    # transform selenium object to string
    contents = [content.text for content in contents]
    content = " ".join(contents)

    return content


def scrap_content(links):
    # open web page
    driver.get(links[0][1])
    contents = {}
    # contents = {"article_id": "content", ...}
    for link in links:
        contents[link[0]] = get_content(driver, link[1])

    df_content = pd.DataFrame(contents.items(), columns=["article_id", "content"])

    return df_content


def get_title(xpath: str):
    title = driver.find_element(by=By.XPATH, value=xpath)

    return title


def get_date(xpath: str):
    dates = driver.find_elements(by=By.XPATH, value=xpath)

    return dates


def get_link(xpath: str):
    link = driver.find_element(by=By.XPATH, value=xpath).get_attribute("href")

    return link


######################################################### handling data #########################################################


def convert_date(df: pd.DataFrame):
    """
    convert string date column to datetime format
    """
    df["date"] = df["date"].str.findall(r"[^Publié le ].+?(?=\d{2}h\d{2}).{5}").str[0]
    df["date"] = df["date"].str.replace("à ", "")
    today = date.today()
    yesterday = today - timedelta(days=1)
    df["date"] = df["date"].str.replace("aujourd’hui", today.strftime("%d %m %Y"))
    df["date"] = df["date"].str.replace("hier", yesterday.strftime("%d %m %Y"))
    df["date"] = df["date"].str.replace("h", " ")
    df[["day", "month", "year", "hour", "minute"]] = df["date"].str.split(
        " ", expand=True
    )

    month_dict = {
        "janvier": "01",
        "février": "02",
        "mars": "03",
        "avril": "04",
        "mai": "05",
        "juin": "06",
        "juillet": "07",
        "août": "08",
        "septembre": "09",
        "octobre": "10",
        "novembre": "11",
        "décembre": "12",
    }

    df["month"] = df["month"].replace(month_dict)
    df["date"] = (
        df["year"]
        + "/"
        + df["month"]
        + "/"
        + df["day"]
        + " "
        + df["hour"]
        + ":"
        + df["minute"]
    )
    df["article_date"] = pd.to_datetime(df["date"])
    df.drop(columns=["day", "month", "year", "hour", "minute", "date"], inplace=True)

    return df


if __name__ == "__main__":
    main()
