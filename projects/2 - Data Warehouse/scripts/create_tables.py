import configparser
import psycopg2
from pathlib import Path
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    # Load pararameters from dwh.cfg
    path = Path(__file__)
    ROOT_DIR = path.parent.absolute() # Use root path if calling script from a separate directory
    config_path = Path(ROOT_DIR, 'dwh.cfg')
    config = configparser.ConfigParser()
    config.read_file(open(config_path))

    conn = psycopg2.connect(
        dbname=config.get("CLUSTER", "DB_NAME"),
        user=config.get("CLUSTER", "DB_USER"),
        password=config.get("CLUSTER", "DB_PASSWORD"),
        host=config.get("CLUSTER", "HOST"),
        port=config.get("CLUSTER", "DB_PORT")
    )
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()