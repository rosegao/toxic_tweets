# Project: Toxic Tweets
# Filename: demo_plotly_dashboard.py
# Author: Rose Gao

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import plotly
import plotly.graph_objs as go
import plotly.plotly as py
import plotly.dashboard_objs as dashboard
import IPython.display
from IPython.display import Image

def df_processing(filename):
    df = pd.read_csv(filename, encoding = "ISO-8859-1")
    df = df.drop('Unnamed: 0', 1)
    df = df.dropna()
    return df

def create_traces(df):
    trace1 = go.Scatter(x=df['date'], y=df['toxic'], marker={'color': 'blue', 'symbol': 104, 'size': "5"},
                        mode="markers", name='1st Trace')
    data = go.Data([trace1])
    url_1 = py.plot(data, filename='first_plot', sharing='public', auto_open=False)

    trace2 = go.Scatter(x=df['date'], y=df['severe_toxic'], marker={'color': 'purple', 'symbol': 104, 'size': "5"},
                        mode="markers", name='2nd Trace')
    data = go.Data([trace2])
    url_2 = py.plot(data, filename='second_plot', sharing='public', auto_open=False)

    trace3 = go.Scatter(x=df['date'], y=df['obscene'], marker={'color': 'orange', 'symbol': 104, 'size': "5"},
                        mode="markers", name='3rd Trace')
    data = go.Data([trace3])
    url_3 = py.plot(data, filename='third_plot', sharing='public', auto_open=False)

    trace4 = go.Scatter(x=df['date'], y=df['threat'], marker={'color': 'green', 'symbol': 104, 'size': "5"},
                        mode="markers", name='4th Trace')
    data = go.Data([trace4])
    url_4 = py.plot(data, filename='fourth_plot', sharing='public', auto_open=False)

    trace5 = go.Scatter(x=df['date'], y=df['insult'], marker={'color': 'red', 'symbol': 104, 'size': "5"},
                        mode="markers", name='5th Trace')
    data = go.Data([trace5])
    url_5 = py.plot(data, filename='fifth_plot', sharing='public', auto_open=False)

    trace6 = go.Scatter(x=df['date'], y=df['identity_hate'], marker={'color': 'blue', 'symbol': 104, 'size': "5"},
                        mode="markers", name='6th Trace')
    data = go.Data([trace6])
    url_6 = py.plot(data, filename='sixth_plot', sharing='public', auto_open=False)

    urls = [url_1, url_2, url_3, url_4, url_5, url_6]
    return urls

def parse_fileId(url):
    '''
    Derive fileID of plot from plot's url
    '''
    split = url.split("/")
    username = split[-2][1:]
    number = split[-1]
    return username + ":" + number

def get_fileIds(urls):
    fileIds = []
    for i in urls:
        fileIds.append(parse_fileId(i))

    return fileIds

def create_boxes(fileIds):
    box_1 = {
        'type': 'box',
        'boxType': 'plot',
        'fileId': fileIds[0],
        'title': 'Toxic Plot'
    }

    box_2 = {
        'type': 'box',
        'boxType': 'plot',
        'fileId': fileIds[1],
        'title': 'Severe Toxic Plot'
    }

    box_3 = {
        'type': 'box',
        'boxType': 'plot',
        'fileId': fileIds[2],
        'title': 'Obscene Plot'
    }

    box_4 = {
        'type': 'box',
        'boxType': 'plot',
        'fileId': fileIds[3],
        'title': 'Threat Plot'
    }

    box_5 = {
        'type': 'box',
        'boxType': 'plot',
        'fileId': fileIds[4],
        'title': 'Insult Plot'
    }

    box_6 = {
        'type': 'box',
        'boxType': 'plot',
        'fileId': fileIds[5],
        'title': 'Identity Hate Plot'
    }

    boxes = [box_1, box_2, box_3, box_4, box_5, box_6]
    return boxes

def create_dashboard(boxes):
    # create dashboard
    demo_dashboard = dashboard.Dashboard()

    # name dashboard
    demo_dashboard['settings']['title'] = 'Tweet Toxicity Dashboard'

    # unpack boxes
    box_1, box_2, box_3, box_4, box_5, box_6 = boxes

    # insert boxes
    demo_dashboard.insert(box_1)
    demo_dashboard.insert(box_2, 'right', 1)
    demo_dashboard.insert(box_3, 'below', 1)
    demo_dashboard.insert(box_4, 'below', 3)
    demo_dashboard.insert(box_5, 'below', 2)
    demo_dashboard.insert(box_6, 'below', 5)

    return demo_dashboard

if __name__ == '__main__':
    num_args = len(sys.argv)

    if num_args != 2:
        print("usage: python " + sys.argv[0] + " <classified tweets csv>")
        sys.exit(0)

    filename = sys.argv[1]
    df = df_processing(filename)

    plotly.tools.set_credentials_file(username='rose.gao6', api_key='9ivalbyhazaM1JEEaHaZ')
    urls = create_traces(df)
    fileIds = get_fileIds(urls)
    boxes = create_boxes(fileIds)
    demo_dashboard = create_dashboard(boxes)
    py.dashboard_ops.upload(demo_dashboard, 'Tweet Toxicity Dashboard')