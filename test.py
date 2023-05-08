import unittest
import json
from app import app
from src.components.data_ingestion import DataIngestion


# The following class consist of unit test functions to test the response from flask APIs
# We use the test client to send the GET request to the endpoints in the following functions
# and store the result in the "result" variable.
class UnitTest(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    # -----------------weather data api testing ------------------

    # This method tests the status code of a GET request to the endpoint "/api/weather".
    def test_weather_data_1(self):
        result = self.app.get("/api/weather")
        self.assertEqual(result.status_code, 200)

    # This method tests the status code of a GET request to the endpoint "/api/weather/data".
    def test_weather_data_2(self):
        result = self.app.get("/api/weather/data")
        self.assertEqual(result.status_code, 404)

    # This method tests the "results" value of a GET request to the endpoint "/api/weather?year=1900".
    def test_weather_data_3(self):
        result = self.app.get("/api/weather?year=1900")
        output = json.loads(result.data)
        self.assertEqual(output["results"], None)

    def test_weather_data_4(self):
        result = self.app.get(
            "/api/weather?year=2000&stationid=USC00110072&page=1")
        output = json.loads(result.data)
        self.assertEqual(output["total_count"], 366)

    def test_weather_data_5(self):
        result = self.app.get(
            "/api/weather?year=2000&stationid=USC00110072&page=2")
        output = json.loads(result.data)
        self.assertEqual(output["total_count"], 366)

    def test_weather_data_6(self):
        result = self.app.get(
            "/api/weather?year=2000&stationid=USC00110072&page=38")
        output = json.loads(result.data)
        self.assertEqual(output["results"], None)

    def test_weather_data_6(self):
        result = self.app.get(
            "/api/weather?year=2000&stationid=USC00110072&page=38")
        output = json.loads(result.data)
        self.assertEqual(output["results"], None)

    # -----------------weather statistics api testing ------------------

    # This method tests the status code of a GET request to the endpoint "/api/weather/stats".
    def test_weather_stats_1(self):
        result = self.app.get("/api/weather/stats")
        self.assertEqual(result.status_code, 200)

    # This method tests the status code of a GET request to the endpoint "/api/weather/stats/data".
    def test_weather_stats_2(self):
        result = self.app.get("/api/weather/stats/data")
        self.assertEqual(result.status_code, 404)

    # This method tests the GET request to the endpoint "/api/weather/stats?year=1900".
    def test_weather_stats_3(self):
        result = self.app.get(
            "/api/weather/stats?year=2000&stationid=USC00113879&page=1")
        output = json.loads(result.data)
        self.assertEqual(output['total_count'], 1)

    def test_weather_stats_4(self):
        result = self.app.get(
            "/api/weather/stats?year=2000&page=2")
        output = json.loads(result.data)
        self.assertEqual(output['total_count'], 166)

    def test_weather_stats_5(self):
        result = self.app.get(
            "/api/weather/stats?year=2000&page=18")
        output = json.loads(result.data)
        self.assertEqual(output['results'], None)

    # ----------- Insertion weather data to database --------------

    def test_ingestion_files_to_db(self):
        di = DataIngestion()
        response = di.insert_files_to_db()
        self.assertEqual(
            response, "Inserted all files into database successfully")


if __name__ == '__main__':
    unittest.main()
