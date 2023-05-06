from flask import Flask, request
from flask.json import jsonify
# from flask_cors import CORS

from src.components.data_analysis import DataAnalysis

app = Flask(__name__)
# CORS(app)


# @app.route('/api/weather', methods=['GET'])
# def summary():
#     date = request.args.get('date')
#     stationid = request.args.get('stationid')
#     page = request.args.get('page')
#     result = text_prompt_input(data["publication_title"])
#     return result


@app.route('/api/weather/stats', methods=['GET'])
def weather_stats():
    da = DataAnalysis()
    params_dict = {}
    if "year" in request.args:
        params_dict["year"] = request.args.get('year')
    if "stationid" in request.args:
        params_dict["stationid"] = request.args.get('stationid')
    if "page" in request.args:
        params_dict["page"] = request.args.get('page')
    response = da.get_weather_stats(params_dict)
    return response


if __name__ == '__main__':
    app.run(debug=True)
