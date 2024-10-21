import os
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import numpy as np
import plotly.graph_objs as go

app = dash.Dash(__name__)

# Add a hidden dcc.Store to track the window width
# Updated layout with separate sections for sliders and layer properties
# Updated layout with sliders on top and layer properties below
app.layout = html.Div([
    dcc.Store(id='window-width'),

    # Add the dcc.Interval component to track the window width
    dcc.Interval(id='interval', interval=1000, n_intervals=0),

    # Main container
    html.Div(style={'display': 'flex', 'flexDirection': 'row', 'width': '100%', 'height': '100vh'}, children=[
        # Control container (sliders)
        html.Div(id='control-container', style={'width': '25%', 'padding': '10px', 'flexDirection': 'column'}, children=[
            html.H1('Water in Soils', style={'textAlign': 'center'}, className='h1'),

            # Sliders for each layer
            html.Div(className='slider-container', children=[
                # Layer 1 Slider
                html.Label(children=[
                    'Z', html.Sub('1'), ' (m)'
                ], className='slider-label'),
                dcc.Slider(
                    id='z-1', min=0, max=20, step=0.25, value=2,
                    marks={i: f'{i}' for i in range(0, 21, 5)},
                    className='slider', tooltip={'placement': 'bottom', 'always_visible': True}
                ),

                # Layer 2 Slider
                html.Label(children=[
                    'Z', html.Sub('2'), ' (m)'
                ], className='slider-label'),
                dcc.Slider(
                    id='z-2', min=0, max=20, step=0.25, value=2,
                    marks={i: f'{i}' for i in range(0, 21, 5)},
                    className='slider', tooltip={'placement': 'bottom', 'always_visible': True}
                ),

                # Layer 3 Slider
                html.Label(children=[
                    'Z', html.Sub('3'), ' (m)'
                ], className='slider-label'),
                dcc.Slider(
                    id='z-3', min=0, max=20, step=0.25, value=2,
                    marks={i: f'{i}' for i in range(0, 21, 5)},
                    className='slider', tooltip={'placement': 'bottom', 'always_visible': True}
                ),

                # Layer 1 depth slider
                html.Label(children=[
                    'h', html.Sub('1'), ' (m)'
                ], className='slider-label'),
                dcc.Slider(
                    id='h-1', min=0, max=20, step=0.25, value=1,
                    marks={i: f'{i}' for i in range(0, 21, 5)},
                    className='slider', tooltip={'placement': 'bottom', 'always_visible': True}
                ),

                # Layer 3 depth slider
                html.Label(children=[
                    'h', html.Sub('3'), ' (m)'
                ], className='slider-label'),
                dcc.Slider(
                    id='h-3', min=0, max=25, step=0.25, value=6.5,
                    marks={i: f'{i}' for i in range(0, 31, 5)},
                    className='slider', tooltip={'placement': 'bottom', 'always_visible': True}
                ),
            ]),

            # Properties for each layer
            html.Div(className='layer-properties',  children=[
                # Layer 1 Properties
                html.H3('Layer 1', style={'textAlign': 'left'}),
                html.Label([f'γ (kN/m³)'], className='input-label'),
                dcc.Input(id='gama_1', type='number', value=18, step=0.01, style={'width': '12%'}, className='input-field'),
                html.Label([f'γ', html.Sub('r'), ' (kN/m³)'], className='input-label'),
                dcc.Input(id='gama_r_1', type='number', value=19, step=0.01, style={'width': '12%'}, className='input-field'),
                html.Label([f'γ′ (kN/m³)'], className='input-label'),
                dcc.Input(id='gama_prime_1', type='number', value=None, step=0.01, style={'width': '12%'}, className='input-field', readOnly=True),

                # Layer 2 Properties
                html.H3('Layer 2', style={'textAlign': 'left'}),
                html.Label([f'γ (kN/m³)'], className='input-label'),
                dcc.Input(id='gama_2', type='number', value=19, step=0.01, style={'width': '12%'}, className='input-field'),
                html.Label([f'γ', html.Sub('r'), ' (kN/m³)'], className='input-label'),
                dcc.Input(id='gama_r_2', type='number', value=21, step=0.01, style={'width': '12%'}, className='input-field'),
                html.Label([f'γ′ (kN/m³)'], className='input-label'),
                dcc.Input(id='gama_prime_2', type='number', value=None, step=0.01, style={'width': '12%'}, className='input-field', readOnly=True),

                # Layer 3 Properties
                html.H3('Layer 3', style={'textAlign': 'left'}),
                html.Label([f'γ (kN/m³)'], className='input-label'),
                dcc.Input(id='gama_3', type='number', value=18, step=0.01, style={'width': '12%'}, className='input-field'),
                html.Label([f'γ', html.Sub('r'), ' (kN/m³)'], className='input-label'),
                dcc.Input(id='gama_r_3', type='number', value=19, step=0.01, style={'width': '12%'}, className='input-field'),
                html.Label([f'γ′ (kN/m³)'], className='input-label'),
                dcc.Input(id='gama_prime_3', type='number', value=None, step=0.01, style={'width': '12%'}, className='input-field', readOnly=True),

                # equations
                html.H3(children=[f'γ′  = γ', html.Sub('r'),  ' - γ', html.Sub('w')], style={'textAlign': 'left'}),

            ]),
        ]),

        # Graphs container
        html.Div(className='graph-container', id='graphs-container', style={'display': 'flex', 'flexDirection': 'row', 'width': '70%'}, children=[
            html.Div(style={'width': '40%', 'height': '100%'}, children=[
                dcc.Graph(id='soil-layers-graph', style={'height': '100%', 'width': '100%'})
            ]),
            html.Div(style={'width': '60%', 'height': '100%'}, children=[
                dcc.Graph(id='pore-pressure-graph', style={'height': '100%', 'width': '100%'})
            ])
        ]),
        
        # Add the logo image to the top left corner
        html.Img(
            src='/assets/logo.png', className='logo',
            style={
                'position': 'absolute',
                'width': '250px',  # Adjust size as needed
                'height': 'auto',
                'z-index': '1000',  # Ensure it's on top of other elements
            }
        )
    ])
])

