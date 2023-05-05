import psycopg2
import sys

from config import config
from src.exception import CustomException
from src.logger import logging


class DataModeling:

    def __init__(self) -> None:
        pass

    def insertOne(self, data):
        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            curr = conn.cursor()
            query = 'INSERT INTO weatherdata (id, stationid, date, maxtemp, mintemp, precipitation) VALUES(%s, %s, %s, %s, %s, %s)'

            response = curr.execute(query, data)
            print(response)
        except (Exception, psycopg2.DatabaseError) as e:
            raise CustomException(e, sys)
        finally:
            if conn is not None:
                conn.close()

    def insertMany(self, data):
        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            curr = conn.cursor()
            query = 'INSERT INTO weatherdata (id, stationid, date, maxtemp, mintemp, precipitation) VALUES(%s, %s, %s, %s, %s, %s)'

            response = curr.executemany(query, data)
            conn.commit()
            print(response)
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

    def get_weather_stats(self, stationid=None, date=None, page=0):
        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            curr = conn.cursor()
            query = ''
            curr.execute(query, (stationid, ))
            response = curr.fetchone()
            return response[0]
        except (Exception, psycopg2.DatabaseError) as e:
            raise CustomException(e, sys)
        finally:
            if conn is not None:
                curr.close()
                conn.close()
