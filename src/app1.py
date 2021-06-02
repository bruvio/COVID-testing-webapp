import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_table
from dash import Dash
import dash_core_components as dcc
import plotly.graph_objs as go
import pandas as pd
import sqlite3
import numpy as np
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
# df = pd.read_csv("workouts_bruvio_2020.csv")

cnx = sqlite3.connect("./src/data.db")

df = pd.read_sql_query("SELECT * FROM cartridges", cnx)


is_complete = df["testStatus"] == "Complete"
df_try = df[is_complete]
df_fake = df.append([df_try] * 5, ignore_index=True)


df_fake["submitedOn"] = pd.to_datetime(
    df_fake["submissionDateTime"], infer_datetime_format=True
)
df_fake["testStartedOn"] = pd.to_datetime(
    df_fake["testStartDateTime"], infer_datetime_format=True
)
df_fake["lastUpdatedon"] = pd.to_datetime(
    df_fake["lastUpdatedDateTime"], infer_datetime_format=True
)

df_fake.drop(
    ["submissionDateTime", "testStartDateTime", "lastUpdatedDateTime"],
    axis=1,
    inplace=True,
)

df_fake["testTime"] = (df_fake["lastUpdatedon"] - df_fake["submitedOn"]) / pd.Timedelta(
    minutes=1
)


df_testStatus = pd.pivot_table(
    df_fake, index="testStatus", values="cartridgeId", aggfunc=[len]
)

df_testStatus.reset_index(inplace=True)
df_testStatus.columns = ["testStatus", "count"]


p_table = pd.pivot_table(
    df_fake,
    index=["hospitalName", "pattern"],
    values=["testTime"],
    aggfunc={"testTime": [np.sum, np.mean]},
)

p_table.reset_index(inplace=True)

p_table.columns = ["hospitalName", "pattern", "testTime_mean", "testTime_sum"]


# Create your connection.


dataframes = {
    "allData": df_fake,
    "df_testStatus": df_testStatus,
    "df_testingTime": p_table,
}


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
            value="allData",
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
