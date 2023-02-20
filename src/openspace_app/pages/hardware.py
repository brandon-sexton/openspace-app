from math import atan, cos, pi, sin

import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import callback, ctx, dcc, get_asset_url, html, register_page
from dash.dependencies import Input, Output, State

from openspace_app.widgets import nav_column

deg2rad = pi / 180
rad2deg = 180 / pi
moon_size = 0.52
circle_range = range(0, 361)
unit_x, unit_y = [cos(d * deg2rad) for d in circle_range], [sin(d * deg2rad) for d in circle_range]

register_page(__name__, title="OTK - Hardware", name="hardware")

figure = dict(
    data=[
        dict(x=[], y=[], type="scatter", mode="lines", line=dict(color="darkcyan"), name="Image Circle"),
        dict(x=[], y=[], type="scatter", mode="lines", line=dict(color="darkmagenta"), name="Sensor Frame"),
        dict(x=[], y=[], type="scatter", mode="lines", line=dict(color="grey"), showlegend=False),
    ],
    layout=go.Layout(
        autosize=True,
        uirevision="constant",
        template="plotly_dark",
        yaxis=dict(scaleanchor="x", scaleratio=1, showticklabels=False, showgrid=False, zeroline=False),
        xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        annotations=[{}, {}, {}],
        images=[{}],
    ),
)

content_column = dbc.Col(
    [
        dbc.Label("Telescope"),
        dbc.InputGroup(
            [
                dbc.InputGroupText("Image Circle Diameter (mm)", class_name="input-text-label"),
                dbc.Input(id="img-diameter", type="number", value=42, persistence=True, class_name="input-text"),
            ],
        ),
        dbc.InputGroup(
            [
                dbc.InputGroupText("Focal Length (mm)", class_name="input-text-label"),
                dbc.Input(id="focal-length", type="number", value=360, persistence=True, class_name="input-text"),
            ]
        ),
        dbc.Label("Sensor"),
        dbc.InputGroup(
            [
                dbc.InputGroupText("Sensor Width (mm)", class_name="input-text-label"),
                dbc.Input(id="sensor-x", type="number", value=13.2, persistence=True, class_name="input-text"),
            ]
        ),
        dbc.InputGroup(
            [
                dbc.InputGroupText("Sensor Height (mm)", class_name="input-text-label"),
                dbc.Input(id="sensor-y", type="number", value=8.8, persistence=True, class_name="input-text"),
            ]
        ),
        dcc.Graph(id="sensor-plot", responsive=True, figure=figure, style={"width": "100%", "height": "70%"}),
    ],
    className="content-container",
)

layout = dbc.Container(
    [
        html.Br(),
        dbc.Row(
            [nav_column, content_column],
            style={"height": "100vh"},
        ),
    ],
)


