import dash
import dash_html_components as html
import dash_core_components as dcc

from dash.dependencies import Input, Output

from tabs import dash_table_exercise
from tabs import spent
from tabs import settings

from app import app

app.layout = html.Div([
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Table', value='tab-1'),
        dcc.Tab(label='Graph', value='tab-2'),
        dcc.Tab(label='Sources', value='tab-3'),
    ]),
    html.Div(id='tabs-content')
])

@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return dash_table_exercise.layout
    elif tab == 'tab-2':
        return spent.layout
    elif tab == 'tab-3':
        return settings.layout


if __name__ == '__main__':
    app.run_server(debug=True)