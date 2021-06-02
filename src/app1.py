import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_table
from dash import Dash
import dash_core_components as dcc
import plotly.graph_objs as go

from src.server import server
from src.utils.data import get_data

# @server.route("/tableReport/")
# def MyDashApp():
#     return app.index()


app = Dash(
    __name__,
    server=server,
    external_stylesheets=[dbc.themes.SLATE],
    url_base_pathname="/tableReport/",
)

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True


colors = {
    "background": "#111111",
    # 'background': '#0000ff',
    "text": "rgb(255,0,0)",
    "plots": "rgb(255,128,0)",
}

df_fake, df_testStatus, p_table = get_data()


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
