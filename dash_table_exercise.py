import dash
from dash.dependencies import Input, Output, State
import dash_table
import dash_html_components as html
import pandas as pd
from dash.exceptions import PreventUpdate

filepath = "data_table.csv"
with open(filepath) as infile:
    df = pd.read_csv(infile, sep=",")

cols = [{'name': str(i), 'id': str(i)} for i in df.keys()]
data_values = df.to_dict('records')

app = dash.Dash(__name__)

app.layout = html.Div([
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
            row['Total'] = sum([float(value) for key, value in row.items() if key not in ['CPN', 'Total', 'output-data']])
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
        # pass
    else:
        dfres = pd.DataFrame(data)
        dfres.to_csv(filepath, index=False, header=True)
        return "Table saved"


if __name__ == '__main__':
    app.run_server(debug=True)