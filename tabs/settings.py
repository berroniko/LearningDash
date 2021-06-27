import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
from collections import defaultdict
from databasehandler import DataBaseHandler
from dash.exceptions import PreventUpdate
from app import app

DBH = DataBaseHandler(db_name="test_database")
# query_result = DBH.settings.find({})
# set_dic={}
# set_dic["CATS France"]=DBH.settings.find_one({"name": "CATS France"})["setting"]

size_left = 7
size_right = 4

layout = dbc.Container([
    dbc.Row(dbc.Col(html.H3("Data sources"),
                    width={'size': 12, 'offset': 0},
                    className="mt-4"
                    ),
            ),
    dbc.Row(dbc.Col(html.Div("Address and status of data sources"),
                    width=12
                    )
            ),

    # --------------------------------------------------------------------------       request      ----------
    html.Div([
        dbc.Row(
            [
                dbc.Col(html.H4("Request"),
                        width={'size': size_left, "offset": 0}
                        ),
                dbc.Col(html.Div(["status: 16.06.2021",
                                  dbc.Badge("up to date", pill=True, color="success", className="ml-2")]),
                        width={'size': size_right, 'offset': 1}
                        ),
            ]
        ),
        dbc.Row([
            dbc.Col(
                dbc.InputGroup(
                    [
                        dbc.InputGroupAddon("Sheet_id", addon_type="prepend"),
                        dbc.Input(placeholder="l2345shjadf5azld3andvn"),
                    ],
                    className="mb-3",
                    size="md"
                ),
                width={'size': size_left, "offset": 0}
            )
        ]),
        dbc.Row([
            dbc.Col(
                dbc.InputGroup(
                    [
                        dbc.InputGroupAddon("tab name", addon_type="prepend"),
                        dbc.Input(placeholder="Tab_1"),
                    ],
                    className="mb-3",
                    size="md"
                ),
                width={'size': size_left, "offset": 0}
            ),
            dbc.Col(
                dbc.InputGroup(
                    [
                        dbc.InputGroupAddon("range", addon_type="prepend"),
                        dbc.Input(placeholder="A1:Q151"),
                    ],
                    className="mb-3",
                    size="md"
                ),
                width={'size': size_right, "offset": 1},
            )
        ]),
    ], className='mt-4'),
    # --------------------------------------------------------------------------       request  one row   ------
    dbc.Row([
        dbc.Col([
            html.H4("Request in one row", className='mt-4'),
            dbc.InputGroup(
                [
                    dbc.InputGroupAddon("Sheet_id", addon_type="prepend"),
                    dbc.Input(placeholder="l2345shjadf5azld3andvn"),
                ], className="mb-3"
            ),
            dbc.InputGroup(
                [
                    dbc.InputGroupAddon("tab name", addon_type="prepend"),
                    dbc.Input(placeholder="Tab_1"),
                ], className="mb-3"
            ),
        ], width={'size': 4, "offset": 0}
        ),
        dbc.Col([
            html.P(
                [
                    "status: 16.06.2021",
                    dbc.Badge("up to date", pill=True, color="success", className="ml-2")
                ], className="mt-3",
            ),
            dbc.InputGroup(
                [
                    dbc.InputGroupAddon("range", addon_type="prepend"),
                    dbc.Input(placeholder="A1:Q151"),
                ], className="mb-3"
            ),
        ], width={'size': 3, 'offset': 1}
        ),
    ]),

    # -------------------- CATS
    html.Div([
        dbc.Row(
            [
                dbc.Col(html.H4(["CATS"]),
                        width={'size': 7, "offset": 0},
                        ),
                dbc.Col(
                    html.Div(["status: 16.06.2021", dbc.Badge("error", pill=True, color="warning", className="ml-2")]),
                    width={'size': 4, "offset": 1}
                    )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            dbc.Input(id="input", placeholder="existing filename", type="text", bs_size="md",
                                      className="mb-3"),
                            dbc.FormText("CATS Germany"),
                            html.Br(),
                            html.P(id="output")
                        ]
                    ),
                    width={'size': 12, "offset": 0},
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            dbc.Input(id="cats_f",
                                      type="text", bs_size="md",
                                      className="mb-3", debounce=True),
                            dbc.FormText("CATS France"),
                            html.Br(),
                            html.P(id="output")
                        ]
                    ),
                    width={'size': 12, "offset": 0},
                )
            ]
        )
    ], className='mt-4'),

    # -------------------- CnB
    html.Div([
        dbc.Row(
            [
                dbc.Col(html.H4(["Click n'Buy"]),
                        width={'size': size_left, "offset": 0},
                        ),
                dbc.Col(html.Div(["status: 05.06.2021",
                                  dbc.Badge("database", pill=True, color="primary", className="ml-2")]),
                        width={'size': size_right, "offset": 1},
                        )
            ]
        )
    ], className='mt-4'),
    # --------------------- whatever filepath

])


@app.callback(
    Output("cats_f", "placeholder"),
    # Output("cats_f", "placeholder"),
    [Input("cats_f", "value")])
def send_to_mongo(value):
    if value is None:
        return DBH.settings.find_one({"name": "CATS France"})["setting"]
    else:
        result = DBH.settings.replace_one({"name": "CATS France"}, {"name": "CATS France", "setting": value}, upsert=True)
        return value
