import psycopg2
import sys
import json

from config import config
from src.exception import CustomException
from src.logger import logging


class DataModeling:

    def __init__(self) -> None:
        pass

    def insertMany(self, data):
        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            curr = conn.cursor()
            query = 'INSERT INTO weatherdata (id, stationid, date, year, maxtemp, mintemp, precipitation) VALUES(%s, %s, %s, %s, %s, %s, %s)'

            curr.executemany(query, data)
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as e:
            raise CustomException(e, sys)
        finally:
            if conn is not None:
                curr.close()
                conn.close()

    def validate_station_data(self, stationid):
        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            curr = conn.cursor()
            query = 'SELECT exists (SELECT 1 FROM weatherdata WHERE stationid = %s LIMIT 1)'
            curr.execute(query, (stationid, ))
            response = curr.fetchone()
            return response[0]
        except (Exception, psycopg2.DatabaseError) as e:
            raise CustomException(e, sys)
        finally:
            if conn is not None:
                curr.close()
                conn.close()

    def get_weather_stats_from_db(self, stationid=None, year=None, page=1, page_size=10):
        conn = None
        try:
            query_filter_keys = []
            query_filter_values = []

            if stationid is not None:
                query_filter_keys.append("stationid = %s")
                query_filter_values.append(stationid)
            if year is not None:
                query_filter_keys.append("year = %s")
                query_filter_values.append(year)

            query_filter_keys = " and ".join(query_filter_keys)
            query_limit = page_size
            query_offset = page_size * (int(page) - 1)
            print(stationid, year, page, page_size,
                  query_filter_keys, query_filter_values)
            params = config()
            conn = psycopg2.connect(**params)
            curr = conn.cursor()
            # query = f'select json_agg(to_json(t.*)) AS json_array, (select count(*) as total_count from weatherdata where {query_filter_keys}) as count_query from (select ROUND(AVG(maxtemp)/10, 2) as avg_maxtemp, ROUND(AVG(mintemp)/10, 2) as avg_mintemp, SUM(precipitation)/100 as precipitation, year, stationid  from weatherdata where {query_filter_keys} group by stationid, year order by year, stationid limit {query_limit} offset {query_offset}) t'
            query = f'select json_agg(to_json(t)) as output from (select count(*) OVER() as total_count, ROUND(AVG(maxtemp)/10, 2) as avg_maxtemp, ROUND(AVG(mintemp)/10, 2) as avg_mintemp, SUM(precipitation)/100 as precipitation, year, stationid  from weatherdata where {query_filter_keys} group by stationid, year order by year, stationid limit {query_limit} offset {query_offset}) t'

            curr.execute(query, tuple(
                query_filter_values))
            rows = curr.fetchall()
            return rows[0][0]
        except (Exception, psycopg2.DatabaseError) as e:
            raise CustomException(e, sys)
        finally:
            if conn is not None:
                curr.close()
                conn.close()
