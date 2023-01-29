import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback, dcc, html, register_page
from openspace.bodies.celestial import Earth
from openspace.coordinates.states import GCRF, HCW, StateConvert
from openspace.math.functions import EquationsOfMotion
from openspace.math.linalg import Vector3D, Vector6D
from openspace.time import Epoch

from openspace_app.configs import CONTENT_STYLE, LAYOUT_BG_STYLE, NAV_STYLE

register_page(__name__, path="/", title="Dashboard", name="Dashboard")
config_accordion = dbc.Accordion(
    [
        dbc.AccordionItem(
            [
                html.P("This epoch represents the time at which the target state is valid.  Inputs are in TDT."),
                dbc.InputGroup(
                    [
                        dbc.Input(
                            id="year-input", type="number", value=2023, persistence=True, style={"width": "16.666%"}
                        ),
                        dbc.Input(
                            id="month-input", type="number", value=1, persistence=True, style={"width": "16.666%"}
                        ),
                        dbc.Input(
                            id="day-input", type="number", value=26, persistence=True, style={"width": "16.666%"}
                        ),
                        dbc.Input(
                            id="hour-input", type="number", value=12, persistence=True, style={"width": "16.666%"}
                        ),
                        dbc.Input(
                            id="minute-input", type="number", value=30, persistence=True, style={"width": "16.666%"}
                        ),
                        dbc.Input(
                            id="second-input", type="number", value=0, persistence=True, style={"width": "16.666%"}
                        ),
                    ]
                ),
                dbc.InputGroup(
                    [
                        dbc.InputGroupText("year", style={"width": "16.666%"}),
                        dbc.InputGroupText("month", style={"width": "16.666%"}),
                        dbc.InputGroupText("day", style={"width": "16.666%"}),
                        dbc.InputGroupText("hour", style={"width": "16.666%"}),
                        dbc.InputGroupText("minute", style={"width": "16.666%"}),
                        dbc.InputGroupText("second", style={"width": "16.666%"}),
                    ],
                ),
            ],
            title="Epoch",
        ),
        dbc.AccordionItem(
            [
                html.P(
                    "This state will act as the origin when defining the chase vehicle's state.  Inputs are in the \
                    GCRF frame"
                ),
                dbc.InputGroup(
                    [
                        dbc.Input(
                            id="target-input-x",
                            type="number",
                            value=42164,
                            persistence=True,
                            style={"width": "16.666%"},
                        ),
                        dbc.Input(
                            id="target-input-y", type="number", value=0, persistence=True, style={"width": "16.666%"}
                        ),
                        dbc.Input(
                            id="target-input-z", type="number", value=0, persistence=True, style={"width": "16.666%"}
                        ),
                        dbc.Input(
                            id="target-input-vx", type="number", value=0, persistence=True, style={"width": "16.666%"}
                        ),
                        dbc.Input(
                            id="target-input-vy",
                            type="number",
                            value=3.074,
                            persistence=True,
                            style={"width": "16.666%"},
                        ),
                        dbc.Input(
                            id="target-input-vz", type="number", value=0, persistence=True, style={"width": "16.666%"}
                        ),
                    ]
                ),
                dbc.InputGroup(
                    [
                        dbc.InputGroupText(dcc.Markdown(r"$x (km)$", mathjax=True), style={"width": "16.666%"}),
                        dbc.InputGroupText(dcc.Markdown(r"$y (km)$", mathjax=True), style={"width": "16.666%"}),
                        dbc.InputGroupText(dcc.Markdown(r"$z (km)$", mathjax=True), style={"width": "16.666%"}),
                        dbc.InputGroupText(
                            dcc.Markdown(r"$\dot x (\frac{km}{s})$", mathjax=True), style={"width": "16.666%"}
                        ),
                        dbc.InputGroupText(
                            dcc.Markdown(r"$\dot y (\frac{km}{s})$", mathjax=True), style={"width": "16.666%"}
                        ),
                        dbc.InputGroupText(
                            dcc.Markdown(r"$\dot z (\frac{km}{s})$", mathjax=True), style={"width": "16.666%"}
                        ),
                    ],
                ),
            ],
            title="Target State",
        ),
        dbc.AccordionItem(
            [
                html.P(
                    "This represents the chase vehicle's state in the inertial frame.  Direct edits cannot be made \
                    here.  Instead, use the relative motion tab."
                ),
                dbc.InputGroup(
                    [
                        dbc.InputGroupText("", style={"width": "16.666%"}, id="chase-text-x"),
                        dbc.InputGroupText("", style={"width": "16.666%"}, id="chase-text-y"),
                        dbc.InputGroupText("", style={"width": "16.666%"}, id="chase-text-z"),
                        dbc.InputGroupText("", style={"width": "16.666%"}, id="chase-text-vx"),
                        dbc.InputGroupText("", style={"width": "16.666%"}, id="chase-text-vy"),
                        dbc.InputGroupText("", style={"width": "16.666%"}, id="chase-text-vz"),
                    ]
                ),
                dbc.InputGroup(
                    [
                        dbc.InputGroupText(dcc.Markdown(r"$x (km)$", mathjax=True), style={"width": "16.666%"}),
                        dbc.InputGroupText(dcc.Markdown(r"$y (km)$", mathjax=True), style={"width": "16.666%"}),
                        dbc.InputGroupText(dcc.Markdown(r"$z (km)$", mathjax=True), style={"width": "16.666%"}),
                        dbc.InputGroupText(
                            dcc.Markdown(r"$\dot x (\frac{km}{s})$", mathjax=True), style={"width": "16.666%"}
                        ),
                        dbc.InputGroupText(
                            dcc.Markdown(r"$\dot y (\frac{km}{s})$", mathjax=True), style={"width": "16.666%"}
                        ),
                        dbc.InputGroupText(
                            dcc.Markdown(r"$\dot z (\frac{km}{s})$", mathjax=True), style={"width": "16.666%"}
                        ),
                    ],
                ),
            ],
            title="Chase State",
        ),
    ],
    style={"width": "90%"},
)
content_column = dbc.Col(
    [
        html.P(
            "Openspace is an opensource solution to training and education of space operations. \
            The backend library can be installed from a command line using 'pip install openspace' or by downloading \
            the source code from https://github.com/brandon-sexton/openspace.  For information on backend \
            capabilities, visit https://www.openspace-docs.com.  For questions, function requests, or to report \
            an issue, please e-mail brandon.sexton.1@outlook.com.  Otherwise, select a widget link from the \
            toolbar to get started."
        ),
        config_accordion,
    ],
    style=CONTENT_STYLE,
)

