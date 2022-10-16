from configparser import ConfigParser
from typing import Dict
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


def create_db(
    conn_info: Dict[str, str],
) -> None:
    psql_connection_string = f"host={conn_info['host']} user={conn_info['user']} password={conn_info['password']}"
    print(psql_connection_string)
    conn = psycopg2.connect(psql_connection_string)
    cur = conn.cursor()
    conn.autocommit = True
    sql_query = f"CREATE DATABASE {conn_info['database']}"

    try:
        cur.execute(sql_query)
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        print(f"Query: {cur.query}")
        cur.close()
    else:
        conn.autocommit = False


def create_table(
    sql_query: str, 
    conn: psycopg2.extensions.connection, 
    cur: psycopg2.extensions.cursor
) -> None:
    try:
        cur.execute(sql_query)
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        print(f"Query: {cur.query}")
        conn.rollback()
        cur.close()
    else:
        conn.commit()


def setup_database() -> None:
    conn_info = load_connection_info("db.ini")
    
    create_db(conn_info)

    connection = psycopg2.connect(**conn_info)
    cursor = connection.cursor()

    house_sql = """
        CREATE TABLE properties (
            id SERIAL PRIMARY KEY,
            street VARCHAR(200) NOT NULL
        )
    """
    create_table(house_sql, connection, cursor)

    connection.close()
    cursor.close()


def connect_to_database() -> psycopg2.extensions.connection:
    conn_info = load_connection_info("db.ini")
    connection = psycopg2.connect(**conn_info)

    return connection
    

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