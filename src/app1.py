import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_table
from dash import Dash
import dash_core_components as dcc
import plotly.graph_objs as go
import logging
from src.server import server
from src.utils.data import get_data

logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Dash(
    __name__,
    server=server,
    external_stylesheets=[dbc.themes.SLATE],
    url_base_pathname="/tableReport/",
)

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

global dataframes
global df_fake
global df_testStatus
global p_table

try:
    df_fake, df_testStatus, p_table = get_data()

    dataframes = {
        "allData": df_fake,
        "df_testStatus": df_testStatus,
        "df_testingTime": p_table,
    }
except:
    logger.warning("\n error reading database or empty database")


# def get_data_object(user_selection):
#     """
#     For user selections, return the relevant in-memory data frame.
#     """
#     return dataframes[user_selection]


def change_layout():
    try:
        df_fake, df_testStatus, p_table = get_data()

        dataframes = {
            "allData": df_fake,
            "df_testStatus": df_testStatus,
            "df_testingTime": p_table,
        }
        return html.Div(
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
    except:
        logger.warning("\n error reading database or empty database")
        return html.Div("Dash app 1")


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
    df_fake, df_testStatus, p_table = get_data()

    dataframes = {
        "allData": df_fake,
        "df_testStatus": df_testStatus,
        "df_testingTime": p_table,
    }

    df = dataframes[user_selection]
    columns = [{"name": col, "id": col} for col in df.columns]
    data = df.to_dict(orient="records")
    return data, columns


app.layout = change_layout