# Callback to update γ′ based on γ_r values for each layer
@app.callback(
    [Output(f'gama_prime_{i}', 'value') for i in range(1, 4)],
    [Input(f'gama_r_{i}', 'value') for i in range(1, 4)]
)
def update_gamma_prime(gama_r1, gama_r2, gama_r3):
    # Calculate γ′ as γ_r - 9.81 for each layer
    gama_prime1 = round(gama_r1 - 9.81, 2) if gama_r1 is not None else None
    gama_prime2 = round(gama_r2 - 9.81, 2) if gama_r2 is not None else None
    gama_prime3 = round(gama_r3 - 9.81, 2) if gama_r3 is not None else None
    
    return gama_prime1, gama_prime2, gama_prime3



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
        graph_style = {'display': 'flex', 'flexDirection': 'raw', 'alignItems': 'center', 'width': '100%'}
        control_style = {'width': '100%', 'padding': '10px'}
    else:
        # Display sliders on the left and graphs on the right for wider screens
        graph_style = {'display': 'flex', 'flexDirection': 'raw', 'width': '75%', 'gap': '0px'}
        control_style = {'width': '25%', 'padding': '10px'}
    
    return graph_style, control_style

@app.callback(
    Output('h-1', 'max'),
    Input('z-1', 'value'),
    Input('h-1', 'value')
)
def update_h1_max(z1_value, h1_value):
    if z1_value >= -h1_value:
        return z1_value
    else:
        return 20  

