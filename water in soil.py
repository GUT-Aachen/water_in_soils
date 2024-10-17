import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import numpy as np
import plotly.graph_objs as go

app = dash.Dash(__name__)

# Add a hidden dcc.Store to track the window width
app.layout = html.Div([
    dcc.Store(id='window-width'),

    # Add the dcc.Interval component to track the window width
    dcc.Interval(id='interval', interval=1000, n_intervals=0),

    # Main container
    html.Div(style={'display': 'flex', 'flexDirection': 'row', 'width': '100%', 'height': '100vh'}, children=[
        # Control container (sliders)
        html.Div(id='control-container', style={'width': '25%', 'padding': '10px', 'flexDirection': 'column'}, children=[
            html.H1('Water in Soils', style={'textAlign': 'center'}),

            # Sliders for layer depths
            html.Div(className='slider-container', children=[
                html.Label(children=[
                    'Z', html.Sub('1'), ' (m)'
                ], className='slider-label'),  # Subscript for Z1
                dcc.Slider(
                    id='z-1', min=0, max=10, step=1, value=5,
                    marks={i: f'{i}' for i in range(0, 11, 2)},
                    className='slider', tooltip={'placement': 'bottom', 'always_visible': True}
                ),
            ]),
            html.Div(className='slider-container', children=[
                html.Label(children=[
                    'Z', html.Sub('2'), ' (m)'
                ], className='slider-label'),  # Subscript for Z2
                dcc.Slider(
                    id='z-2', min=0, max=5, step=1, value=2,
                    marks={i: f'{i}' for i in range(0, 6, 1)},
                    className='slider', tooltip={'placement': 'bottom', 'always_visible': True}
                ),
            ]),
            html.Div(className='slider-container', children=[
                html.Label(children=[
                    'Z', html.Sub('3'), ' (m)'
                ], className='slider-label'),  # Subscript for Z3
                dcc.Slider(
                    id='z-3', min=0, max=10, step=1, value=5,
                    marks={i: f'{i}' for i in range(0, 11, 2)},
                    className='slider', tooltip={'placement': 'bottom', 'always_visible': True}
                ),
            ]),
            # Dropdown for type selection
            html.Div(className='dropdown-container', children=[
                html.Label('Type', className='dropdown-label'),
                dcc.Dropdown(
                    id='type-dropdown',
                    options=[
                        {'label': 'Hydrostatic', 'value': 'hydrostatic'},
                        {'label': 'Undrained', 'value': 'undrained'},
                        {'label': 'artesian', 'value': 'artesian'}
                    ],
                    value='hydrostatic'  # Default 
                ),
            ]),
        ]),

        # Graphs container
        html.Div(className='graph-container', id='graphs-container', style={'display': 'flex', 'flexDirection': 'coloun', 'width': '75%'}, children=[
            html.Div(style={'width': '100%', 'height': '50%'}, children=[
                dcc.Graph(id='soil-layers-graph', style={'height': '100%', 'width': '100%'})
            ]),
            html.Div(style={'width': '100%', 'height': '50%'}, children=[
                dcc.Graph(id='pore-pressure-graph', style={'height': '100%', 'width': '100%'})
            ])
        ])
    ])
])



# JavaScript for updating window width
app.clientside_callback(
    """
    function(n_intervals) {
        return window.innerWidth;
    }
    """,
    Output('window-width', 'data'),
    Input('interval', 'n_intervals')
)

# Callback to update layout based on window width
@app.callback(
    [Output('graphs-container', 'style'), Output('control-container', 'style')],
    [Input('window-width', 'data')]
)
def update_layout(window_width):
    if window_width is not None and window_width < 700:
        # Stack graphs and controls vertically for narrow screens
        graph_style = {'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'width': '100%'}
        control_style = {'width': '100%', 'padding': '10px'}
    else:
        # Display sliders on the left and graphs on the right for wider screens
        graph_style = {'display': 'flex', 'flexDirection': 'column', 'width': '75%', 'gap': '0px'}
        control_style = {'width': '25%', 'padding': '10px'}
    
    return graph_style, control_style



# Callback to handle the animations and input updates
@app.callback(
    Output('soil-layers-graph', 'figure'),
    Output('pore-pressure-graph', 'figure'),\
    Input('type-dropdown', 'value'),
    Input('z-1', 'value'),
    Input('z-2', 'value'),
    Input('z-3', 'value')
)
def update_graphs(type, z1, z2, z3):
    if type == 'hydrostatic':
        z2= 0
    # Define soil layers and their boundaries
    layers = [
        {'name': 'Sand', 'top': 0, 'bottom': z1, 'color': 'lightblue', 'x0': -0.60},
        {'name': 'Clay', 'top': z1, 'bottom': z1 + z2, 'color': 'brown', 'x0': -0.55},
        {'name': 'Sand', 'top': z1 + z2, 'bottom': z1 + z2 + z3, 'color': 'lightblue', 'x0': -0.5},
    ]

    # Create the soil layers figure
    soil_layers_fig = go.Figure()

    for layer in layers:
        soil_layers_fig.add_trace(go.Scatter(
            x=[-1, -1, 1, 1],  # Create a rectangle-like shape
            y=[layer['top'], layer['bottom'], layer['bottom'], layer['top']],
            fill='toself',
            fillcolor=layer['color'],
            mode='lines',
            line=dict(width=1, color='black'),
            name=layer['name'],
            showlegend=True
        ))

        soil_layers_fig.add_shape(type="rect",
                xref="x", yref="y",
                x0=layer['x0'], y0=layer['bottom'],
                x1=layer['x0']+0.01, y1=0,
                line=dict(
                    color="RoyalBlue",
                    width=3,
                ),
                fillcolor='LightSkyBlue',
            )

    soil_layers_fig.update_layout(
        title='Soil Layers',
        xaxis_title='Width',
        yaxis_title='Depth (m)',
        yaxis=dict(autorange='reversed'),  # Reverse y-axis

    )

    # Calculate pore water pressure based on conditions
    depths = np.linspace(0, z1 + z2 + z3, 100)  # Define depths from 0 to total depth
    pore_pressure = np.zeros_like(depths)

    if z2 == 0:  # No clay layer (hydrostatic pressure)
        pore_pressure = depths * 9.81  # Hydrostatic pressure (ρg)
    else:
        # Handle the three cases
        for i, depth in enumerate(depths):
            if depth < z1:  # In the first layer
                pore_pressure[i] = depth * 9.81  # Hydrostatic pressure
            elif z1 <= depth < z1 + z2:  # In the clay layer
                pore_pressure[i] = z1 * 9.81  # Constant head
            else:  # In the second sand layer
                head_diff = z1 + z2 + z3 - depth
                if head_diff > 0:
                    pore_pressure[i] = (z1 + z2) * 9.81  # Head in layer 3 larger than layer 2
                else:
                    pore_pressure[i] = (z1 + z2 + z3) * 9.81  # Head in layer 3 less than layer 1

    # Create the pore pressure figure
    pore_pressure_fig = go.Figure()
    pore_pressure_fig.add_trace(go.Scatter(
        x=pore_pressure,
        y=depths,
        mode='lines',
        line=dict(color='blue'),
        name='Pore Water Pressure'
    ))

    pore_pressure_fig.update_layout(
        title='Pore Water Pressure with Depth',
        xaxis_title='Pore Water Pressure (Pa)',
        xaxis = dict(side = 'top'),
        yaxis_title='Depth (m)',
        yaxis=dict(autorange='reversed'),  # Reverse y-axis
    )

    return soil_layers_fig, pore_pressure_fig

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
