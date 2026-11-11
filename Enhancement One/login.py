
from dash import html, dcc, Input, Output, State


def create_login_layout(app, message=""):

    #Get image from assets folder
    earth_url = app.get_asset_url("earth.gif")
    logo_url = app.get_asset_url("my-image.png")

    return html.Div(

        # Login page contents
        [
            # Grazioso Salvare image
            html.Div(
                html.Img(
                    src=logo_url,
                    style={
                        "width": "400px",
                        "maxWidth": "80%",
                        "height": "auto"
                    }
                ),
                style={
                    "position": "absolute",
                    "top": "35%",
                    "left": "50%",
                    "transform": "translate(-50%, -50%)",
                    "textAlign": "center",
                    "width": "100%"
                }
            ),

            # Login fields
            html.Div(
                [
                    html.Label("Username",
                               style={
                                   "color": "white",
                                   "fontWeight": "bold",
                               }
                    ),

                    dcc.Input(
                        id="login-username",
                        type="text",
                        placeholder="Enter Username",
                        style={
                            "width": "280px",
                            "padding": "10px",
                            "borderRadius": "5px",
                            "border": "1px solid #ccc",
                        }
                    ),

                    html.Br(),
                    html.Br(),

                    html.Label("Password",
                               style={
                                   "color": "white",
                                   "fontWeight": "bold"
                               }
                    ),
                    dcc.Input(
                        id="login-password",
                        type="password",
                        placeholder="Enter Password",
                        style={
                            "width": "280px",
                            "padding": "10px",
                            "borderRadius": "5px",
                            "border": "1px solid #ccc",
                            "marginBottom": "10px",
                        }
                    ),

                    html.Br(),
                    html.Br(),

                    html.Button("Login",
                                id="login-button",
                                n_clicks=0,
                                style={
                                    "width": "305px",
                                    "padding": "10px",
                                    "backgroundColor": "#286090",
                                    "color": "white",
                                    "fontWeight": "bold",
                                    "borderRadius": "5px",
                                    "border": "none",
                                    "cursor": "pointer",
                                }
                    ),

                    html.Div(
                        message,
                        id="login-message",
                        style={
                            "color": "red",
                            "marginTop": "10px",
                            "fontWeight": "bold",
                        }
                    )
                ],
                style={
                    "position": "absolute",
                    "bottom": "40px",
                    "left": "50%",
                    "transform": "translatex(-50%)",
                    "display": "flex",
                    "flexDirection": "column",
                    "alignItems": "center",
                    "width": "100%",
                }
            )

        ],

        style={
            "backgroundImage": f"url({earth_url})",
            "backgroundSize": "cover",
            "backgroundPosition": "center center",
            "backgroundRepeat": "no-repeat",
            "width": "100%",
            "height": "100vh",
            "position": "relative",
            "overflow": "hidden"
        }
    )

