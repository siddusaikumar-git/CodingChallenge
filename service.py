from flask import Flask, request
from flask.json import jsonify
# from flask_cors import CORS

from src.components import data_analysis

app = Flask(__name__)
# CORS(app)


@app.route('/api/weather', methods=['GET'])
def summary():
    date = request.args.get('date')
    stationid = request.args.get('stationid')
    page = request.args.get('page')
    result = text_prompt_input(data["publication_title"])
    return result


@app.route('/api/weather/stats', methods=['GET'])
def image():
    data = request.get_json()
    result = image_prompt_input(data["image_prompt"])
    return result


if __name__ == '__main__':
    app.run(debug=True)
