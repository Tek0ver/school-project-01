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
    """scrap new articles and contents from 'le monde' and export it to database"""
    # connection to database
    conn = psycopg2.connect(config.azure_conn_user)
    print("connected")

    # cookies
    accept_cookies(url="https://www.lemonde.fr", path='//*[@id="js-body"]/div[6]/div/footer/button')

    # update database
    if config.article:
        update_articles(conn)

    if config.content:
        update_contents(conn)

    # quit selenium driver
    driver.quit()

    # close sql connection
    conn.close()


def scrap__articles():
    """scrap articles from  , only title, date, then export it to database"""
    pass


def update_articles(conn):
    """scrap new articles title, date and link from 'le monde' and export it to database"""
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
            databaseInterface.export_to_csv(
                df=df_le_monde, file_name="articles.csv", if_exists="append"
            )
        if config.database:
            # export to postgresql database
            databaseInterface.export_to_database(df=df_le_monde, table="articles")

    print(f"{len(df_le_monde)} rows added to articles")


def update_contents(conn):
    """scrap new contents of each new articles from 'le monde' and export it to database"""
    scraping = True
    while scraping:
        # get links of each articles
        links = get_content_link(conn, batch_size=config.batch_size, journal='le monde')
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


def scrap_articles_liberation(max_range=500, time_sleep=5, end_date="31/03/2023"):
    """Scrap all titles and dates from Libération, articles start to end"""
    
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
    
    def close_popup() -> bool:
        try:
            print('Closing popup')
            driver.switch_to.default_content()
            time.sleep(10)
            #print('step 0')
            #iframe = driver.find_element(By.XPATH, '/html/body/iframe[3]')
            print('Step 1')
            driver.switch_to.frame(iframe)
            iframe = driver.find_element(By.XPATH, '//*[@id="mailmunch-popover-frame-*"]')
            print('Step 2')
            driver.switch_to.frame(iframe)
            driver.find_element(By.CSS_SELECTOR, 'html body.contacts.new div.step-container.live a#close-icon').click()
            print('Step 3')
            print("Popup closed")
            driver.switch_to.default_content()
            return True
        except:
            print("No popup")
            return False
       
    def select_dates(start="01/02/2021", end="31/03/2023"):
        time.sleep(2)
        # CSS selectors for text boxes
        start_box = "#datepicker_from"
        end_box = "#datepicker_to"
        submit_button = "#pubDate_filter > div:nth-child(7) > button:nth-child(3)"
        
        driver.find_element(By.CSS_SELECTOR, start_box).send_keys(start)
        driver.find_element(By.CSS_SELECTOR, end_box).send_keys(end)
        
        # submit
        driver.find_element(By.CSS_SELECTOR, submit_button).click()
        
        print(f"Dates submitted ({start} to {end})")
        time.sleep(2)
      
    def select_sort(type_sort="Récent"):
        """Put Récent or Pertinent"""
        
        from selenium.webdriver.support.ui import Select
        
        select = Select(driver.find_element(By.CSS_SELECTOR, '#sortby'))

        # select by visible text
        select.select_by_visible_text(type_sort)
        
        print(f"Sort articles with : {type_sort}")
        time.sleep(2)
    
    def transform_dates(date):
        if type(date) == pd._libs.tslibs.timestamps.Timestamp:
            return date
        else:
            try:
                date = date.split()
                date = pd.to_datetime(" ".join([date[2], month_dict[date[1]], date[0]]))
                return date
            except:
                return f"error date : {date}"
    
    def parse_one_page(time_sleep=5):
        print('Parsing one page')
        driver.set_window_size(1920,1080)
        parsed = []
        time.sleep(time_sleep)

        for article in driver.find_elements(By.CSS_SELECTOR, "div.queryly_item_row"):

            try:
                parsed.append({
                    'journal': 'liberation',
                    'title': article.find_element(
                        By.CLASS_NAME,
                        'queryly_item_title').text,
                    'article_date': article.find_element(
                    By.CSS_SELECTOR,
                    'div.queryly_item_description').find_element(By.CSS_SELECTOR, 'div').text.split(" / ")[0],
                    'link': article.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                })
            except:
                print('FAILED PARSING PAGE')

        print('Page end')
        return parsed

    
    print("Start scraping Libération")
    start_time = time.time()
    
    # define driver
    driver = webdriver.Chrome()

    # open web page
    url = 'https://www.liberation.fr/recherche/?query=ukraine'
    driver.get(url)

    #change iframe for cookies button
    time.sleep(5)
    iframe = driver.find_element(By.XPATH, '//*[@id="sp_message_iframe_726760"]')
    driver.switch_to.frame(iframe)
    # accept cookies
    driver.find_element(By.XPATH, '//*[@id="notice"]/div[3]/div/button[1]').click()
    driver.switch_to.default_content()
    print('Cookies accepted')

    # close bottom bar
    driver.set_window_size(1920,1080)
    time.sleep(5)
    iframe = driver.find_element(By.XPATH, '/html/body/div[1]/iframe')
    driver.switch_to.frame(iframe)
    driver.find_element(By.XPATH, '//*[@id="close-icon"]').click()
    driver.switch_to.default_content()
    print('Bottom bar closed')

    # submit dates
    select_dates(end=end_date)
    
    # sort articles
    select_sort(type_sort="Récent")
    
    popup_closed = False
    parsed = []

    for i, page in enumerate(range(max_range)):
        print(f"Scraping page {i+1}")

        # parse one page
        parsed = parsed + parse_one_page(time_sleep)

        # go to next page
        driver.set_window_size(1920,1080)
        button_xpath_next = '/html/body/div[2]/section/div/div[2]/div/div[2]/div/div/div[2]/a'

        try:
            button_next = driver.find_element(By.XPATH, button_xpath_next)
            button_next.click()
        except:
            if not popup_closed:
                close_popup()
                popup_closed = True
            else:
                print("End of scraping (no more page)")
                break

    print("End of scraping (end of loop)")
    
    # close driver
    driver.quit()
    
    # convert data to dataframe
    df = pd.DataFrame(parsed)

    # transforme date
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
    
    print(f"Time of scraping : {time.time() - start_time}")
    print(f"Number of articles scraped : {df.shape[0]}")
    
    # check for missing data
    print("Check for missing data...")
    missing_data = df[(df['title'] == '') | (df['article_date'] == '') | (df['link'] == '')].shape[0]
    if missing_data > 20:
        print(f"{missing_data} rows with missing data, check for scraping errors.")
    else:
        df = df[~(df['title'] == '') & ~(df['article_date'] == '') & ~(df['link'] == '')]
        print(f"{df.shape[0]} rows of data scraped")

        # convert dates to Pandas Timestamp
        df['article_date'] = df['article_date'].apply(transform_dates)
        
    def cut_link(link: str, lenght=255):
        if len(link) > lenght:
            return link[:lenght]
        else:
            return link

    #cut links too long
    print(f"{df[df['link'].str.len() > 255].shape[0]} links are too long, these will be cuted")
    df['link'] = df['link'].apply(cut_link)
    
    # export to postgresql database
    databaseInterface = DatabaseInterface()
    databaseInterface.export_to_database(df=df, table="articles")
    
    return df


######################################################### scraping #########################################################


def accept_cookies(url, path: str):
    """accept cookies by clicking on XPATH button"""
    # open web page
    driver.get(url)
    # click button
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, path)
        )
    ).click()
    # wait for correct page loading
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
    """get links of articles already in database for stop the scraping function when one of them reached"""
    query = """
        SELECT link
        FROM articles
        ORDER BY id DESC
        ;
    """

    stop_link = databaseInterface.sql_select(query)
    stop_link = [x[0] for x in stop_link]

    return stop_link


def scrap_page(page: int, stop_link, articles, url: str):
    """append scraped title, content and date to articles list of dict"""
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


def get_content_link(conn, batch_size: int, journal: str):
    query = f"""
        SELECT id, link
        FROM articles
        WHERE id NOT IN (
            SELECT article_id
            FROM contents
            ) AND journal = '{journal}'
        ORDER BY id ASC
        LIMIT {batch_size}
        ;
    """

    links = databaseInterface.sql_select(query)

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
    """scrap new contents of each new articles from 'le monde' and export it to database"""
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
    df["date"] = df["date"].str.replace(",", " 00h00")
    df["date"] = df["date"] + " 00h00"
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
