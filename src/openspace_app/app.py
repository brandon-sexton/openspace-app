import webbrowser
from threading import Timer

import dash
import dash_bootstrap_components as dbc
import flask
from dash import Dash, dcc, html

app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP, "\\assets\\css\\custom-style.css"],
    server=flask.Flask(__name__),
    title="OTK - Home",
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

app.layout = dbc.Container(
    [
        html.Br(),
        dbc.Row(
            html.Img(className="header-img", src=dash.get_asset_url("img/openspace-header.png")),
        ),
        dbc.Row(
            dash.page_container,
        ),
        dcc.Store(id="r-pos", storage_type="session", data=0),
        dcc.Store(id="i-pos", storage_type="session", data=0),
        dcc.Store(id="c-pos", storage_type="session", data=0),
        dcc.Store(id="r-vel", storage_type="session", data=0),
        dcc.Store(id="i-vel", storage_type="session", data=0),
        dcc.Store(id="c-vel", storage_type="session", data=0),
        dcc.Store(id="target-epoch", storage_type="session", data=0),
        dcc.Store(id="year-input", storage_type="session", data=0),
        dcc.Store(id="month-input", storage_type="session", data=0),
        dcc.Store(id="day-input", storage_type="session", data=0),
        dcc.Store(id="hour-input", storage_type="session", data=0),
        dcc.Store(id="minute-input", storage_type="session", data=0),
        dcc.Store(id="second-input", storage_type="session", data=0),
        dcc.Store(id="target-x", storage_type="session", data=0),
        dcc.Store(id="target-y", storage_type="session", data=0),
        dcc.Store(id="target-z", storage_type="session", data=0),
        dcc.Store(id="target-vx", storage_type="session", data=0),
        dcc.Store(id="target-vy", storage_type="session", data=0),
        dcc.Store(id="target-vz", storage_type="session", data=0),
        dcc.Store(id="sma", storage_type="session", data=0),
    ],
)


def run():
    host = "localhost"
    port = 8888
    url = f"http://{host}:{port}"
    Timer(10, webbrowser.open_new(url))

    # run app
    app.run(host=host, port=port, debug=False)


if __name__ == "__main__":
    run()
