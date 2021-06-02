from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from dash import Dash
import dash_core_components as dcc
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_html_components as html
import sqlite3
from db import db
from security_class import authenticate, identity
from resources.user import UserRegister
from resources.cartridge import Cartridge, CartridgeList


# Keep this out of source code repository - save in a file or a database
VALID_USERNAME_PASSWORD_PAIRS = {"bruno": "asdf"}

server = Flask(__name__)
server.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
server.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config['PROPAGATE_EXCEPTIONS'] = True
server.secret_key = "br1"
api = Api(server)


@server.before_first_request
def create_tables():
    from models.user import UserModel

    db.create_all()  # sql alchemy creates the tables that it sees and this works through imports
    admin = UserModel("bruno", "asdf")

    db.session.add(admin)
    db.session.commit()


jwt = JWT(server, authenticate, identity)  # allows authentication of users /auth

api.add_resource(Cartridge, "/cartridge/<string:cartridgeId>")

api.add_resource(CartridgeList, "/cartridges")
api.add_resource(UserRegister, "/register")


db.init_app(server)


@server.route("/")  # we are specifying the endopoint ##'http://www.google.com
def home():
    return "Hello, bruvio!"


# app = Dash(__name__,
#                server=server,
#                url_base_pathname='/')

# app.layout = html.Div(id='dash-container')


@server.route("/dashboard/")
def MyDashApp():
    return app.index()


app = Dash(
    __name__,
    server=server,
    external_stylesheets=[dbc.themes.SLATE],
    url_base_pathname="/",
)
# auth = dash_auth.BasicAuth(
#     app,
#     VALID_USERNAME_PASSWORD_PAIRS
# )
app.scripts.config.serve_locally = True
app.css.config.serve_locally = True
# auth = dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)

# app = dash.Dash()

colors = {
    "background": "#111111",
    # 'background': '#0000ff',
    "text": "rgb(255,0,0)",
    "plots": "rgb(255,128,0)",
}

name = "workouts_bruvio_2020.csv"

# df = read_df_from_s3(name, bucket)
df = pd.read_csv("workouts_bruvio_2020.csv")


# Create your connection.
# cnx = sqlite3.connect('./src/data.db')

# df = pd.read_sql_query("SELECT * FROM cartridges", cnx)


sport_options = []
for sport in df["WorkoutType"].unique():
    if sport == "Day Off":
        continue
    else:
        sport_options.append({"label": str(sport), "value": sport})

# sport_options.remove('Day Off')

columns = df.columns
remove_list = []
features = [x for x in columns if x not in remove_list]

bike_power_avg = df[df["WorkoutType"] == "Bike"]["PowerAverage"]
bike_TimeTotalInHours = df[df["WorkoutType"] == "Bike"]["TimeTotalInHours"]

run_power_avg = df[df["WorkoutType"] == "Run"]["PowerAverage"]
run_TimeTotalInHours = df[df["WorkoutType"] == "Run"]["TimeTotalInHours"]


app.layout = html.Div(
    children=[
        html.H1(
            children="My Training Dashboard.",
            style={"textAlign": "center", "color": colors["text"]},
        ),
        html.Div(
            children=[
                dcc.Graph(
                    id="scatter3",
                    figure={
                        "data": [
                            go.Scatter(
                                x=bike_TimeTotalInHours,
                                y=bike_power_avg,
                                mode="markers",
                                text=df["Title"],
                                marker={
                                    "size": 12,
                                    "color": "rgb(51,204,153)",
                                    "symbol": "pentagon",
                                    "line": {"width": 2},
                                },
                            )
                        ],
                        "layout": go.Layout(
                            plot_bgcolor=colors["background"],
                            paper_bgcolor=colors["background"],
                            font={"color": colors["plots"]},
                            title="Bike Data Scatterplot",
                            xaxis={"title": "TimeTotalInHours"},
                            yaxis={"title": "PowerAverage"},
                            hovermode="closest",
                        ),
                    },
                ),
                dcc.Graph(
                    id="scatter4",
                    figure={
                        "data": [
                            go.Scatter(
                                x=run_TimeTotalInHours,
                                y=run_power_avg,
                                mode="markers",
                                text=df["Title"],
                                marker={
                                    "size": 12,
                                    "color": "rgb(51,204,153)",
                                    "symbol": "pentagon",
                                    "line": {"width": 2},
                                },
                            )
                        ],
                        "layout": go.Layout(
                            plot_bgcolor=colors["background"],
                            paper_bgcolor=colors["background"],
                            font={"color": colors["plots"]},
                            title="Run Data Scatterplot",
                            xaxis={"title": "TimeTotalInHours"},
                            yaxis={"title": "PowerAverage"},
                            hovermode="closest",
                        ),
                    },
                ),
            ]
        ),
        html.Div(
            [
                dcc.Dropdown(
                    id="sport-picker", options=sport_options, value="Complete"
                ),
                dcc.Graph(id="graph"),
            ]
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Dropdown(
                            id="xaxis",
                            options=[
                                {"label": i.title(), "value": i} for i in features
                            ],
                            value="TimeTotalInHours",
                        )
                    ],
                    style={"width": "48%", "display": "inline-block"},
                ),
                html.Div(
                    [
                        dcc.Dropdown(
                            id="yaxis",
                            options=[
                                {"label": i.title(), "value": i} for i in features
                            ],
                            value="PowerAverage",
                        )
                    ],
                    style={"width": "48%", "float": "right", "display": "inline-block"},
                ),
                dcc.Graph(id="feature-graphic"),
            ],
            style={"padding": 10},
        ),
    ],
    style={"backgroundColor": colors["background"]},
)


@app.callback(Output("graph", "figure"), [Input("sport-picker", "value")])
def update_figure(selected_sport):
    filtered_df = df[df["WorkoutType"] == selected_sport]
    traces = []

    traces.append(
        go.Scatter(
            x=filtered_df["TimeTotalInHours"],
            y=filtered_df["TSS"],
            text=filtered_df["Title"],
            mode="markers",
            opacity=0.7,
            marker={"size": 15},
            # ,
            # name=filtered_df['Title']
            # name='ciao'
        )
    )

    return {
        "data": traces,
        "layout": go.Layout(
            plot_bgcolor=colors["background"],
            paper_bgcolor=colors["background"],
            font={"color": colors["plots"]},
            xaxis={"title": "TimeTotalInHours"},
            yaxis={"title": "TSS"},
            hovermode="closest",
        ),
    }


@app.callback(
    Output("feature-graphic", "figure"),
    [Input("xaxis", "value"), Input("yaxis", "value"), Input("sport-picker", "value")],
)
def update_graph(xaxis_name, yaxis_name, selected_sport):
    filtered_df = df[df["WorkoutType"] == selected_sport]
    return {
        "data": [
            go.Scatter(
                x=filtered_df[xaxis_name],
                y=filtered_df[yaxis_name],
                text=df["Title"],
                mode="markers",
                marker={
                    "size": 15,
                    "opacity": 0.5,
                    "line": {"width": 0.5, "color": "white"},
                },
            )
        ],
        "layout": go.Layout(
            plot_bgcolor=colors["background"],
            paper_bgcolor=colors["background"],
            font={"color": colors["plots"]},
            xaxis={"title": xaxis_name.title()},
            yaxis={"title": yaxis_name.title()},
            margin={"l": 40, "b": 40, "t": 10, "r": 0},
            hovermode="closest",
        ),
    }


if __name__ == "__main__":
    app.run_server(port=5000, debug=True)
