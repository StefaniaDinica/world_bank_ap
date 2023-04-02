from world_bank_app import app
from flask import render_template, request, jsonify
from .wrangling.wrangle_data import get_figure
import json
import os
import requests
import plotly

@app.route('/', methods=['GET', 'POST'])
def index():
    f = open('world_bank_app/data/euro_countries.json')
    countries_list = json.load(f)
    f.close()

    f = open('world_bank_app/data/indicators.json')
    indicators_list = json.load(f)
    f.close()

    f = open('world_bank_app/data/years.json')
    years_list = json.load(f)
    f.close()

    print(request)

    return render_template('index.html',
                           countries_list=countries_list,
                           indicators_list=indicators_list,
                           years_list = years_list)

@app.route('/generate-plots/', methods=['POST'])
def generatePlots():
    print(request.json)
    
    indicators = request.json['indicators']
    countries = request.json['countries']
    year = request.json['year']

    figures = []

    for indicator in indicators:
        url = 'https://api.worldbank.org/v2/country/' + ";".join(countries) + '/indicator/' + indicator + '?format=json&date=' + year

        try:
            r = requests.get(url)
            # data[indicator] = r.json()[1]
            figure = get_figure(indicator, r.json()[1])
            if figure:
                figures.append(figure)

        except Exception as e:
            print(e)
            print('could not load data')

    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return figuresJSON