# Callback to handle the animations and input updates
@app.callback(
    Output('soil-layers-graph', 'figure'),
    Output('pore-pressure-graph', 'figure'),
    Input('z-1', 'value'),
    Input('z-2', 'value'),
    Input('z-3', 'value'),
    Input('h-1', 'value'),
    Input('h-3', 'value'),
    Input('gama_1', 'value'),
    Input('gama_r_1', 'value'),
    Input('gama_prime_1', 'value'),
    Input('gama_2', 'value'),
    Input('gama_r_2', 'value'),
    Input('gama_prime_2', 'value'),
    Input('gama_3', 'value'),
    Input('gama_r_3', 'value'),
    Input('gama_prime_3', 'value')
    
)
def update_graphs(z1, z2, z3, h1, h3, gama_1, gama_r_1, gama_prime_1, gama_2, gama_r_2, gama_prime_2, gama_3, gama_r_3, gama_prime_3):

    # Define soil layers and their boundaries with specified patterns
    layers = [
        {'layer_id': '1', 'name': 'Sand', 'top': 0, 'bottom': z1, 'color': 'rgb(244,164,96)','fillpattern': {'shape': '.'}, 'x0': -0.2, 'h':h1, 'text':'h\u2081'},  # Dots for Sand
        {'layer_id': '2', 'name': 'Clay', 'top': z1, 'bottom': z1 + z2, 'color': 'rgb(139,69,19)','fillpattern': {'shape': ''}, 'x0': 0},  # Dashes for Clay
        {'layer_id': '3', 'name': 'Sand', 'top': z1 + z2, 'bottom': z1 + z2 + z3, 'color': 'rgb(244,164,96)','fillpattern': {'shape': '.'}, 'x0': -0.70, 'h':h3, 'text':'h\u2083'},  # Dots for Sand
    ]

    # Create the soil layers figure (139,69,19)
    soil_layers_fig = go.Figure()

    for layer in layers:
        soil_layers_fig.add_trace(go.Scatter(
            x=[0.25, 0.25, 0.5, 0.5],  # Create a rectangle-like shape
            y=[layer['top'], layer['bottom'], layer['bottom'], layer['top']],
            fill='toself',
            fillcolor=layer['color'],  # Transparent background to see the pattern
            line=dict(width=1, color='black'),
            name=layer['name'],
            showlegend=False,
            fillpattern=layer['fillpattern']  # Use the specified fill pattern
        ))
        
        # Add a line at the top and bottom of each layer
        soil_layers_fig.add_trace(go.Scatter(
        x=[-1, 1],  # Start at -1 and end at 1
        y=[layer['top'], layer['top']],  # Horizontal line at the top of the layer
        mode='lines',
        line=dict(color='black', width=1, dash='dash'),
        showlegend=False  # Hide legend for these lines
        ))

        # Add the annotation for the layer name
        mid_depth = (layer['top'] + layer['bottom']) / 2  # Midpoint of the layer
        soil_layers_fig.add_annotation(
        x=0.6,  # Position the text slightly to the right of the layer box
        y=mid_depth,
        text=layer['name'],  # Layer name as text
        showarrow=False,  # Don't show an arrow
        font=dict(size=14, color="black"),
        xanchor='left',  # Anchor text to the left
        yanchor='middle'  # Center text vertically with the midpoint
        )

        # Add the filled rectangle shape
        if layer['name'] != 'Clay':
            soil_layers_fig.add_shape(
                    type="rect",
                    xref="x", yref="y",
                    x0=layer['x0'], y0=layer['bottom'],
                    x1=layer['x0'] + 0.1, y1=layer['bottom'] - layer['h'],
                    line=dict(
                        color="black",  # Change to 'rgba(0,0,0,0)' if you want no border at all
                        width=0,
                        dash='solid'  # Optional: specify dash type if desired
                    ),
                    fillcolor='lightskyblue',  # Fill color for the rectangle
                )
            
            if (layer['bottom'] - layer['h']) < 0:
                y_top = layer['bottom'] - layer['h'] -1
            else:
                y_top = -1
            # Add a line at left of Piezometer
            soil_layers_fig.add_trace(go.Scatter(
            x=[layer['x0']-0.005, layer['x0']-0.005],  
            y=[layer['bottom'], y_top],  
            mode='lines',
            line=dict(color='black', width=3, dash='solid'),
            showlegend=False  # Hide legend for these lines
            ))

            # Add a line at right of Piezometer
            soil_layers_fig.add_trace(go.Scatter(
            x=[layer['x0']+0.105, layer['x0']+0.105],  
            y=[layer['bottom'], y_top],  
            mode='lines',
            line=dict(color='black', width=3, dash='solid'),
            showlegend=False  # Hide legend for these lines
            ))

            # Add the annotation (text label) at the top of the rectangle
            soil_layers_fig.add_annotation(
                x=layer['x0'] - 0.1,  # Position the text in the middle of the rectangle's width
                y=layer['bottom'] - layer['h']+0.2,  # Place it at the top of the rectangle
                text=layer['text'],  # The text label to be displayed
                showarrow=False,  # Don't show the arrow
                font=dict(
                    size=16,  # Adjust the font size as needed
                    color="red"
                ),
                xanchor='center',  # Center the text horizontally
                yanchor='bottom'   # Anchor the text to the bottom
            )

    soil_layers_fig.update_layout(
        title=dict(
        text='Soil Layers',
        x=0.4,  # Center the title horizontally
        y=0.95,  # Position the title above the plot area
        xanchor='right',
        yanchor='top',
        font=dict(size=20)  # Adjust the font size as needed
        ),
        plot_bgcolor='white',
        xaxis_title='Width',
        xaxis=dict(
            range=[-1, 1], 
            showticklabels=False,
            showgrid=False,
            title=None, 
            zeroline=False),
        yaxis_title='Depth (m)',
        yaxis=dict(
            autorange='reversed', 
            # range=[0, z1+z2+z3],  # Reverse y-axis
            showticklabels=True,
            ticks='outside',
            ticklen=10,
            minor_ticks="inside",
            showline=True, 
            linewidth=2, 
            linecolor='black',
            zeroline=False),
    )

    # Calculate pore water pressure based on conditions
    step = 0.01
    depths = np.linspace(0, z1 + z2 + z3, num=int((z1 + z2 + z3)/step) + 1, endpoint=True)  # Define depths from 0 to total depth
    total_stress = np.zeros_like(depths)
    pore_pressure = np.zeros_like(depths)
    effective_stress = np.zeros_like(depths)

        # Constants
    gamma_water = 10 # kN/m³ for water


    # Calculate pore pressure based on the conditions
    for i, depth in enumerate(depths):
        if depth <= z1:
            if depth <= (z1 - h1):
                pore_pressure[i] = 0
                total_stress[i] = depth * gama_1
            else:
                pore_pressure[i] = (depth - (z1 - h1)) * gamma_water
                total_stress[i] = (z1 - h1)*gama_1 + (depth - z1 + h1) * gama_r_1
            effective_stress[i] = total_stress[i] - pore_pressure[i]
        elif depth <= z1 + z2:
            if (h1 + z2 + z3) == h3:
                pore_pressure[i] = (depth - (z1 - h1)) * gamma_water
                total_stress[i] = total_stress[int(z1/step)] + (depth - z1) * gama_r_2
            elif (h1 + z2 + z3) > h3:
                pore_pressure[i] = ((1 - abs(((z2 + z3 + h1) - h3)/z2)) * gamma_water * (depth - z1)) + pore_pressure[int(z1/step)]
                if h3 < (z2 + z3):
                    if depth <= (z1+z2+z3-h3):
                        total_stress[i] = total_stress[int(z1/step)] + (depth - z1) * gama_2
                    else:
                        total_stress[i] = total_stress[int(z1/step)] + (depth - (z1+z2+z3-h3)) * gama_r_2 + (z2+z3-h3) * gama_2
                else:
                    total_stress[i] = total_stress[int(z1/step)] + (depth - z1) * gama_r_2
            else:
                pore_pressure[i] = ((1 + abs(((z2 + z3 + h1) - h3)/z2)) * gamma_water * (depth - z1))  + pore_pressure[int(z1/step)]
                total_stress[i] = total_stress[int(z1/step)] + (depth - z1) * gama_r_2
            effective_stress[i] = total_stress[i] - pore_pressure[i]
            
        else:

            if (h1 + z2 + z3) == h3:
                pore_pressure[i] = (depth - (z1 - h1)) * gamma_water
                total_stress[i] = total_stress[int((z1 + z2)/step)]+ (depth - z1 - z2) * gama_r_3
            elif (h1 + z2 + z3) > h3:
                if h3 < z3:
                    if depth <= z1 + z2 + z3 - h3:
                        pore_pressure[i] = 0 + pore_pressure[int((z1 + z2)/step)]
                        total_stress[i] = total_stress[int((z1 + z2)/step)] + (depth - z1 - z2) * gama_3
                    else:
                        pore_pressure[i] = (depth - (z1 + z2 + z3 - h3)) * gamma_water +  pore_pressure[int((z1 + z2 + z3 - h3)/step)]
                        total_stress[i] = total_stress[int((z1 + z2 + z3 - h3)/step)] + (depth - (z1 + z2 + z3 - h3)) * gama_r_3
                else:
                    total_stress[i] = total_stress[int((z1 + z2)/step)]+ (depth - z1 - z2) * gama_r_3
                    pore_pressure[i] = (depth - z1 - z2) * gamma_water + pore_pressure[int((z1 + z2)/step)]
            else:
                pore_pressure[i] = (depth - z1 - z2) * gamma_water + pore_pressure[int((z1 + z2)/step)]
                total_stress[i] = total_stress[int((z1 + z2)/step)]+ (depth - z1 - z2) * gama_r_3
            effective_stress[i] = total_stress[i] - pore_pressure[i]


    # Create the pore pressure figure
    pressure_fig = go.Figure()
    pressure_fig.add_trace(go.Scatter(
        x=total_stress,
        y=depths,
        mode='lines',
        line=dict(color='red', width=3 ),
        name='Total Vertical Stress'
    ))

    pressure_fig.add_trace(go.Scatter(
        x=pore_pressure,
        y=depths,
        mode='lines',
        line=dict(color='blue', width=3 ),
        name='Pore Water Pressure'
    ))

    pressure_fig.add_trace(go.Scatter(
        x=effective_stress,
        y=depths,
        mode='lines',
        line=dict(color='green', width=3 ),
        name='Effective Vertical Stress'
    ))

    pressure_fig.update_layout(
    title=dict(
        text='Pore Water Pressure with Depth',
        x=0.5,  # Center the title horizontally
        y=0.98,  # Position the title above the plot area
        xanchor='center',
        yanchor='top',
        font=dict(size=20)  # Adjust the font size as needed
        ),
        xaxis_title='Pore Water Pressure (Pa)',
        plot_bgcolor='white',
        xaxis = dict(
            side = 'top',
            zeroline=False,
            showticklabels=True,
            ticks='outside',
            ticklen=10,
            minor_ticks="inside",
            showline=True, 
            linewidth=2, 
            linecolor='black',
            showgrid=True,
            gridwidth=1, 
            gridcolor='grey',
            mirror = True
            
            ),
        yaxis_title='Depth (m)',
        yaxis=dict(
            autorange='reversed',
            zeroline=False,
            showticklabels=True,
            ticks='outside',
            ticklen=10,
            minor_ticks="inside",
            showline=True, 
            linewidth=2, 
            linecolor='black',
            showgrid=True,
            gridwidth=1, 
            gridcolor='grey',
            mirror = True


            ), 
    )

    return soil_layers_fig, pressure_fig

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
    

# Expose the server
server = app.server
