import streamlit as st
from datetime import timedelta
import matplotlib.pyplot as plt
import pandas as pd
from main import MultiCalendar, work_url_hh, happy_url_hh, study_url_hh, work_url_myj, happy_url_myj, study_url_myj, \
    datetime_now, draw_bar
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
        row = mc.analyze(date, verbal=True)
        df = pd.concat([df, pd.DataFrame(row, index=[date.date().strftime('%Y-%m-%d')])])
    df.sort_index(ascending=True, inplace=True)
    return df


data = load_data(num_day, work_url_hh, happy_url_hh, study_url_hh)
st.dataframe(data, use_container_width=True)

# # 画图
# params = {'font.family': 'YouYuan',
#           'font.serif': 'Arial',
#           'font.weight': 'normal',  # or 'blod'
#           'ytick.major.size': 1.5,
#           'ytick.labelsize': 'large',
#           'ytick.major.pad': 2,
#           'figure.autolayout': True,
#           "axes.unicode_minus": False  # 该语句解决图像中的“-”负号的乱码问题
#           }
# rcParams.update(params)
#
# fig_0, ax = plt.subplots()
# for col in data.columns:
#     ax.plot(data['工作（重要必须）'], c='r', marker='*')
#     ax.plot(data['生活（健康快乐）'], c='g', marker='*')
#     ax.plot(data['学习（自我提升）'], c='b', marker='*')
#     ax.plot(data['碎片（发呆赖床）'], c='gray', marker='*')
# ax.set_xlabel("Date (day)")
# ax.set_xticks([i for i in range(num_day)])
# ax.set_xticklabels(data.index, rotation=45)
# ax.set_ylabel("Percentage (%)")
# st.pyplot(fig_0)

# 画图
st.pyplot(draw_bar(data))

st.divider()
st.header("Yujun's Calendar")

data = load_data(num_day,work_url_myj,happy_url_myj,study_url_myj)
st.dataframe(data, use_container_width=True)

# 画图

st.pyplot(draw_bar(data))
