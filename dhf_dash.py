import dash
import dash_bootstrap_components as dbc  # 0.10.5
import pandas as pd
import plotly.graph_objects as go

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Start dash app and get external bootstrap stylesheet
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

# Import Mapbox Access Token
mapbox_access_token = 'pk.eyJ1IjoidG9iaXNpbTQ0IiwiYSI6ImNrZDlkMnJ0cDAzMXkycm16bnkxbG5nbnAifQ.FWzb3dUhfEMJetVGNww31Q'

# Importing data into pandas
df = pd.read_csv('https://raw.githubusercontent.com/TobiSim44/Bachelorarbeit/master/dhf-homes-3.csv')

# Add column with data of each home
df['text'] = 'Type: ' + df['type'] + \
             '<br>Street: ' + df['street'].astype(str) + \
             '<br>Neighborhood: ' + df['neighborhood'] + \
             '<br>Cost: ' + df['cost'].astype(str) + ' $' \
                                                     '<br>Bedrooms: ' + df['bedrooms'].astype(str) + \
             '<br>Fireplace: ' + df['fireplace'] + \
             '<br>Garage: ' + df['garage'] + \
             '<br>Air Conditioner : ' + df['ac'] + \
             '<br>new : ' + df['new']

df.head()
index = df.index
number_homes = len(index)
available_neighborhood = df['neighborhood'].unique()

# Layout of the app
app.layout = \
    html.Div([

        dbc.Row(dbc.Col(html.H1("Dynamic HomeFinder"), width={'size': 6, 'offset': 5}), ),

        # Radio items to display all homes in df or only the selected ones
        html.P("Filter dataset:"),
        dbc.Row(dbc.Col(dcc.RadioItems(id='all_homes',
                                       options=[
                                           {'label': 'All', 'value': 'all'},
                                           {'label': 'Selected', 'value': 'selected'},
                                       ],
                                       value='selected'),
                        width={'size': 4, 'offset': 0}
                        ),
                ),

        dbc.Row([
            dbc.Col([
                # Checklist roomnumber
                html.P("Filter by rooms:"),
                dcc.Checklist(id='room_number',
                              options=[
                                  {'label': str(i), 'value': i} for i in sorted(df['bedrooms'].unique())
                              ],
                              value=[i for i in sorted(df['bedrooms'].unique())],
                              style={'width': '40%'},
                              ),
            ]),

            dbc.Col([
                # Checklist fireplace
                html.P("Filter by fireplace:"),
                dcc.Checklist(id='select_fireplace',
                              options=[
                                  {'label': str(i), 'value': i} for i in sorted(df['fireplace'].unique())
                              ],
                              value=[i for i in sorted(df['fireplace'].unique())],
                              style={'width': '40%'},
                              ),
            ]),

            dbc.Col([
                # Checklist attributes
                html.P("Filter by garage:"),
                dcc.Checklist(id='select_garage',
                              options=[
                                  {'label': str(i), 'value': i} for i in sorted(df['garage'].unique())
                              ],
                              value=[i for i in sorted(df['garage'].unique())],
                              style={'width': '40%'},
                              ),
            ]),
            dbc.Col([
                # Checklist Air Conditioner
                html.P("Filter by air conditioner:"),
                dcc.Checklist(id='select_air',
                              options=[
                                  {'label': str(i), 'value': i} for i in sorted(df['ac'].unique())
                              ],
                              value=[i for i in sorted(df['ac'].unique())],
                              style={'width': '40%'},
                              ),
            ]),
            dbc.Col([
                # Checklist New
                html.P("Filter by new:"),
                dcc.Checklist(id='select_new',
                              options=[
                                  {'label': str(i), 'value': i} for i in sorted(df['new'].unique())
                              ],
                              value=[i for i in sorted(df['new'].unique())],
                              style={'width': '40%'},
                              ),
            ]),
        ]),
        html.Br(),

        dbc.Row([
            dbc.Col([
                # Dropdown menu for type of house
                html.P("Filter by well status:"),
                dcc.Dropdown(id='select_type',
                             options=[
                                 {'label': str(i), 'value': i} for i in sorted(df['type'].unique())
                             ],
                             multi=True,
                             value=[i for i in sorted(df['type'].unique())],
                             style={'width': '65%'},
                             ),

                # Prints out selected type
                html.Div(id='output_type', children=[]),
                html.Br(),

                # Dropdown menu for all neighborhoods
                html.P("Filter by neighborhood:"),
                dcc.Dropdown(id='select_neighborhood',
                             options=[
                                 {'label': str(i), 'value': i} for i in sorted(df['neighborhood'].unique())
                             ],
                             multi=True,
                             value=[i for i in sorted(df['neighborhood'].unique())],
                             style={'width': '90%'},
                             ),
            ]),

            # show graph
            dcc.Graph(id='my_dynamichomefinder', figure={},
                      style={'height': '700px', 'width': '55%'}),
        ]),

        # Range slider for cost
        dbc.Row([
            dbc.Col([
                html.P("Filter by price:"),
                dcc.RangeSlider(id='price_range',
                                min=df['cost'].min(),
                                max=df['cost'].max(),
                                step=1,
                                marks={str(i): str(i) for i in df['cost'].unique()},
                                value=[df['cost'].min(), df['cost'].max()],
                                ),
                # Prints out selected lowest and highest price
                html.Div(id='output_price', children=[]),
            ]),
        ]),
    ])


