import os
import sys
import time
from src.components.data_modeling import DataModeling
from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass


@dataclass
class DataIngestionConfig:
    file_location: str = os.path.join('artifacts', 'wx_data')


class DataIngestion:
    def __init__(self):
        self.filelocation = DataIngestionConfig().file_location

    def clean_row_data(self, line):
        rowData = [int(col.strip()) for col in line.split("\t")]
        for index in range(1, len(rowData)):
            if rowData[index] == -9999:
                rowData[index] = None
        return rowData

    def insert_data_from_file_to_db(self, filename, stationid, model_obj):
        try:
            linesToInsert = []
            with open(os.path.join(self.filelocation, filename), 'r', encoding='utf-8') as fp:
                lines = fp.readlines()

            for line in lines:
                rowData = self.clean_row_data(line)
                id = stationid + str(rowData[0])
                year = int(rowData[0]) / 10000
                linesToInsert.append(
                    (id, stationid, rowData[0], year,
                     rowData[1], rowData[2], rowData[3])
                )
            numberOfRecords = len(linesToInsert)
            start_time = time.time()
            model_obj.insertMany(linesToInsert)
            end_time = time.time()
            numberOfSeconds = end_time - start_time
            logging.info(
                f"Data from station {stationid} is ingested with {numberOfRecords} records in {numberOfSeconds:.2f} seconds into database successfully with start time {time.asctime(time.localtime(start_time))} and end time {time.asctime(time.localtime(end_time))}")
            print(
                f"Data from station {stationid} is ingested with {numberOfRecords} records in {numberOfSeconds:.2f} seconds into database successfully with start time {time.asctime(time.localtime(start_time))} and end time {time.asctime(time.localtime(end_time))}")
        except (Exception) as e:
            raise CustomException(e, sys)

    def insert_files_to_db(self):
        try:
            model_obj = DataModeling()
            for filename in os.listdir(self.filelocation):
                if filename.endswith('.txt'):
                    stationid = filename.split(".")[0]
                    if model_obj.validate_station_data(stationid):
                        logging.info(
                            f"station {stationid} insertion is skipped as it is already present in database")
                        print(
                            f"station {stationid} insertion is skipped as it is already present in database")
                        continue
                    self.insert_data_from_file_to_db(
                        filename=filename, stationid=stationid, model_obj=model_obj)
                else:
                    continue
        except (Exception) as e:
            raise CustomException(e, sys)
