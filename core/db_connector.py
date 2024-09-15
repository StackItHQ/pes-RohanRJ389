import pymysql
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config.config import Config


DB_HOST = MYSQL_HOST = Config.MYSQL_HOST
DB_PORT = MYSQL_PORT = Config.MYSQL_PORT
DB_USER = MYSQL_USER = Config.MYSQL_USER
DB_PASSWORD = MYSQL_PASSWORD = Config.MYSQL_PASSWORD
DB_NAME = MYSQL_DB = Config.MYSQL_DB


def get_db_connection():
    """
    Creates and returns a connection to the MySQL database.
    """
    try:
        conn = pymysql.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
        )
        return conn
    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL: {e}")
        return None
