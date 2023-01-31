import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback, dcc, html, register_page
from openspace.bodies.celestial import Earth
from openspace.coordinates.states import GCRF, HCW, StateConvert
from openspace.math.functions import EquationsOfMotion
from openspace.math.linalg import Vector3D, Vector6D
from openspace.time import Epoch

register_page(__name__, path="/", title="Dashboard", name="Dashboard")
config_accordion = dbc.Accordion(
    [
        dbc.AccordionItem(
            [
                dbc.Label("Target Epoch"),
                dbc.Input(
                    id="target-epoch-input",
                    persistence=True,
                    type="text",
                    className="epoch-input",
                    value="2023-01-30 12:00:00",
                ),
                dbc.FormText(
                    "This epoch represents the time at which the target state is valid.  Inputs are in Terrestrial \
                    Dynamic Time (TDT).  "
                ),
                dbc.Label("Format:  YYYY-MM-DD hh:mm:ss"),
            ],
            title="Epochs",
        ),
        dbc.AccordionItem(
            [
                dbc.Label("Target State"),
                dbc.InputGroup(
                    [
                        dbc.Input(
                            id="target-input-x",
                            type="number",
                            value=42164,
                            persistence=True,
                            className="vector6d-field",
                        ),
                        dbc.Input(
                            id="target-input-y", type="number", value=0, persistence=True, className="vector6d-field"
                        ),
                        dbc.Input(
                            id="target-input-z", type="number", value=0, persistence=True, className="vector6d-field"
                        ),
                        dbc.Input(
                            id="target-input-vx", type="number", value=0, persistence=True, className="vector6d-field"
                        ),
                        dbc.Input(
                            id="target-input-vy",
                            type="number",
                            value=3.074,
                            persistence=True,
                            className="vector6d-field",
                        ),
                        dbc.Input(
                            id="target-input-vz", type="number", value=0, persistence=True, className="vector6d-field"
                        ),
                    ]
                ),
                dbc.FormText(
                    " This state will act as the origin when defining the chase vehicle's \
                    state.  Inputs are in the GCRF frame."
                ),
                html.Br(),
                dbc.Label("Chase State", style={"margin-top": "5%"}),
                dbc.Row(
                    [
                        dbc.Col(dbc.FormText(id="chase-text-x")),
                        dbc.Col(dbc.FormText(id="chase-text-y")),
                        dbc.Col(dbc.FormText(id="chase-text-z")),
                        dbc.Col(dbc.FormText(id="chase-text-vx")),
                        dbc.Col(dbc.FormText(id="chase-text-vy")),
                        dbc.Col(dbc.FormText(id="chase-text-vz")),
                    ]
                ),
                dbc.FormText(
                    "This represents the chase vehicle's state in the inertial frame.  Direct edits cannot be made \
                    here.  Instead, use the relative motion tab."
                ),
                html.Br(),
                dbc.Label("Format:", style={"margin-top": "5%"}),
                dbc.Row(
                    [
                        dbc.Col(dcc.Markdown(r"$x (km)$", mathjax=True)),
                        dbc.Col(dcc.Markdown(r"$y (km)$", mathjax=True)),
                        dbc.Col(dcc.Markdown(r"$z (km)$", mathjax=True)),
                        dbc.Col(dcc.Markdown(r"$\dot x (\frac{km}{s})$", mathjax=True)),
                        dbc.Col(dcc.Markdown(r"$\dot y (\frac{km}{s})$", mathjax=True)),
                        dbc.Col(dcc.Markdown(r"$\dot z (\frac{km}{s})$", mathjax=True)),
                    ]
                ),
            ],
            title="States",
        ),
    ],
)
content_column = dbc.Col(
    [
        dbc.FormText(
            "Openspace is an opensource solution to training and education of space operations. \
            The backend library can be installed from a command line using 'pip install openspace' or by downloading \
            the source code from https://github.com/brandon-sexton/openspace.  For information on backend \
            capabilities, visit https://www.openspace-docs.com.  For questions, function requests, or to report \
            an issue, please e-mail brandon.sexton.1@outlook.com.  Otherwise, select a widget link from the \
            toolbar to get started.",
        ),
        config_accordion,
    ],
    className="content-container",
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
)

layout = dbc.Container([html.Br(), dbc.Row([nav_column, content_column])])


@callback(
    [
        Output("target-epoch", "data"),
        Output("target-epoch-input", "invalid"),
    ],
    Input("target-epoch-input", "value"),
    State("target-epoch", "data"),
)
def update_target_epoch(ep_str, tgt_ep):

    ep = tgt_ep
    invalid = False
    date_time = ep_str.split(" ")
    if len(date_time) < 2:
        invalid = True
    else:
        date_list = date_time[0].split("-")
        time_list = date_time[1].split(":")
        if len(date_list) < 3 or len(time_list) < 3:
            invalid = True
        else:
            year = float(date_list[0])
            month = float(date_list[1])
            day = float(date_list[2])

            hrs = float(time_list[0])
            mins = float(time_list[1])
            secs = float(time_list[2])
            if hrs >= 24 or hrs < 0:
                invalid = True
            elif mins >= 60 or mins < 0:
                invalid = True
            elif secs >= 60 or secs < 0:
                invalid = True
            elif year < 1858:
                invalid = True
            elif month < 1 or month > 12:
                invalid = True
            elif day < 0:
                invalid = True
            elif (month == 9 or month == 4 or month == 6 or month == 10) and day > 30:
                invalid = True
            elif month == 2 and day > 29:
                invalid = True

    if not invalid:
        ep = Epoch.from_gregorian(year, month, day, hrs, mins, secs)

    return invalid, ep


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
    ],
    [
        Input("target-epoch", "data"),
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
def update_chase(tgt_ep, x, y, z, vx, vy, vz, r, i, c, vr, vi, vc):

    ep: Epoch = Epoch(tgt_ep)
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
    return cx, cy, cz, cvx, cvy, cvz, sma, x, y, z, vx, vy, vz
