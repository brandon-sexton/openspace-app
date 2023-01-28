from dash import html, dcc, register_page, callback, page_registry
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from openspace.propagators.relative import Hill
from openspace.coordinates.states import HCW
from openspace.math.linalg import Vector6D
from openspace.math.constants import SECONDS_IN_DAY, BASE_IN_KILO


register_page(__name__, title='Relative Motion', name='Relative Motion')

figure = {
    'data':[
        {'type':'scatter3d', 'mode':'lines', 'line':{'color':'darkcyan'}, 'name':'Chase'},
        {'type':'scatter3d', 'mode':'markers', 'marker':{'color':'darkmagenta'}, 'name':'Target'}
    ],
    'layout':go.Layout(
        autosize=True,
        uirevision='constant',
        template='plotly_dark',
        scene={
            'xaxis':{'range':[-300, 300], 'title':'radial'},
            'yaxis':{'range':[-300, 300], 'title':'in-track'},
            'zaxis':{'range':[-300, 300], 'title':'cross-track'}
        }
    ),
}

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

content_column = dbc.Col(
    [
        html.H2('3-D Relative Motion Visualization and Planning'),
        dbc.InputGroup(
            [
                dbc.Input(id='r-pos-input', type='number', value=0, persistence=True, style={'width':'16.666%'}),
                dbc.Input(id='i-pos-input', type='number', value=0, persistence=True, style={'width':'16.666%'}),
                dbc.Input(id='c-pos-input', type='number', value=0, persistence=True, style={'width':'16.666%'}),
                dbc.Input(id='r-vel-input', type='number', value=0, persistence=True, style={'width':'16.666%'}),
                dbc.Input(id='i-vel-input', type='number', value=0, persistence=True, style={'width':'16.666%'}),
                dbc.Input(id='c-vel-input', type='number', value=0, persistence=True, style={'width':'16.666%'}),
            ]
        ),
        dbc.InputGroup(
            [
                dbc.InputGroupText(dcc.Markdown(r'$x (km)$', mathjax=True), style={'width':'16.666%'}),
                dbc.InputGroupText(dcc.Markdown(r'$y (km)$', mathjax=True), style={'width':'16.666%'}),
                dbc.InputGroupText(dcc.Markdown(r'$z (km)$', mathjax=True), style={'width':'16.666%'}),
                dbc.InputGroupText(dcc.Markdown(r'$\dot x (\frac{m}{s})$', mathjax=True), style={'width':'16.666%'}),
                dbc.InputGroupText(dcc.Markdown(r'$\dot y (\frac{m}{s})$', mathjax=True), style={'width':'16.666%'}),
                dbc.InputGroupText(dcc.Markdown(r'$\dot z (\frac{m}{s})$', mathjax=True), style={'width':'16.666%'}),
            ],
        ),
        dcc.Graph(id='rel-plot', responsive=True, style={'width':'100%','height':'100%',}, figure=figure)
    ]
)
layout = html.Div(
    dbc.Row(
        [
            nav_column,
            content_column
        ],
        style={'width':'100%','height':'100vh',}
    ),
)

@callback(
    Output('rel-plot', 'figure'),
    [
        Input('r-pos-input', 'value'), 
        Input('i-pos-input', 'value'), 
        Input('c-pos-input', 'value'), 
        Input('r-vel-input', 'value'), 
        Input('i-vel-input', 'value'), 
        Input('c-vel-input', 'value'),
    ],
    [
        State('sma', 'data'),
        State('rel-plot', 'figure'),
    ]
)
def update_plot(r, i, c, vr, vi, vc, sma, figure):
    m_to_km = 1/BASE_IN_KILO
    input_hcw: HCW = HCW.from_state_vector(Vector6D(r, i, c, vr*m_to_km, vi*m_to_km, vc*m_to_km))
    prop = Hill(input_hcw, sma)
    total_time = 0
    dt = prop.step_size
    r, i, c = [], [], []
    prop.step_by_seconds(-SECONDS_IN_DAY*.5)

    while total_time < SECONDS_IN_DAY:
        prop.step()
        r.append(prop.state.position.x)
        i.append(prop.state.position.y)
        c.append(prop.state.position.z)
        total_time+=dt

    figure = {
        'data':[
            {'x':r, 'y':i, 'z':c, 'type':'scatter3d', 'mode':'lines', 'line':{'color':'darkcyan'}, 'name':'Chase'},
            {'x':[0], 'y':[0], 'z':[0], 'type':'scatter3d', 'mode':'markers', 'marker':{'color':'darkmagenta'}, 'name':'Target'}
        ],
        'layout':go.Layout(
            autosize=True,
            uirevision='constant',
            template='plotly_dark',
            scene={
                'xaxis':{'range':[-300, 300], 'title':'radial'},
                'yaxis':{'range':[-300, 300], 'title':'in-track'},
                'zaxis':{'range':[-300, 300], 'title':'cross-track'}
            }
        ),
    }


    return figure

@callback(
    [
        Output('r-pos', 'data'),
        Output('i-pos', 'data'),
        Output('c-pos', 'data'),
    ],
    [
        Input('r-pos-input', 'value'), 
        Input('i-pos-input', 'value'), 
        Input('c-pos-input', 'value'), 
    ],
)
def update_position(r, i, c):
    return r, i, c

@callback(
    [
        Output('r-vel', 'data'),
        Output('i-vel', 'data'),
        Output('c-vel', 'data'),
    ],
    [
        Input('r-vel-input', 'value'), 
        Input('i-vel-input', 'value'), 
        Input('c-vel-input', 'value'), 
    ],
)
def update_velocity(r, i, c):
    return r/BASE_IN_KILO, i/BASE_IN_KILO, c/BASE_IN_KILO