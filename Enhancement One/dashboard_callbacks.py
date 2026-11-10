#########################################
# Dashboard CallBacks for
# Filtering, Tables, Graphs, and Maps
########################################

import dash
import pandas as pd
import plotly.express as px
import dash_leaflet as dl
from dash import dcc, html
from dash.dependencies import Input, Output

from dashboard_logic import get_dashboard_records


def register_callbacks(app, shelter):

    #############################################
    # Set the Selected Rescue Filter
    #############################################

    @app.callback(
        Output('selected-filter', 'data'),
        Output('reset-trigger', 'data'),

        Input('btn-reset', 'n_clicks'),
        Input('btn-all', 'n_clicks'),
        Input('btn-water', 'n_clicks'),
        Input('btn-mountain', 'n_clicks'),
        Input('btn-disaster', 'n_clicks'),
        prevent_initial_call=True)

    def set_filter(
            _water_clicks,
            _mountain_clicks,
            _disaster_clicks,
            _all_clicks,
            _reset_clicks
    ):
        ctx = dash.callback_context

        if not ctx.triggered:
            raise dash.exceptions.PreventUpdate

        clicked_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if clicked_id == 'btn-reset':
            return '', True

        elif clicked_id == 'btn-all':
            return 'All', False

        elif clicked_id == 'btn-water':
            return 'Water', False

        elif clicked_id == 'btn-mountain':
            return 'Mountain', False

        elif clicked_id == 'btn-disaster':
            return 'Disaster', False

        raise dash.exceptions.PreventUpdate

    # Update Filter Button Styles
    @app.callback(
        Output('btn-reset', 'style'),
        Output('btn-all', 'style'),
        Output('btn-water', 'style'),
        Output('btn-mountain', 'style'),
        Output('btn-disaster', 'style'),
        Input('selected-filter', 'data')
    )
    def update_button_styles(selected):
        def style(active):
            return {
                'margin': '5px',
                'backgroundColor': '#007BFF' if active else '#e0e0e0',
                'color': 'white' if active else 'black',
                'border': '2px solid #999',
                'padding': '10px 20px',
                'borderRadius': '8px',
                'cursor': 'pointer',
                'boxShadow': 'inset 2px 2px 5px rgba(0, 0, 0, 0.3)' if active else '2px 2px 5px rgba(0, 0, 0, 0.3)',
                'fontWeight': 'bold',
                'transition': 'all 0.2s ease-in-out',
            }

        return (
            style(selected == 'reset'),
            style(selected == 'All'),
            style(selected == 'Water'),
            style(selected == 'Mountain'),
            style(selected == 'Disaster')
        )

    # Button activated filter queries
    @app.callback(
        Output("datatable-id", "data"),
        Input("selected-filter", "data")
    )
    def update_dashboard(rescue_type):

        df = get_dashboard_records(
            shelter,
            rescue_type
        )

        return df.to_dict("records")


    # Reset selected row when 'Reset' is clicked
    @app.callback(
        Output('datatable-id', 'selected_rows'),

        Input('btn-reset', 'n_clicks'),
        Input('btn-all', 'n_clicks'),
        Input('btn-water', 'n_clicks'),
        Input('btn-mountain', 'n_clicks'),
        Input('btn-disaster', 'n_clicks'),
        prevent_initial_call=True
    )
    def reset_selected_rows(_reset,
        _all,
        _water,
        _mountain,
        _disaster

    ):
        return []

    # Update the Breed Distribution Graph

    # noinspection pep8-naming
    @app.callback(
        Output('graph-id', "children"),
        [Input('datatable-id', "derived_virtual_data")]
    )
    def update_graphs(viewData):
        if viewData is None or len(viewData) == 0:
            return html.Div("No data to display")

        dff = pd.DataFrame.from_dict(viewData)

        if 'breed' in dff.columns:
            breed_counts = dff['breed'].value_counts().reset_index()
            breed_counts.columns = ['breed', 'count']

            # Use breed_counts instead of dff
            fig = px.pie(
                breed_counts,
                names='breed',
                values='count',
                title='Breed Distribution',
                labels={'breed': 'Breed', 'count': 'Count'}
            )

            fig.update_traces(textposition='inside', textinfo='percent+label')

            return [dcc.Graph(figure=fig)]
        else:
            return html.Div("Breed column missing in data")

    # This callback will highlight a cell on the data table when the user selects it
    @app.callback(
        Output('datatable-id', 'style_data_conditional'),
        [Input('datatable-id', 'selected_columns')]
    )
    def update_styles(selected_columns):
        # Check if any column is selected
        if not selected_columns:
            return []  # No columns selected, no styling applied

        # Apply background color to selected columns
        return [
            {
            'if': {'column_id': i},
            'background_color': '#D2F3FF'
        }
        for i in selected_columns
        ]

    # This callback will update the geolocation chart for the selected data entry
    # derived_virtual_data will be the set of data available from the datatable in the form of
    # a dictionary.
    # derived_virtual_selected_rows will be the selected row(s) in the table in the form of
    # a list. For this application, we are only permitting single row selection so there is only
    # one value in the list.
    # The iloc method allows for a row, column notation to pull data from the datatable
    # noinspection pep8-naming
    @app.callback(
        Output('map-id', "children"),

        [Input('datatable-id', "derived_virtual_data"),
         Input('datatable-id', "derived_virtual_selected_rows"),
         Input('selected-filter', 'data')
         ]
    )

    def update_map(viewData, index, selected_filter):

        # If reset is pressed, clear the map
        if selected_filter == 'Reset':
            return [
                html.P("Map cleared. Select a row to display location.")
            ]

        # 1. Defensive check: No data
        if not viewData or not index:
            return [
                html.P("No data to display on the map.",
                       style={"color": "red",
                              "fontWeight": "bold"
                              }
                       )
            ]

        # 2. Convert input to DataFrame
        dff = pd.DataFrame(viewData)

        # 3. Check for required columns
        required_columns = [
            'location_lat',
            'location_long',
            'breed',
            'name'
        ]

        missing_columns = [
            col for col in required_columns if col not in dff.columns
        ]
        if missing_columns:
            return [
                html.P(f"Missing required column(s): {', '.join(missing_columns)}")
            ]

        # 4. Handle selected row (or default to 0)
        if not index or len(index) == 0:
            row = 0
        else:
            row = index[0]

        # 5. Avoid row index error
        if row >= len(dff):
            return [
                html.P("Selected row is out of range.")
            ]

        # 6. Extract location + info
        lat = dff.iloc[row]['location_lat']
        lon = dff.iloc[row]['location_long']
        breed = dff.iloc[row]['breed']
        name = dff.iloc[row].get('name', '')
        if not name:
            name = "No name available"

        return [
            dl.Map(style={'width': '1000px', 'height': '500px'},
                   center=[lat, lon], zoom=10, children=[
                    dl.TileLayer(id="base-layer-id"),
                    dl.Marker(position=[lat, lon], children=[
                        dl.Tooltip(breed),
                        dl.Popup([
                            html.H1("Animal Name"),
                            html.P(name)
                        ])
                    ])
                ])
        ]
