import streamlit as st
from datetime import timedelta
import matplotlib.pyplot as plt
import pandas as pd
from streamlit_echarts import st_echarts

from main import MultiCalendar, work_url_hh, happy_url_hh, study_url_hh, work_url_myj, happy_url_myj, study_url_myj, \
    datetime_now, draw_bar, draw_pie
from matplotlib import rcParams

st.title(f"Now:{datetime_now.strftime('%Y-%m-%d')}")
st.markdown("This application is recording life of Hao Huang and Yujun Ma. Tomorrow is every second in today~")
num_day = st.slider("Number of Days", 0, 30, 7)
st.divider()

st.header("Howard's Calendar")


def load_data(days, url, *more_url):
    # data = pd.read_csv(DATA_URL, nrows=nrows)
    # lowercase = lambda x: str(x).lower()
    # data.rename(lowercase, axis='columns', inplace=True)
    # data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    # return data
    mc = MultiCalendar(url, *more_url)
    df = pd.DataFrame()
    for d in range(days):
        date = datetime_now - timedelta(days=d)
        row = mc.analyze(date, verbal=False)
        df = pd.concat([df, pd.DataFrame(row, index=[date.date().strftime('%Y-%m-%d')])])
    df.sort_index(ascending=True, inplace=True)
    return df.round(2)


data = load_data(num_day, work_url_hh, happy_url_hh, study_url_hh)
st.dataframe(data, use_container_width=True)

draw_pie(data)
draw_bar(data)


st.divider()
st.header("Yujun's Calendar")

data = load_data(num_day,work_url_myj,happy_url_myj,study_url_myj)
st.dataframe(data, use_container_width=True)

# 画图

draw_pie(data)
draw_bar(data)
