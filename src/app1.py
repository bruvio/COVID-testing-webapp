import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_table
from dash import Dash
import dash_core_components as dcc
import plotly.graph_objs as go
import pandas as pd
import sqlite3

from src.server import server


# @server.route("/tableReport/")
# def MyDashApp():
#     return app.index()


app = Dash(
    __name__,
    server=server,
    external_stylesheets=[dbc.themes.SLATE],
    url_base_pathname="/tableReport/",
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

df_complete = df
df_incomplete = df

# Create your connection.
# cnx = sqlite3.connect('./src/data.db')

# df = pd.read_sql_query("SELECT * FROM cartridges", cnx)

dataframes = {"df_complete": df_complete, "df_incomplete": df_incomplete}


def get_data_object(user_selection):
    """
    For user selections, return the relevant in-memory data frame.
    """
    return dataframes[user_selection]


app.layout = html.Div(
    [
        html.H4("DataTable"),
        html.Label("Report type:", style={"font-weight": "bold"}),
        dcc.Dropdown(
            id="field-dropdown",
            options=[{"label": df, "value": df} for df in dataframes],
            value="df",
            clearable=False,
        ),
        dash_table.DataTable(id="table"),
    ]
)


@app.callback(
    [
        Output(component_id="table", component_property="data"),
        Output(component_id="table", component_property="columns"),
    ],
    [Input("field-dropdown", "value")],
)
def update_table(user_selection):
    """
    For user selections, return the relevant table
    """

    df = get_data_object(user_selection)
    columns = [{"name": col, "id": col} for col in df.columns]
    data = df.to_dict(orient="records")
    return data, columns