# Connection between graphs and components
@app.callback(
    [Output(component_id='output_type', component_property='children'),
     Output(component_id='output_price', component_property='children'),
     Output(component_id='my_dynamichomefinder', component_property='figure')],
    [Input(component_id='all_homes', component_property='value'),
     Input(component_id='select_type', component_property='value'),
     Input(component_id='select_fireplace', component_property='value'),
     Input(component_id='select_garage', component_property='value'),
     Input(component_id='select_neighborhood', component_property='value'),
     Input(component_id='room_number', component_property='value'),
     Input(component_id='select_air', component_property='value'),
     Input(component_id='select_new', component_property='value'),
     Input(component_id='price_range', component_property='value')
     ]
)
# Updating graph with input data
# Data is handed over to function in input order
def update_graph(all_homes, select_type, select_fireplace, select_garage, select_neighborhood, room_number,
                 select_air, select_new, price_range):
    print(all_homes, number_homes, select_type, select_fireplace, select_garage, select_neighborhood, room_number,
          select_air, select_new, price_range),

    # Saves selected type. Returns with container to output_container
    container_type = "The type of the estate is: {}".format(select_type)
    container_price = "Price is higher than {}".format(price_range[0]) + "$ and lower than {}".format(
        price_range[1]) + '$'

    # Copy and filter dataframe
    dff = df.copy()
    if all_homes == 'all':
        dff
    else:
        dff = dff[df['type'].isin(select_type) &
                  df['neighborhood'].isin(select_neighborhood) &
                  df['garage'].isin(select_garage) &
                  df['bedrooms'].isin(room_number) &
                  df['fireplace'].isin(select_fireplace) &
                  df['ac'].isin(select_air) &
                  df['new'].isin(select_new)]
        dff = dff[df['cost'] >= price_range[0]]
        dff = dff[df['cost'] <= price_range[1]]

    # Create map with marker
    fig = go.Figure(go.Scattermapbox(
        lat=dff['latitude'],
        lon=dff['longitude'],
        text=dff['text'],
        hoverinfo='text',
        mode='markers',
        unselected={'marker': {'opacity': 0.4, 'size': 9.0}},
        selected={'marker': {'opacity': 1.0, 'size': 16.0}},
        marker=go.scattermapbox.Marker(
            size=9.0,
            opacity=0.6,
            color=dff['cost'],
            colorbar=dict(
                x=1.0,
                title="Price",
            )
        ),
        showlegend=False,
    ))

    # Update map and position
    fig.update_layout(
        autosize=True,
        uirevision='true',  # preserves map after callback activated # Value doesn't matter
        clickmode='event+select',  # enable select markers
        hovermode='closest',
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            style='light',  # 'open-street-map' if no key available
            center=dict(
                lat=38.92,
                lon=-77.07
            ),
            pitch=0,
            zoom=10
        ),
    )

    # Return to callback in output order
    return container_type, container_price, fig


# start app
if __name__ == '__main__':
    app.run_server(debug=True)
