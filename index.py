import dash
import dash_html_components as html
import dash_core_components as dcc

from dash.dependencies import Input, Output

from tabs import dash_table_exercise

from app import app

# app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Table', value='tab-1'),
        dcc.Tab(label='Graph', value='tab-2'),
    ]),
    html.Div(id='tabs-content')
])

@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return dash_table_exercise.layout
    elif tab == 'tab-2':
        return html.Div([
            dcc.Graph(
                figure={
                    'data': [
                        {'x': [1, 2, 3], 'y': [1, 4, 1],
                         'type': 'bar', 'name': 'SF'},
                        {'x': [1, 2, 3], 'y': [1, 2, 3],
                         'type': 'bar', 'name': u'Montréal'},
                    ]
                }
            )
        ])


if __name__ == '__main__':
    app.run_server(debug=True)