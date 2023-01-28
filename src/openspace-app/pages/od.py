from dash import html, dcc, register_page, callback, page_registry
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from openspace.propagators.relative import Hill
from openspace.coordinates.states import HCW, GCRF, StateConvert
from openspace.math.linalg import Vector6D
from openspace.math.constants import SECONDS_IN_DAY, BASE_IN_KILO
from openspace.bodies.artificial import Spacecraft
from openspace.time import Epoch
from openspace.math.linalg import Vector3D

register_page(__name__, title='State Estimation', name='State Estimation')

nav_column = dbc.Col(
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Dashboard", href='/')),
            dbc.NavItem(dbc.NavLink("Relative Motion", href='/cw')),
            dbc.NavItem(dbc.NavLink("Inertial View", href='/inertial')),
            dbc.NavItem(dbc.NavLink("State Estimation", href='/od')),
        ],
        vertical="sm",
        pills=True
    ),
    width='auto'
)

figure = {
    'data':[
        {'type':'scatter3d', 'mode':'markers', 'marker':{'color':'darkmagenta'}, 'name':'Target'},
        {'type':'scatter3d', 'mode':'lines', 'line':{'color':'darkcyan'}, 'name':'Truth'}, 
        {'type':'scatter3d', 'mode':'lines', 'line':{'color':'firebrick'}, 'name':'Observed'},  
    ],
    'layout':go.Layout(
        autosize=True,
        uirevision='constant',
        template='plotly_dark',
    ),
}
layout = html.Div(
    dbc.Row(
        [
            nav_column,
            dbc.Col(
                [
                    html.H2('Filter Performance'),
                    dcc.Graph(id='od-plot', responsive=True, style={'width':'100%','height':'100%'}, figure=figure),
                ]
            ),
        ],
        style={'width':'100%','height':'100vh',}
    ),
)

@callback(
    Output('od-plot', 'figure'),
    [
        Input('target-x', 'data'), 
        Input('target-y', 'data'), 
        Input('target-z', 'data'), 
        Input('target-vx', 'data'), 
        Input('target-vy', 'data'), 
        Input('target-vz', 'data'), 
        Input('year', 'data'), 
        Input('month', 'data'), 
        Input('day', 'data'), 
        Input('hour', 'data'), 
        Input('minute', 'data'), 
        Input('second', 'data'), 
        Input('r-pos', 'data'), 
        Input('i-pos', 'data'),
        Input('c-pos', 'data'),
        Input('r-vel', 'data'),
        Input('i-vel', 'data'),
        Input('c-vel', 'data'),
    ],
    State('od-plot', 'figure')
)
def update_plot(x, y, z, vx, vy, vz, yr, mon, day, hrs, mins, secs, r, i, c, vr, vi, vc, figure):
    ep = Epoch.from_gregorian(yr, mon, day, hrs, mins, secs)
    tgt = Spacecraft(GCRF(ep, Vector3D(x, y, z), Vector3D(vx, vy, vz)))
    chase = Spacecraft(StateConvert.hcw.to_gcrf(HCW.from_state_vector(Vector6D(r, i, c, vr, vi, vc)), tgt.current_state()))
    tgt.step_to_epoch(ep.plus_days(-.5))
    chase.step_to_epoch(ep.plus_days(-.5))
    end_ep = ep.plus_days(.5)

    seed = Spacecraft(GCRF(ep, Vector3D(x+.5, y+.5, z+.5), Vector3D(vx, vy, vz)))
    seed.step_to_epoch(ep.plus_days(-.5))
    chase.acquire(seed)
    tx, ty, tz, cx, cy, cz = [], [], [], [], [], []
    while tgt.current_epoch().value < end_ep.value:
        tgt.step()
        chase.step()
        chase.process_wfov(tgt)

        rel_truth = tgt.hill_position(chase)
        tx.append(-chase.filter.propagator.state.position.x)
        ty.append(-chase.filter.propagator.state.position.y)
        tz.append(-chase.filter.propagator.state.position.z)
        cx.append(rel_truth.x)
        cy.append(rel_truth.y)
        cz.append(rel_truth.z)

    figure = {
        'data':[
            {'x':[0], 'y':[0], 'z':[0], 'type':'scatter3d', 'mode':'markers', 'marker':{'color':'darkmagenta'}, 'name':'Target'},
            {'x':cx, 'y':cy, 'z':cz, 'type':'scatter3d', 'mode':'lines', 'line':{'color':'darkcyan'}, 'name':'Truth'}, 
            {'x':tx, 'y':ty, 'z':tz, 'type':'scatter3d', 'mode':'lines', 'line':{'color':'firebrick'}, 'name':'Observed'},  
        ],
        'layout':go.Layout(
            autosize=True,
            uirevision='constant',
            template='plotly_dark',
        ),
    }


    return figure