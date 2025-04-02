# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Declare input and output objects
dku_input = dataiku.Dataset("new_FD001_cycles_movingavg")
dku_output = dataiku.Dataset("new_FD001_features")

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
df_input = dku_input.get_dataframe()
df_output = df_input

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
def calc_ratio(a,b):
    if a == 0:
        return np.nan
    else:
        return (b - a)/a

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
for i in range(1,4):
    current_setting = "setting_" + str(i)
    current_max_setting = "pct_to_max_" + current_setting
    current_min_setting = "pct_to_min_" + current_setting
    current_full_max = "w_full_history_" + current_setting + "_max"
    current_full_min = "w_full_history_" + current_setting + "_min"

    df_output[current_max_setting] = df_output.apply(lambda row: calc_ratio(row[current_setting], row[current_full_max]), axis=1)
    df_output[current_min_setting] = df_output.apply(lambda row: calc_ratio(row[current_full_min], row[current_setting]), axis=1)

    del df_output[current_full_max]
    del df_output[current_full_min]
    del df_output["w_full_history_" + current_setting + "_avg"]
    del df_output["w10_cycles_" + current_setting + "_min"]
    del df_output["w10_cycles_" + current_setting + "_max"]

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
for i in range(1,22):
    current_sensor = "sensor_" + str(i)
    current_max_sensor = "pct_to_max_" + current_sensor
    current_min_sensor = "pct_to_min_" + current_sensor
    current_full_sensor_max = "w_full_history_" + current_sensor + "_max"
    current_full_sensor_min = "w_full_history_" + current_sensor + "_min"

    df_output[current_max_sensor] = df_output.apply(lambda row: calc_ratio(row[current_sensor], row[current_full_sensor_max]), axis=1)
    df_output[current_min_sensor] = df_output.apply(lambda row: calc_ratio(row[current_full_sensor_min], row[current_sensor]), axis=1)

    del df_output[current_full_sensor_max]
    del df_output[current_full_sensor_min]
    del df_output["w_full_history_" + current_sensor + "_avg"]
    del df_output["w10_cycles_" + current_sensor + "_min"]
    del df_output["w10_cycles_" + current_sensor + "_max"]

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
dku_output.write_with_schema(df_output)