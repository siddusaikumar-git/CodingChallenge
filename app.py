from flask import Flask, request
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from src.components.data_analysis import get_weather_stats, get_weather_data

app = Flask(__name__)
CORS(app)


SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'My API'
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


@app.route('/api/weather', methods=['GET'])
def weather_data():
    params_dict = {}
    if "year" in request.args:
        params_dict["year"] = request.args.get('year')
    if "stationid" in request.args:
        params_dict["stationid"] = request.args.get('stationid')
    if "page" in request.args:
        params_dict["page"] = request.args.get('page')
    response = get_weather_data(params_dict)
    return response


@app.route('/api/weather/stats', methods=['GET'])
def weather_stats():
    params_dict = {}
    if "year" in request.args:
        params_dict["year"] = request.args.get('year')
    if "stationid" in request.args:
        params_dict["stationid"] = request.args.get('stationid')
    if "page" in request.args:
        params_dict["page"] = request.args.get('page')
    response = get_weather_stats(params_dict)
    return response


if __name__ == '__main__':
    app.run(debug=True)
