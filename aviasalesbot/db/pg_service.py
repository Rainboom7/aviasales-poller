import os
import string

import psycopg
from psycopg.abc import Params

from db.queries import SQL_CREATE_TABLES, SQL_CALCULATE_MIN_PRICE, SQL_INSERT_NEW_PRICE
from dto.avia_response_item import AviaResponseItem


class PgService(object):
    def __init__(self):
        self.pg_dbname = os.getenv("POSTGRES_DB", "aviasales")
        self.pg_user = os.getenv("POSTGRES_USER", "postgres")
        self.pg_password = os.getenv("POSTGRES_PASSWORD", "postgres")
        self.pg_postgres_host = os.getenv("POSTGRES_HOST", "127.0.0.1")
        self.pg_postgres_port = os.getenv("POSTGRES_PORT", "5434")
        print(
            f"dbname={self.pg_dbname} user={self.pg_user} password={self.pg_password} host={self.pg_postgres_host} port={self.pg_postgres_port}")
        try:
            with self.__get_connection() as connection:
                with connection.cursor() as curs:
                    curs.execute(SQL_CREATE_TABLES)
            print("Executing SQL_CREATE_TABLE is done")
        except Exception as error:
            print("PostgreSQL connection is failed", error)
        finally:
            connection.close()

    def __get_connection(self):
        connection = psycopg.connect(
            f"dbname={self.pg_dbname} user={self.pg_user} password={self.pg_password} host={self.pg_postgres_host} port={self.pg_postgres_port}")
        connection.autocommit = True
        return connection

    def calculate_min_by_key(self, fly_key: string):
        query_result = self._execute_query_with_params(SQL_CALCULATE_MIN_PRICE, {'fly_key': "\"" + fly_key + "\""})
        if query_result is None:
            return 922337203
        return query_result[0][0]

    def insert_price(self, item: AviaResponseItem):
        self._execute_query_with_params(SQL_INSERT_NEW_PRICE,
                                        {'fly_key': "\"" + item.origin + "->" + item.destination + "\"",
                                         'price': item.price * 2,
                                         'fly_date': item.departure_at,
                                         'link': item.link
                                         })

    def _execute_query_with_params(self, query, params: Params):
        try:
            with self.__get_connection() as cnt:
                with cnt.cursor() as curs:
                    print("Executing query {0} with params {1}".format(query, params))
                    curs.execute(query, params)
                    print("Query {0} result is {1}".format(query, curs.description))
                    if curs.description is not None:
                        return curs.fetchall()
        #   print("Query - {0} is done".format(query.format(*args)))
        except psycopg.InterfaceError as exc:
            print(exc)
        finally:
            cnt.close()
