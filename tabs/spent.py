import dash_html_components as html
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from collections import defaultdict
from databasehandler import DataBaseHandler
from app import app

DBH = DataBaseHandler(db_name="test_database")

cpn_selection=["01-005985", "01-000123"]
pers_selection=["01565483", "0234982"]
query_result = DBH.cats.find({"cpn": {"$in": cpn_selection}, "pers": {"$in": pers_selection}})

# d=defaultdict(float)
# total=0
# for elem in query_result:
#     d[elem["week"]] += elem["hours"]
#     total += elem["hours"]

# find the available CPNs for dropdown
res = DBH.cpn.find({}, {"_id": 1}).sort("_id", 1)
available_cpns = [i["_id"] for i in list(res)]

layout = html.Div([
        dcc.Dropdown(
        id='cpn-dropdown',
        options=[
            {'label': i, 'value': i} for i in available_cpns
        ],
        placeholder='Select...',
        multi=True
    ),
            dcc.Graph(id='graph_weekly_booking'),
            html.Br(),
            html.Div(id='resulting_total')
    ])

@app.callback(
    Output('graph_weekly_booking', 'figure'),
    Output('resulting_total', 'children'),
    Input('cpn-dropdown', 'value'))
def update_graph(cpn_selection):
    query_result = DBH.cats.find({"cpn": {"$in": cpn_selection}})
    d = defaultdict(float)
    total = 0
    for elem in query_result:
        d[elem["week"]] += elem["hours"]
        total += elem["hours"]
    total = "total " + str(int(total)) + " hrs"

    figure = {
        'data': [{'x': list(d.keys()), 'y': list(d.values()),
                  'type': 'bar', 'name': 'test'}]
    }
    return figure, total
