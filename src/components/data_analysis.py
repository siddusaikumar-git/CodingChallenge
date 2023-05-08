import sys
from src.components.data_modeling import get_weather_stats_from_db, get_weather_data_from_db, insert_weather_stats_to_db
from config import page_config, url_config
from src.exception import CustomException
from src.logger import logging

"""
    This function is used to generate "prevLink" and "nextLink" based on page number and total record count
"""


def generate_links(page_no, total_records_count, link):
    try:
        prevLink, nextLink = None, None
        page_params = page_config()

        numOf_records_per_page = int(page_params["page_count"])
        numOf_records_start_offset = numOf_records_per_page * (page_no - 1)
        numOf_records_end_offset = numOf_records_per_page * page_no

        if (page_no == 1):
            if (total_records_count > numOf_records_end_offset):
                nextLink = link + "&page=" + str(page_no + 1)
            return prevLink, nextLink
        elif ((total_records_count > numOf_records_start_offset) and (total_records_count > numOf_records_end_offset)):
            prevLink = link + "&page=" + str(page_no - 1)
            nextLink = link + "&page=" + str(page_no + 1)
            return prevLink, nextLink
        elif (numOf_records_end_offset >= total_records_count > numOf_records_start_offset):
            prevLink = link + "&page=" + str(page_no - 1)
            return prevLink, nextLink
        else:
            return prevLink, nextLink
    except Exception as error:
        raise CustomException(error, sys)


"""
    This function is to insert input request to weatherstats table in weather dababase with the help of 
    insert_weather_stats_to_db function from data_modeling.py file
"""


def insert_weather_stats_results(results):
    try:
        for result in results:
            stationid = result["stationid"]
            year = result["year"]
            total_precipitation = result["total_precipitation"]
            avg_maxtemp = result["avg_maxtemp"]
            avg_mintemp = result["avg_mintemp"]

            insert_weather_stats_to_db(
                stationid=stationid, year=year, total_precipitation=total_precipitation, avg_maxtemp=avg_maxtemp, avg_mintemp=avg_mintemp)
    except Exception as error:
        raise CustomException(error, sys)


"""
    This function is get weather statistics from the weatherdata table in weather dababase based on input query params with the help of 
    get_weather_stats_from_db function from data_modeling.py file
"""


def get_weather_stats(params):
    try:
        url_params = url_config()
        result = {"total_count": 0, "results": [],
                  "nextLink": None, "prevLink": None, "message": "No results found for request query"}

        stationid = params.get("stationid", None)
        year = params.get("year", None)
        page = int(params.get("page", 1))
        query_params = []
        link = f'{url_params["url"]}/api/weather/stats?'
        if stationid:
            query_params.append(f'stationid={stationid}')
        if year:
            query_params.append(f'year={year}')

        link += '&'.join(query_params)

        response = get_weather_stats_from_db(
            stationid=stationid, year=year, page=page)

        if response:
            result["total_count"] = response["total_count"]
            if response["results"]:
                result["prevLink"], result["nextLink"] = generate_links(
                    page, response["total_count"], link)
                result["message"] = "Successfully retrieved the results"
                insert_weather_stats_results(response["results"])
            result["results"] = response["results"]

        return result
    except Exception as error:
        raise CustomException(error, sys)


"""
    This function is get weather data from the weatherdata table in weather dababase based on input query params with the help of 
    get_weather_data_from_db function from data_modeling.py file
"""


def get_weather_data(params):
    try:
        url_params = url_config()
        result = {"total_count": 0, "results": [],
                  "nextLink": None, "prevLink": None, "message": "No results found for request query"}

        stationid = params.get("stationid", None)
        year = params.get("year", None)
        page = int(params.get("page", 1))
        query_params = []
        link = f'{url_params["url"]}/api/weather?'
        if stationid:
            query_params.append(f'stationid={stationid}')
        if year:
            query_params.append(f'year={year}')

        link += '&'.join(query_params)

        response = get_weather_data_from_db(
            stationid=stationid, year=year, page=page)

        if response:
            result["total_count"] = response["total_count"]
            if response["results"]:
                result["prevLink"], result["nextLink"] = generate_links(
                    page, response["total_count"], link)
                result["message"] = "Successfully retrieved the results"
            result["results"] = response["results"]
        return result
    except Exception as error:
        raise CustomException(error, sys)
