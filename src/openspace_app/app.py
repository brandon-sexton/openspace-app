import webbrowser
from threading import Timer

import dash
import dash_bootstrap_components as dbc
import flask
from dash import Dash, dcc, html

from openspace_app.configs import LAYOUT_BG_STYLE

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.CYBORG], server=flask.Flask(__name__))

content_column = dbc.Col(
    [
        dcc.Store(id="r-pos", storage_type="local", data=0),
        dcc.Store(id="i-pos", storage_type="local", data=0),
        dcc.Store(id="c-pos", storage_type="local", data=0),
        dcc.Store(id="r-vel", storage_type="local", data=0),
        dcc.Store(id="i-vel", storage_type="local", data=0),
        dcc.Store(id="c-vel", storage_type="local", data=0),
        dcc.Store(id="year", storage_type="local", data=0),
        dcc.Store(id="month", storage_type="local", data=0),
        dcc.Store(id="day", storage_type="local", data=0),
        dcc.Store(id="hour", storage_type="local", data=0),
        dcc.Store(id="minute", storage_type="local", data=0),
        dcc.Store(id="second", storage_type="local", data=0),
        dcc.Store(id="target-x", storage_type="local", data=0),
        dcc.Store(id="target-y", storage_type="local", data=0),
        dcc.Store(id="target-z", storage_type="local", data=0),
        dcc.Store(id="target-vx", storage_type="local", data=0),
        dcc.Store(id="target-vy", storage_type="local", data=0),
        dcc.Store(id="target-vz", storage_type="local", data=0),
        dcc.Store(id="sma", storage_type="local", data=0),
        dash.page_container,
    ],
)
app.layout = html.Div(
    [
        html.Img(
            src=dash.get_asset_url("openspace-header.png"),
            style={"width": "100%", "margin-bottom": "1%", "background-color": "#010332"},
        ),
        dbc.Row([content_column]),
    ],
    style=LAYOUT_BG_STYLE,
)


def run():
    host = "localhost"
    port = 8080
    url = f"http://{host}:{port}"
    Timer(10, webbrowser.open_new(url))

    # run app
    app.run(host=host, port=port, debug=False)


if __name__ == "__main__":
    run()
