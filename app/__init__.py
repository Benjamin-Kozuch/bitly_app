from flask import Flask, jsonify
from config import Config
from app.bitly_api import average_clicks_per_country


app = Flask(__name__)
app.config.from_object(Config)


@app.route('/avg_clicks_per_country', defaults={'access_token': None})
@app.route('/avg_clicks_per_country/<access_token>')
def avg_clicks_per_country(access_token):
    access_token = access_token or app.config['ACCESS_TOKEN']
    avg_clicks = average_clicks_per_country(access_token)
    return jsonify(dict(data=avg_clicks))