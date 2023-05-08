import psycopg2
import sys
import json

from config import db_config, page_config
from src.exception import CustomException
from src.logger import logging


""""
This function is to insert data to weatherdata table in weather database when the insert_data_from_file_to_db function  
is triggered from data_ingestion.py file.

It inserts all records from a weather station as all in one transaction.
"""


def insertMany(data):
    conn = None
    try:
        params = db_config()
        conn = psycopg2.connect(**params)
        curr = conn.cursor()
        query = 'INSERT INTO weatherdata (stationid, date, year, maxtemp, mintemp, precipitation) VALUES(%s, %s, %s, %s, %s, %s)'
        curr.executemany(query, data)
        conn.commit()
        logging.info('Inserted weather data into database successfully')
    except (Exception, psycopg2.DatabaseError) as e:
        raise CustomException(e, sys)
    finally:
        if conn is not None:
            curr.close()
            conn.close()


""""
This function is to validate the stationid present in weatherdata table from weather database when the data ingestion function is triggered.

It returns the output as boolean
"""


def validate_station_data(stationid):
    conn = None
    try:
        params = db_config()
        conn = psycopg2.connect(**params)
        curr = conn.cursor()
        query = 'SELECT exists (SELECT 1 FROM weatherdata WHERE stationid = %s LIMIT 1)'
        curr.execute(query, (stationid, ))
        response = curr.fetchone()
        logging.info('Validated station data from database successfully')
        return response[0]
    except (Exception, psycopg2.DatabaseError) as e:
        raise CustomException(e, sys)
    finally:
        if conn is not None:
            curr.close()
            conn.close()


""""
This function is to get weather statistics to weatherdata table from weather database when the /api/weather/stats api is called.

It returns the data as output in two columns {total_count(INTEGER), results(JSON Array Object)}, for more details refer /swagger api
"""


def get_weather_stats_from_db(stationid=None, year=None, page=1):
    conn = None
    try:
        page_params = page_config()
        query_filter_keys = []
        query_filter_values = {}

        if stationid is not None:
            query_filter_keys.append("stationid = %(stationid)s")
            query_filter_values["stationid"] = stationid
        if year is not None:
            query_filter_keys.append("year = %(year)s")
            query_filter_values["year"] = year

        filter_query = " and ".join(query_filter_keys)
        query_limit = int(page_params["page_count"])
        query_offset = query_limit * (int(page) - 1)
        params = db_config()
        conn = psycopg2.connect(**params)
        curr = conn.cursor()
        if query_filter_keys:
            query = f"""
                        select row_to_json(o) as output from (
                            select (
                                select count(*) OVER() from weatherdata where {filter_query} group by stationid, year limit 1) as total_count, 
                                json_agg(to_json(t)) as results 
                                from (
                                    select ROUND(AVG(maxtemp)/10, 2) as avg_maxtemp, 
                                    ROUND(AVG(mintemp)/10, 2) as avg_mintemp, 
                                    SUM(precipitation)/100 as total_precipitation, 
                                    year, 
                                    stationid  from weatherdata 
                                    where {filter_query} group by stationid, year order by year, stationid limit {query_limit} offset {query_offset}
                                    ) as t
                                ) as o"""
            curr.execute(query, query_filter_values)
        else:
            query = f"""
                        select row_to_json(o) as output from (
                            select (
                                select count(*) OVER() from weatherdata group by stationid, year limit 1) as total_count, 
                                json_agg(to_json(t)) as results from (
                                    select ROUND(AVG(maxtemp)/10, 2) as avg_maxtemp, 
                                    ROUND(AVG(mintemp)/10, 2) as avg_mintemp, 
                                    SUM(precipitation)/100 as total_precipitation, 
                                    year, 
                                    stationid  from weatherdata group by stationid, year order by year, stationid limit {query_limit} offset {query_offset}
                                    ) as t
                                ) as o"""
            curr.execute(query)

        rows = curr.fetchall()
        logging.info('Fetched Weather stats data from database successfully')
        return rows[0][0]
    except (Exception, psycopg2.DatabaseError) as e:
        raise CustomException(e, sys)
    finally:
        if conn is not None:
            curr.close()
            conn.close()


""""
This function is to get weather data to weatherdata table from weather database when the /api/weather api is called.

It returns the data as output in two columns {total_count(INTEGER), results(JSON Array Object)}, for more details refer /swagger api
"""


