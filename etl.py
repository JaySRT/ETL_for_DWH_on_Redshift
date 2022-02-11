import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    The Function loads data from S3 into staging tables

    Parameters:
    -----------
    cur : psycopg2.cursor
    cursor obtained from active session to execute PostgreSQL commands.

    conn: Database connection.
    
    Returns:
        None
    """
    
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """
    The Function transforms data from staging tables and inserts into actual analytics tables

    Parameters:
    -----------
    cur : psycopg2.cursor
    cursor obtained from active session to execute PostgreSQL commands.

    conn: Database connection.
    
    Returns:
        None
    """
    
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Initiates ETL process
    
    Parameters:
        None
    
    Returns:
        None
    """

    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()