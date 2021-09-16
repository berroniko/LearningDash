from dash.dependencies import Input, Output, State
import dash_table
import dash_html_components as html
import pandas as pd
from dash.exceptions import PreventUpdate
from app import app
from databasehandler import DataBaseHandler
from dash_table.Format import Format, Scheme
import dash_bootstrap_components as dbc


DBH = DataBaseHandler(db_name="test_database")
query_result = DBH.alloc.find({})
data_values = [e for e in query_result]
col_total = dict(id='Total', name='Total', type='numeric', format=Format(precision=0, scheme=Scheme.fixed))
cols = [col_total if i == "Total" else {'id': str(i), 'name': str(i)} for i in data_values[0]]

for elem in cols:
    if elem["name"] == "_id":
        elem["name"] = "CPN"

layout = html.Div([
    dash_table.DataTable(
        id='computed-table',
        columns=cols,
        data=data_values,  # the contents of the table
        editable=True,  # allow editing of data inside all cells
        filter_action="native",  # allow filtering of data by user ('native') or not ('none')
        sort_action="native",  # enables data to be sorted per-column by user or not ('none')
        sort_mode="single",  # sort across 'multi' or 'single' columns
        column_selectable="multi",  # allow users to select 'multi' or 'single' columns
        row_selectable="multi",  # allow users to select 'multi' or 'single' rows
        selected_columns=[],  # ids of columns that user selects
        selected_rows=[],  # indices of rows that user selects
        page_action="native",  # all data is passed to the table up-front or not ('none')
        # export_format="csv",
        # export_headers='ids',
        style_cell={  # ensure adequate header width when text is shorter than cell's text
            'minWidth': 40, 'maxWidth': 95, 'width': 50
        },
        style_data_conditional=[
            {
                'if': {
                    'column_id': 'Total',
                },
                'backgroundColor': 'grey',
                'color': 'white'
            }
        ]
    ),
    html.Br(),
    html.Button('Save', id='save-button'),
    html.Br(),
    html.Div(id='output-state')
])


@app.callback(
    Output('computed-table', 'data'),
    Input('computed-table', 'data_timestamp'),
    State('computed-table', 'data'))
def update_columns(timestamp, rows):
    for row in rows:
        try:
            row['Total'] = sum([float(value) for key, value in row.items() if key not in [
                'CPN', '_id', 'Total', 'lastModified']])
        except:
            row['Total'] = 'NA'
    return rows


@app.callback(
    Output('output-state', 'children'),
    Input('computed-table', 'data'),
    Input('save-button', 'n_clicks')
)
def submit_action(data, n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        # changed data become a string and are converted back to float before saving them to the database
        data_float = [{k: (float(v) if k not in ['CPN', '_id', 'lastModified'] else v) for k, v in elem.items()}
                      for elem in data]
        DBH.fill_update(DBH.alloc, data_float)
        return "Table saved"
