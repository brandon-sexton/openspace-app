import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import callback, dcc, html, register_page
from dash.dependencies import Input, Output, State
from openspace.bodies.artificial import Spacecraft
from openspace.coordinates.states import GCRF, HCW, StateConvert
from openspace.math.linalg import Vector3D, Vector6D
from openspace.time import Epoch

from openspace_app.widgets import nav_column

register_page(__name__, title="OTK - Inertial", name="inertial")

figure = {
    "data": [
        {"type": "scatter3d", "mode": "markers", "marker": {"color": "blue"}, "name": "Earth"},
        {"type": "scatter3d", "mode": "lines", "line": {"color": "darkmagenta"}, "name": "Target"},
        {"type": "scatter3d", "mode": "lines", "line": {"color": "darkcyan"}, "name": "Chase"},
    ],
    "layout": go.Layout(
        autosize=True,
        uirevision="constant",
        template="plotly_dark",
    ),
}

layout = dbc.Container(
    [
        html.Br(),
        dbc.Row(
            [
                nav_column,
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.H2("Inertial Visualization"),
                                dbc.FormText(
                                    "This view shows how the target and chase state look independent of each other."
                                ),
                            ]
                        ),
                        dcc.Graph(
                            id="eci-plot", responsive=True, figure=figure, style={"width": "100%", "height": "80%"}
                        ),
                    ],
                    className="content-container",
                ),
            ],
            style={"height": "100vh"},
        ),
    ]
)


@callback(
    Output("eci-plot", "figure"),
    [
        Input("target-x", "data"),
        Input("target-y", "data"),
        Input("target-z", "data"),
        Input("target-vx", "data"),
        Input("target-vy", "data"),
        Input("target-vz", "data"),
        Input("target-epoch", "data"),
        Input("r-pos", "data"),
        Input("i-pos", "data"),
        Input("c-pos", "data"),
        Input("r-vel", "data"),
        Input("i-vel", "data"),
        Input("c-vel", "data"),
    ],
    State("eci-plot", "figure"),
)
def update_plot(x, y, z, vx, vy, vz, tgt_ep, r, i, c, vr, vi, vc, figure):
    ep = Epoch(tgt_ep)
    tgt = Spacecraft(GCRF(ep, Vector3D(x, y, z), Vector3D(vx, vy, vz)))
    chase = Spacecraft(
        StateConvert.hcw.to_gcrf(HCW.from_state_vector(Vector6D(r, i, c, vr, vi, vc)), tgt.current_state())
    )
    end_ep = ep.plus_days(1)

    tx, ty, tz, cx, cy, cz = [], [], [], [], [], []
    while tgt.current_epoch().value < end_ep.value:
        tgt.step()
        chase.step()
        tx.append(tgt.position().x)
        ty.append(tgt.position().y)
        tz.append(tgt.position().z)
        cx.append(chase.position().x)
        cy.append(chase.position().y)
        cz.append(chase.position().z)

    figure = {
        "data": [
            {
                "x": [0],
                "y": [0],
                "z": [0],
                "type": "scatter3d",
                "mode": "markers",
                "marker": {"color": "blue"},
                "name": "Earth",
            },
            {
                "x": tx,
                "y": ty,
                "z": tz,
                "type": "scatter3d",
                "mode": "lines",
                "line": {"color": "darkmagenta"},
                "name": "Target",
            },
            {
                "x": cx,
                "y": cy,
                "z": cz,
                "type": "scatter3d",
                "mode": "lines",
                "line": {"color": "darkcyan"},
                "name": "Chase",
            },
        ],
        "layout": go.Layout(
            autosize=True,
            uirevision="constant",
            template="plotly_dark",
        ),
    }

    return figure
