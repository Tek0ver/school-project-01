import pandas as pd


def main():
    df = pd.read_csv("data/le_monde.csv")
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
    df['date'] = df['day'] + '/' + df['month'] + '/' + df['year'] + ' ' + df["hour"] + ':' + df["minute"]
    df['date'] = pd.to_datetime(df['date'])
    df.drop(columns = ['day', 'month', 'year', 'hour', 'minute'], inplace=True)

    df.to_csv('data/le_monde.csv')



if __name__ == "__main__":
    main()