import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# tests/test_db_connector.py

import unittest
from src.db_connector import get_db_connection


class TestDBConnection(unittest.TestCase):
    def test_db_connection(self):
        """
        Test the database connection and print all tables in the database.
        """
        conn = get_db_connection()
        self.assertIsNotNone(conn, "Database connection should not be None")

        if conn:
            try:
                with conn.cursor() as cursor:
                    # Execute a query to get all table names
                    cursor.execute("SHOW TABLES;")
                    tables = cursor.fetchall()

                    # Print all table names
                    print("Tables in the database:")
                    for table in tables:
                        print(table[0])

                # Close the connection
                conn.close()
            except Exception as e:
                print(f"Error querying the database: {e}")
                self.fail(f"Test failed due to an error: {e}")


if __name__ == "__main__":
    unittest.main()
