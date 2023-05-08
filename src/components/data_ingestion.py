import os
import sys
import time
from datetime import datetime
from src.components.data_modeling import validate_station_data, insertMany
from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass


@dataclass
class DataIngestionConfig:
    file_location: str = os.path.join('artifacts', 'wx_data')


class DataIngestion:
    def __init__(self):
        self.filelocation = DataIngestionConfig().file_location

    """
        clean each line to list and convert the data to required datatype
    """

    def clean_row_data(self, line):
        try:
            rowData = [int(col.strip()) for col in line.split("\t")]
            for index in range(1, len(rowData)):
                if rowData[index] == -9999:
                    rowData[index] = None
            rowData[0] = datetime.strptime(str(rowData[0]), '%Y%m%d').date()
            return rowData
        except Exception as error:
            raise CustomException(error, sys)

    """
        This function is to insert data from text files (weather station) into database.

        It first perform clean operation with "clean_row_data" function, then will insert data to database
        by calling "insertMany" function from data_modeling.py file.
    """

    def insert_data_from_file_to_db(self, filename, stationid):
        try:
            linesToInsert = []
            with open(os.path.join(self.filelocation, filename), 'r', encoding='utf-8') as fp:
                lines = fp.readlines()

            for line in lines:
                rowData = self.clean_row_data(line)
                year = int(rowData[0].year)
                linesToInsert.append(
                    (stationid, rowData[0], year,
                     rowData[1], rowData[2], rowData[3])
                )
            numberOfRecords = len(linesToInsert)
            start_time = time.time()
            insertMany(linesToInsert)  # ingestion of records to database
            end_time = time.time()
            numberOfSeconds = end_time - start_time
            logging.info(
                f"Data from station {stationid} is ingested with {numberOfRecords} records in {numberOfSeconds:.2f} seconds into database successfully with start time {time.asctime(time.localtime(start_time))} and end time {time.asctime(time.localtime(end_time))}")
            # print(
            #     f"Data from station {stationid} is ingested with {numberOfRecords} records in {numberOfSeconds:.2f} seconds into database successfully with start time {time.asctime(time.localtime(start_time))} and end time {time.asctime(time.localtime(end_time))}")
        except (Exception) as error:
            raise CustomException(error, sys)

    """
        This function is to insert data from text files (weather station) into database.

        It will validate whether data is already present in database, if not present then will call insert_data_from_file_to_db function.
    """

    def insert_files_to_db(self):
        try:
            for filename in os.listdir(self.filelocation):
                if filename.endswith('.txt'):
                    stationid = filename.split(".")[0]
                    if validate_station_data(stationid):
                        logging.info(
                            f"station {stationid} insertion is skipped as it is already present in database")
                        # print(
                        #     f"station {stationid} insertion is skipped as it is already present in database")
                        continue
                    self.insert_data_from_file_to_db(
                        filename=filename, stationid=stationid)
                else:
                    continue
            logging.info("Inserted all files into database successfully")
            return "Inserted all files into database successfully"
        except (Exception) as error:
            raise CustomException(error, sys)
