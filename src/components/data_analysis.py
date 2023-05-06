from src.components.data_modeling import DataModeling


class DataAnalysis:

    def __init__(self) -> None:
        pass

    def get_weather_stats(self, params):
        dm = DataModeling()

        result = {"total_count": 0, "results": [],
                  "nextLink": None, "prevLink": None}

        stationid = params.get("stationid", None)
        year = params.get("year", None)
        page = int(params.get("page", 1))
        query_params = []
        link = f'http://127.0.0.1:5000/api/weather/stats?'
        if stationid:
            query_params.append(f'stationid={stationid}')
        if year:
            query_params.append(f'year={year}')

        link += '&'.join(query_params)
        result["nextLink"] = link + "&page=" + str(page+1)

        if page > 1:
            result["prevLink"] = link + "&page=" + str(page-1)

        response = dm.get_weather_stats_from_db(
            stationid=stationid, year=year, page=page)

        if response:
            result["total_count"] = response[0]["total_count"]
            result["results"] = list(
                map(lambda x: {k: v for k, v in x.items() if k != 'total_count'}, response))
        return result

    def get_weather_details():
        pass
