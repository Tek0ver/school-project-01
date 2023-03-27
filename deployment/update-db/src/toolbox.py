import config

import psycopg2
import pandas as pd
from io import StringIO


class DatabaseInterface:
    def __init__(self):
        """connect to sql database if possible, else load csv to dataframe"""
        self.mode = "azure"
        try:
            self.conn = psycopg2.connect(config.azure_conn_user)
            self.cursor = self.conn.cursor()
        except:
            # TODO log to implement
            self.mode = "local"
            print("[FAIL] Database failure, local mode activated.")
            self.data = {"articles": pd.read_csv("./data-offline/articles.csv")}

    def select(self, query: str) -> pd.DataFrame:
        """load data with sql select"""
        if self.mode == "azure":
            self.cursor.execute(query)
            data = self.cursor.fetchall()
            column_names = [desc[0] for desc in self.cursor.description]
            dataframe = pd.DataFrame(data, columns=column_names)

            return dataframe

        elif self.mode == "local":

            return self.data["articles"]

    def export_to_database(self, df: pd.DataFrame, table: str):
        """
        export to postgresql table
        """
        # save dataframe to an in memory buffer
        cols = tuple(df.columns)
        buffer = StringIO()
        # export
        df.to_csv(buffer, header=False, index=False, sep=";")
        buffer.seek(0)
        cursor = self.conn.cursor()
        cursor.copy_from(buffer, table, sep=";", columns=cols)
        self.conn.commit()

    def export_to_csv(
        self, df: pd.DataFrame, file_name: str, if_exists: str = "replace"
    ):
        """
        export df to csv
        if_exists : {'replace', 'append'}, default 'replace'
        """
        if if_exists == "replace":
            df.to_csv(f"{file_name}", index=False)
        elif if_exists == "append":
            df.to_csv(f"{file_name}", mode="a", index=False, header=False)

    def sql_select(self, query):
        """simple sql select"""
        self.cursor.execute(query)

        return self.cursor.fetchall()

    def sql_execute(self, query):
        """execute sql query"""
        self.cursor.execute(query)
        self.conn.commit()
