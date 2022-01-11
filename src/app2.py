import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_html_components as html
import logging
from dash import Dash
import dash_core_components as dcc
import plotly.graph_objs as go
from src.utils.data import get_data
from src.server import server


logger = logging.getLogger()
logger.setLevel(logging.INFO)




app = Dash(
    __name__,
    server=server,
    external_stylesheets=[dbc.themes.SLATE],
    url_base_pathname="/dashboard/",
)

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

colors = {
    "background": "#111111",
    # 'background': '#0000ff',
    "text": "rgb(255,0,0)",
    "plots": "rgb(255,128,0)",
}


def serve_layout():
    try:
        df_fake, df_testStatus, p_table = get_data()

        test_outcomes = [
            {"label": str(outcome), "value": outcome}
            for outcome in df_fake["testStatus"].unique()
        ]

        columns = df_fake.columns
        remove_list = [
            "submitedOn",
            "testStartedOn",
            "lastUpdatedon",
        ]
        features = [x for x in columns if x not in remove_list]

        return html.Div(
            children=[
                html.H1(
                    children="Covid Testing Dashboard.",
                    style={"textAlign": "center", "color": colors["text"]},
                ),
                html.Div(
                    children=[
                        dcc.Graph(
                            id="scatter3",
                            figure={
                                "data": [
                                    go.Scatter(
                                        x=df_testStatus["testStatus"],
                                        y=df_testStatus["count"],
                                        mode="markers",
                                        # text=df['Title'],
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
                                    # title='Bike Data Scatterplot',
                                    xaxis={"title": "Test outcome"},
                                    yaxis={"title": "count"},
                                    hovermode="closest",
                                ),
                            },
                        ),
                        dcc.Graph(
                            id="scatter4",
                            figure={
                                "data": [
                                    go.Scatter(
                                        x=p_table["pattern"],
                                        y=p_table["testTime_mean"],
                                        mode="markers",
                                        # text=df['Title'],
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
                                    # title='Run Data Scatterplot',
                                    xaxis={"title": "pattern"},
                                    yaxis={"title": "testTime_mean"},
                                    hovermode="closest",
                                ),
                            },
                        ),
                    ]
                ),
                html.Div(
                    [
                        dcc.Dropdown(
                            id="test-picker", options=test_outcomes, value="Complete"
                        ),
                        dcc.Graph(id="graph"),
                    ]
                ),
            ],
            style={"backgroundColor": colors["background"]},
        )
    except:
        logger.warning("\n error reading database or empty database")
        return html.Div("Dash app 2")


@app.callback(Output("graph", "figure"), [Input("test-picker", "value")])
def update_figure(selected):
    df_fake, dum, dum = get_data()
    # filtered_df = df_fake[df_fake['pattern'] == selected]
    filtered_df = df_fake[df_fake["testStatus"] == selected]
    # print(filtered_df)
    traces = [
        go.Scatter(
            x=filtered_df["hospitalName"],
            y=filtered_df["testTime"],
            mode="markers",
            opacity=0.7,
            marker={"size": 15},
        )
    ]

    return {
        "data": traces,
        "layout": go.Layout(
            plot_bgcolor=colors["background"],
            paper_bgcolor=colors["background"],
            font={"color": colors["plots"]},
            xaxis={"title": "hospitalName"},
            yaxis={"title": "testTime"},
            hovermode="closest",
        ),
    }


app.layout = serve_layout
