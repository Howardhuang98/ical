import streamlit as st
from datetime import timedelta
import matplotlib.pyplot as plt
import pandas as pd
from main import MultiCalendar, work_url, happy_url, study_url, datetime_now
from matplotlib import rcParams

st.title("Howard's Calendar")


@st.cache_data
def load_data(days):
    # data = pd.read_csv(DATA_URL, nrows=nrows)
    # lowercase = lambda x: str(x).lower()
    # data.rename(lowercase, axis='columns', inplace=True)
    # data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    # return data
    mc = MultiCalendar(work_url, happy_url, study_url)
    df = pd.DataFrame()
    for d in range(days):
        date = datetime_now - timedelta(days=d)
        row = mc.analyze(date, verbal=False)
        df = pd.concat([df, pd.DataFrame(row, index=[date.date().strftime('%Y-%m-%d')])])
    df.sort_index(ascending=True, inplace=True)
    return df


num_day = st.slider("Number of Days", 0, 30, 7)

st.text(f"Now:{datetime_now.strftime('%Y-%m-%d')}")
data = load_data(num_day)
data

# 画图
params = {'font.family': 'YouYuan',
          'font.serif': 'Arial',
          'font.weight': 'normal',  # or 'blod'
          'ytick.major.size': 1.5,
          'ytick.labelsize': 'large',
          'ytick.major.pad': 2,
          'figure.autolayout': True,
          "axes.unicode_minus": False  # 该语句解决图像中的“-”负号的乱码问题
          }
rcParams.update(params)

fig_0, ax = plt.subplots()
for col in data.columns:
    ax.plot(data['工作（重要必须）'], c='r', marker='*')
    ax.plot(data['生活（健康快乐）'], c='g', marker='*')
    ax.plot(data['学习（自我提升）'], c='b', marker='*')
    ax.plot(data['碎片（发呆赖床）'], c='gray', marker='*')
ax.set_xlabel("Date (day)")
ax.set_xticks([i for i in range(num_day)])
ax.set_xticklabels(data.index, rotation=45)
ax.set_ylabel("Percentage (%)")
st.pyplot(fig_0)

# 画图
fig_1, ax = plt.subplots(figsize=(9.2, 5), dpi=600)
ax.invert_yaxis()
ax.xaxis.set_visible(False)
ax.set_xlim(0, 100)
data_cum = data.cumsum(axis='columns')
for i, (colname, color) in enumerate(zip(data.columns, ['r', 'g', 'b', 'gray'])):
    widths = data.iloc[:, i]
    starts = data_cum.iloc[:, i] - widths
    rects = ax.barh(data.index, widths, left=starts, height=0.5, label=colname, color=color)
ax.legend(ncols=4, bbox_to_anchor=(0, 1), loc='lower left', fontsize='small')
st.pyplot(fig_1)
