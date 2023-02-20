import dash_bootstrap_components as dbc

nav_column = dbc.Col(
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Dashboard", href="/")),
            dbc.NavItem(dbc.NavLink("Relative", href="/cw")),
            dbc.NavItem(dbc.NavLink("Inertial", href="/inertial")),
            dbc.NavItem(dbc.NavLink("Estimation", href="/od")),
            dbc.NavItem(dbc.NavLink("Hardware", href="/hardware")),
            dbc.NavItem(dbc.NavLink("Documentation", href="https://www.openspace-docs.com")),
            dbc.NavItem(dbc.NavLink("Source Code", href="https://github.com/brandon-sexton/")),
        ],
        vertical="sm",
        pills=True,
    ),
    width="auto",
)
