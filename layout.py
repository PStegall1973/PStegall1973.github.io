# This file contains the
# Dashboard layout and UI Components



from dash import dcc, html, dash_table, get_asset_url

# Shared Button Styling
button_style = {
    'margin': '5px',
    'background-color': '#CCCCCC',
    'color': 'white',
    'border': 'none',
    'padding': '10px 20px',
    'border-radius': '5px',
    'cursor': 'pointer',
    'transition': 'all 0.2s ease-in-out',
    'width': '180px'
}

# Main page layout configurations

def create_layout(df):

    # Load and encode the SNHU logo
    logo_url = get_asset_url("my-image.png") # Course supplied image
    background_url = get_asset_url("animal-rescue-background.png")# AI generated image

    return html.Div([

        # Hidden div
        html.Div(
            id="hidden-div",
            style={"display": "none"}
        ),

        # Logo
        html.Div([

            # Grazioso Salvare logo
            html.Div([
                html.A(
                    html.Img(
                        src=logo_url,
                        style={"width": "200px"}
                    ),
                    # Link to SNHU as per assignment
                    href="https://www.snhu.edu",
                    target="_blank"
                )
            ], style={"textAlign": "center",}),

            # Dashboard title
            html.Center(
                html.B(
                    html.H1("Global Rain/Grazioso Salvare Rescue Dashboard") # Rebranded with scenario clients name

                )
            ),

            # Rescue type filter buttons
            html.Div([

                html.Label("Filter by Rescue Type:",
                           style={"textAlign": "center",
                                  "display": "block",
                                  "width": "100%",
                                  "fontWeight": "bold"
                                  }
                           ),

                html.Div([

                    html.Button("Water", id="btn-water", n_clicks=0, style=button_style),
                    html.Button("Mountain/Wilderness", id="btn-mountain", n_clicks=0, style=button_style),
                    html.Button("Disaster", id="btn-disaster", n_clicks=0, style=button_style),
                    html.Button("All", id="btn-all", n_clicks=0, style=button_style),
                    html.Button("Reset", id="btn-reset", n_clicks=0, style=button_style)

                ], style={"margin": "10px 0",
                          "textAlign": "center",
                          }),

                # Store selected filter
                dcc.Store(id="selected-filter", data=""),

                # Store reset trigger
                dcc.Store(id="reset-trigger", data=False)

            ]),

            html.Hr(),

            # Animal shelter data table
            dash_table.DataTable(
                id="datatable-id",

                columns=[
                    {
                        "name": column,
                        "id": column,
                        "deletable": False,
                        "selectable": True
                    }
                    for column in df.columns
                ],

                data=df.to_dict("records"),

                editable=False,
                filter_action="native",
                sort_action="native",
                sort_mode="multi",

                row_selectable="single",
                row_deletable=False,
                selected_rows=[],

                page_action="native",
                page_current=0,
                page_size=5,

                style_table={"overflowX": "auto"},

                style_cell={
                    "textAlign": "left",
                    "minWidth": "100px",
                    "maxWidth": "180px",
                    "whiteSpace": "normal"
                }
            ),

            html.Br(),
            html.Hr(),

            # Graph Containers
            html.Div([

                html.Div(
                    id="graph-id",
                    style={"flex": "1", "padding": "10px"}
                ),

                # Map Containers
                html.Div(
                    id="map-id",
                    style={"flex": "1",
                           "padding": "10px",
                           "overflow": "hidden",
                           }
                )

            ], style={
                "display": "flex",
                "flexDirection": "row"
            })

        ]),

    # Background image
    ], style={
            "backgroundImage": f"url('{background_url}')",
            "backgroundSize": "cover",
            "backgroundPosition": "top center",
            "backgroundRepeat": "no-repeat",
            "backgroundAttachment": "fixed",
            "minHeight": "100vh",

    })
