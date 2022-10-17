from configparser import ConfigParser
from typing import Dict
from xmlrpc.client import boolean
from constants import PROPERTIES_TABLE_NAME
import psycopg2
import psycopg2.extras as psql_extras
import pandas as pd

def load_connection_info(
    ini_filename: str
) -> Dict[str, str]:
    parser = ConfigParser()
    parser.read(ini_filename)
    conn_info = {param[0]: param[1] for param in parser.items("postgresql")}
    return conn_info


def connect_to_database(conn_info: str='') -> psycopg2.extensions.connection:
    if conn_info == '':
        conn_info = load_connection_info("db.ini")

    return psycopg2.connect(**conn_info)


def table_exists(
    table_name: str,     
    cur: psycopg2.extensions.cursor
) -> boolean:
    query="""
        SELECT EXISTS(
            SELECT * FROM information_schema.tables 
            WHERE table_name='{table_name}'
            )
    """.format(table_name=table_name)

    cur.execute(query)
    return bool(cur.fetchone()[0])


def create_table(
    table_name: str,
    conn: psycopg2.extensions.connection, 
    cur: psycopg2.extensions.cursor
) -> None:
    if not table_exists(table_name, cur):
        query = """
            CREATE TABLE {table_name} (
                id SERIAL PRIMARY KEY,
                street VARCHAR(200) NOT NULL
            )
        """.format(table_name=table_name)
        try:
            cur.execute(query)
        except Exception as e:
            print(f"{type(e).__name__}: {e}")
            print(f"Query: {cur.query}")
            conn.rollback()
            cur.close()
        else:
            conn.commit()


def setup_database() -> None:
    connection = connect_to_database()
    cursor = connection.cursor()

    create_table(PROPERTIES_TABLE_NAME, connection, cursor)

    connection.close()
    cursor.close()


def insert_property(
    conn: psycopg2.extensions.connection,
    cur: psycopg2.extensions.cursor,
    df: pd.DataFrame,
    page_size: int
) -> None:
    data_tuples = [tuple(row.to_numpy()) for index, row in df.iterrows()]

    try:
        psql_extras.execute_values(
            cur, query, data_tuples, page_size=page_size)
        print("Query:", cur.query)

    except Exception as error:
        print(f"{type(error).__name__}: {error}")
        print("Query:", cur.query)
        conn.rollback()
        cur.close()

    else:
        conn.commit()