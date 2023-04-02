import pandas as pd
import plotly.graph_objs as go
import json

def get_figure(indicatorCode, json_response_list):
    f = open('world_bank_app/data/indicators.json')
    indicators_list = json.load(f)
    f.close()

    countries = []
    values = []
    for item in json_response_list:
        if (item['value']):
            countries.append(item['country']['value'])
            values.append(item['value'])

    if len(countries) == 0:
       return None

    graph = []
    graph.append(
        go.Bar(
        x = countries,
        y = values,
        )
    )

    indicatorName = ''
    for indicator in indicators_list:
       if indicatorCode == indicator['code']:
          indicatorName = indicator['name']
          break

    layout = dict(title = indicatorName,
            xaxis = dict(title = 'Country',),
            yaxis = dict(title = 'Value'),
            )
    
    return dict(data=graph, layout=layout)