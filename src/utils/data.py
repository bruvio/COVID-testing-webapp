import pandas as pd
import sqlite3
import numpy as np


def get_data():
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

    df_fake["testTime"] = (
        df_fake["lastUpdatedon"] - df_fake["submitedOn"]
    ) / pd.Timedelta(minutes=1)

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

    return df_fake, df_testStatus, p_table
