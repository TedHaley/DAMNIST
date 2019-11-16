import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
from dash_canvas import DashCanvas
import json
from dash_table import DataTable
from dash_canvas.utils import array_to_data_url, parse_jsonstring
import numpy as np
from dash.exceptions import PreventUpdate
from pprint import pprint

app = dash.Dash(__name__)

canvas_width = 1000
canvas_height = 1000

columns = ['type', 'width', 'height', 'scaleX', 'strokeWidth', 'path']

app.layout = html.Div([
    html.H6('Draw on image and press Save to show annotations geometry'),
    html.Div(
        [
            DashCanvas(id='annot-canvas',
                       lineWidth=5,
                       width=canvas_width,
                       height=canvas_height,
                       hide_buttons=["zoom", "pan", "line", "pencil", "rectangle", "undo", "select"])
        ],
        style={"width": "100%"}
    ),

    DataTable(id='annot-canvas-table',
              style_cell={'textAlign': 'left'},
              columns=[{"name": i, "id": i} for i in columns]),
    html.Div([
        html.Img(id='my-image',
                 width=canvas_width,
                 height=canvas_height),
    ]),
    # html.P()
])


@app.callback(Output('annot-canvas-table', 'data'),
              [Input('annot-canvas', 'json_data')])
def update_data(string):
    if string:
        data = json.loads(string)
    else:
        raise PreventUpdate
    return data['objects'][1:]


@app.callback(Output('my-image', 'src'),
              [Input('annot-canvas', 'json_data')])
def update_data(string):
    pprint(string)

    if string:
        mask = parse_jsonstring(string, (canvas_width, canvas_height))
    else:
        raise PreventUpdate

    return array_to_data_url((255 * mask).astype(np.uint8))


#
# @app.callback(Output('annot-canvas-table', 'data'),
#               [Input('annot-canvas', 'image_content')])
# def image_content(content):
#     if content:
#         print(content)


if __name__ == '__main__':
    app.run_server(debug=True)
