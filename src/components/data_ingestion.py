import os
import sys
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

    def insert_data_from_file_to_db(self, filename, stationid):
        try:
            linesToInsert = []
            with open(os.path.join(self.filelocation, filename), 'r', encoding='utf-8') as fp:
                lines = fp.readlines()

            for line in lines:
                rowData = self.clean_row_data(line)
                id = stationid + str(rowData[0])

                linesToInsert.append(
                    (id, stationid, rowData[0],
                     rowData[1], rowData[2], rowData[3])
                )
            dm = DataModeling()
            dm.insertMany(linesToInsert)
            logging.info(
                f"Data from station id {stationid} is inserted into database successfully")
        except (Exception) as e:
            raise CustomException(e, sys)

    def insert_files_to_db(self):
        try:
            for filename in os.listdir(self.filelocation):
                if filename.endswith('.txt'):
                    stationid = filename.split(".")[0]
                    dm = DataModeling()
                    if dm.validate_station_data(stationid):
                        logging.info(
                            f"station id {stationid} is already present in database")
                        continue
                    self.insert_data_from_file_to_db(
                        filename=filename, stationid=stationid)
                else:
                    continue
        except (Exception) as e:
            raise CustomException(e, sys)