nav_column = dbc.Col(
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Dashboard", href="/")),
            dbc.NavItem(dbc.NavLink("Relative Motion", href="/cw")),
            dbc.NavItem(dbc.NavLink("Inertial View", href="/inertial")),
            dbc.NavItem(dbc.NavLink("State Estimation", href="/od")),
            dbc.NavItem(dbc.NavLink("Documentation", href="https://www.openspace-docs.com")),
            dbc.NavItem(dbc.NavLink("Source Code", href="https://github.com/brandon-sexton/")),
        ],
        vertical="sm",
        pills=True,
    ),
    width="auto",
    style=NAV_STYLE,
)

layout = html.Div([dbc.Row([nav_column, content_column], style={"height": "100%"})], style=LAYOUT_BG_STYLE)


@callback(
    [
        Output("chase-text-x", "children"),
        Output("chase-text-y", "children"),
        Output("chase-text-z", "children"),
        Output("chase-text-vx", "children"),
        Output("chase-text-vy", "children"),
        Output("chase-text-vz", "children"),
        Output("sma", "data"),
        Output("target-x", "data"),
        Output("target-y", "data"),
        Output("target-z", "data"),
        Output("target-vx", "data"),
        Output("target-vy", "data"),
        Output("target-vz", "data"),
        Output("year", "data"),
        Output("month", "data"),
        Output("day", "data"),
        Output("hour", "data"),
        Output("minute", "data"),
        Output("second", "data"),
    ],
    [
        Input("year-input", "value"),
        Input("month-input", "value"),
        Input("day-input", "value"),
        Input("hour-input", "value"),
        Input("minute-input", "value"),
        Input("second-input", "value"),
        Input("target-input-x", "value"),
        Input("target-input-y", "value"),
        Input("target-input-z", "value"),
        Input("target-input-vx", "value"),
        Input("target-input-vy", "value"),
        Input("target-input-vz", "value"),
    ],
    [
        State("r-pos", "data"),
        State("i-pos", "data"),
        State("c-pos", "data"),
        State("r-vel", "data"),
        State("i-vel", "data"),
        State("c-vel", "data"),
    ],
)
def update_chase(yr, mon, day, hrs, mins, secs, x, y, z, vx, vy, vz, r, i, c, vr, vi, vc):
    ep: Epoch = Epoch.from_gregorian(yr, mon, day, hrs, mins, secs)
    tgt: GCRF = GCRF(ep, Vector3D(x, y, z), Vector3D(vx, vy, vz))
    hill: HCW = HCW.from_state_vector(Vector6D(r, i, c, vr, vi, vc))
    chase: GCRF = StateConvert.hcw.to_gcrf(hill, tgt)
    sma: float = EquationsOfMotion.A.from_mu_r_v(Earth.MU, tgt.position.magnitude(), tgt.velocity.magnitude())
    cx = "%.6f" % chase.position.x
    cy = "%.6f" % chase.position.y
    cz = "%.6f" % chase.position.z
    cvx = "%.6f" % chase.velocity.x
    cvy = "%.6f" % chase.velocity.y
    cvz = "%.6f" % chase.velocity.z
    return cx, cy, cz, cvx, cvy, cvz, sma, x, y, z, vx, vy, vz, yr, mon, day, hrs, mins, secs
