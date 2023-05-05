from src.components.data_ingestion import DataIngestion
from src.components.data_modeling import DataModeling

if __name__ == '__main__':
    di = DataIngestion()
    di.insert_files_to_db()