@callback(
    Output("sensor-plot", "figure"),
    [
        Input("img-diameter", "value"),
        Input("sensor-x", "value"),
        Input("sensor-y", "value"),
        Input("focal-length", "value"),
    ],
    State("sensor-plot", "figure"),
)
def update_sensor_plot(d: float, w: float, h: float, flen: float, figure):

    if ctx.triggered_id == "img-diameter":
        r = d * 0.5
        fov = atan(d / flen) * rad2deg
        fovx = w / d * fov
        fovy = h / d * fov
        figure["data"][0]["x"], figure["data"][0]["y"] = [r * x for x in unit_x], [r * y for y in unit_y]
        figure["data"][2]["x"], figure["data"][2]["y"] = [-r, r], [r * 1.1, r * 1.1]
        figure["layout"]["annotations"][0] = dict(x=0, y=r * 1.1, text="%.3f degrees" % fov)
        figure["layout"]["annotations"][1] = dict(x=0, y=-h * 0.5, ayref="y", ay=-h * 0.7, text="%.3f degrees" % fovx)
        figure["layout"]["annotations"][2] = dict(x=w * 0.5, y=0, axref="x", ax=w * 0.7, text="%.3f degrees" % fovy)
        moon = moon_size / fov * d
        figure["layout"]["images"][0] = dict(
            source=get_asset_url("img/moon.png"),
            xref="x",
            yref="y",
            sizex=moon,
            sizey=moon,
            x=-moon * 0.5,
            y=moon * 0.5,
            layer="below",
        )
    elif ctx.triggered_id == "sensor-x":
        fov = atan(d / flen) * rad2deg
        fovx = w / d * fov
        fovy = h / d * fov
        figure["data"][1]["x"] = [-w * 0.5, w * 0.5, w * 0.5, w * 0.5, 0, -w * 0.5, -w * 0.5]
        figure["layout"]["annotations"][1] = dict(x=0, y=-h * 0.5, ayref="y", ay=-h * 0.7, text="%.3f degrees" % fovx)
        figure["layout"]["annotations"][2] = dict(x=w * 0.5, y=0, axref="x", ax=w * 0.7, text="%.3f degrees" % fovy)
    elif ctx.triggered_id == "sensor-y":
        fov = atan(d / flen) * rad2deg
        fovx = w / d * fov
        fovy = h / d * fov
        figure["data"][1]["y"] = [h * 0.5, h * 0.5, 0, -h * 0.5, -h * 0.5, -h * 0.5, h * 0.5]
        figure["layout"]["annotations"][1] = dict(x=0, y=-h * 0.5, ayref="y", ay=-h * 0.7, text="%.3f degrees" % fovx)
        figure["layout"]["annotations"][2] = dict(x=w * 0.5, y=0, axref="x", ax=w * 0.7, text="%.3f degrees" % fovy)
    elif ctx.triggered_id == "focal-length":
        r = d * 0.5
        fov = atan(d / flen) * rad2deg
        fovx = w / d * fov
        fovy = h / d * fov
        figure["layout"]["annotations"][0] = dict(x=0, y=r * 1.1, text="%.3f degrees" % fov)
        figure["layout"]["annotations"][1] = dict(x=0, y=-h * 0.5, ayref="y", ay=-h * 0.7, text="%.3f degrees" % fovx)
        figure["layout"]["annotations"][2] = dict(x=w * 0.5, y=0, axref="x", ax=w * 0.7, text="%.3f degrees" % fovy)
        moon = moon_size / fov * d
        figure["layout"]["images"][0] = dict(
            source=get_asset_url("img/moon.png"),
            xref="x",
            yref="y",
            sizex=moon,
            sizey=moon,
            x=-moon * 0.5,
            y=moon * 0.5,
            layer="below",
        )
    elif len(figure["data"][0]["x"]) == 0:
        r = d * 0.5
        fov = atan(d / flen) * rad2deg
        fovx = w / d * fov
        fovy = h / d * fov
        figure["data"][0]["x"], figure["data"][0]["y"] = [r * x for x in unit_x], [r * y for y in unit_y]
        figure["data"][1]["x"] = [-w * 0.5, w * 0.5, w * 0.5, w * 0.5, 0, -w * 0.5, -w * 0.5]
        figure["data"][1]["y"] = [h * 0.5, h * 0.5, 0, -h * 0.5, -h * 0.5, -h * 0.5, h * 0.5]
        figure["data"][2]["x"], figure["data"][2]["y"] = [-r, r], [r * 1.1, r * 1.1]
        figure["layout"]["annotations"][0] = dict(x=0, y=r * 1.1, text="%.3f degrees" % fov)
        figure["layout"]["annotations"][1] = dict(x=0, y=-h * 0.5, ayref="y", ay=-h * 0.7, text="%.3f degrees" % fovx)
        figure["layout"]["annotations"][2] = dict(x=w * 0.5, y=0, axref="x", ax=w * 0.7, text="%.3f degrees" % fovy)
        moon = moon_size / fov * d
        figure["layout"]["images"][0] = dict(
            source=get_asset_url("img/moon.png"),
            xref="x",
            yref="y",
            sizex=moon,
            sizey=moon,
            x=-moon * 0.5,
            y=moon * 0.5,
            layer="below",
        )

    return figure