def get_weather_data_from_db(stationid=None, year=None, page=1):
    conn = None
    try:
        page_params = page_config()
        query_filter_keys = []
        query_filter_values = {}

        if stationid is not None:
            query_filter_keys.append("stationid = %(stationid)s")
            query_filter_values["stationid"] = stationid
        if year is not None:
            query_filter_keys.append("year = %(year)s")
            query_filter_values["year"] = year

        filter_query = " and ".join(query_filter_keys)
        query_limit = int(page_params["page_count"])
        query_offset = query_limit * (int(page) - 1)
        params = db_config()
        conn = psycopg2.connect(**params)
        curr = conn.cursor()
        if query_filter_keys:
            query = f"""
                        select row_to_json(o) as output from (
                            select ( select 
                                    count(*) from weatherdata where {filter_query}
                                    ) as total_count, 
                                    json_agg(to_json(t)) as results 
                                    from ( 
                                        select 
                                            ROUND(maxtemp/10, 2) as maxtemp, 
                                            ROUND(mintemp/10, 2) as mintemp, 
                                            ROUND(precipitation/100, 2) as precipitation, 
                                            date, 
                                            year, 
                                            stationid  
                                            from weatherdata 
                                            where {filter_query} order by year, stationid limit {query_limit} offset {query_offset}
                                ) as t
                            ) as o"""
            curr.execute(query, query_filter_values)
        else:
            query = f"""select row_to_json(o) as output from (
                        select (select count(*) from weatherdata) as total_count, 
                            json_agg(to_json(t)) as results 
                            from (
                                select ROUND(maxtemp/10, 2) as maxtemp, 
                                ROUND(mintemp/10, 2) as mintemp, 
                                ROUND(precipitation/100, 2) as precipitation, 
                                date, 
                                year, 
                                stationid  from weatherdata order by year, stationid limit {query_limit} offset {query_offset}
                                ) as t
                            ) as o"""
            curr.execute(query)
        rows = curr.fetchall()
        logging.info('Fetched Weather stats data from database successfully')
        return rows[0][0]
    except (Exception, psycopg2.DatabaseError) as e:
        raise CustomException(e, sys)
    finally:
        if conn is not None:
            curr.close()
            conn.close()


""""
This function is to insert data to weatherstats table in weather database when the /api/weather/stats api is called.

It checks if data is already present in database, if not present then it will perform insertion operation.
"""


def insert_weather_stats_to_db(stationid=None, year=None, total_precipitation=None, avg_maxtemp=None, avg_mintemp=None):
    conn = None
    try:
        query_filter_keys = []
        insert_keys = []
        query_filter_values = {}

        query_filter_keys.append("stationid = %(stationid)s")
        insert_keys.append("%(stationid)s")
        query_filter_values["stationid"] = stationid

        query_filter_keys.append("year = %(year)s")
        insert_keys.append("%(year)s")
        query_filter_values["year"] = year

        query_filter_keys.append("avgmaxtemp = %(avg_maxtemp)s")
        insert_keys.append("%(avg_maxtemp)s")
        query_filter_values["avg_maxtemp"] = avg_maxtemp

        query_filter_keys.append("avgmintemp = %(avg_mintemp)s")
        insert_keys.append("%(avg_mintemp)s")
        query_filter_values["avg_mintemp"] = avg_mintemp

        query_filter_keys.append(
            "totalprecipitation = %(total_precipitation)s")
        insert_keys.append("%(total_precipitation)s")
        query_filter_values["total_precipitation"] = total_precipitation

        filter_query = " and ".join(query_filter_keys)
        insert_query = ", ".join(insert_keys)
        params = db_config()
        conn = psycopg2.connect(**params)
        curr = conn.cursor()

        query = f""" 
                    INSERT INTO weatherstats (
                        stationid, 
                        year, 
                        avgmaxtemp, 
                        avgmintemp, 
                        totalprecipitation ) 
                    SELECT {insert_query} WHERE NOT EXISTS ( SELECT stationid, year FROM weatherstats WHERE {filter_query} )
                """
        curr.execute(query, query_filter_values)
        conn.commit()
        logging.info(
            f'Inserted/Updated data into Weather stats database successfully for stationid {stationid} and year {year}')
    except (Exception, psycopg2.DatabaseError) as e:
        raise CustomException(e, sys)
    finally:
        if conn is not None:
            curr.close()
            conn.close()
