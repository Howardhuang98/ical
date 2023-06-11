import datetime
from datetime import datetime, timedelta, date
from zoneinfo import ZoneInfo
import requests as r
import icalendar
from matplotlib import pyplot as plt, rcParams
import streamlit as st
from streamlit_echarts import st_echarts

tz = ZoneInfo("Asia/Shanghai")
work_url_hh = r"http://p45-caldav.icloud.com.cn/published/2/MTAyMTY4NDI5NjQxMDIxNg7mk8kqxapws55OOPjqcgOXmRhGVc3dF9eOX0ffGpOg"
happy_url_hh = r"http://p220-caldav.icloud.com.cn/published/2/MTAyMTY4NDI5NjQxMDIxNg7mk8kqxapws55OOPjqcgM6V2h_Dd_m0eiqmceMwF9vDmA08jWqeFqmTKsJN_9MI4Pe1EUF89sc5vbKn5ogYb4"
study_url_hh = r"http://p220-caldav.icloud.com.cn/published/2/MTAyMTY4NDI5NjQxMDIxNg7mk8kqxapws55OOPjqcgNVwYPqz3tAV6cRsBBHIg8wkh6DpdABxQXPH1T_kkkPSdsRSBGWlbSSpN9d2QljP80"
work_url_myj = r"http://p220-caldav.icloud.com.cn/published/2/MTAyMTY4NDI5NjQxMDIxNg7mk8kqxapws55OOPjqcgPSWgzdQwLzSle08QRT3GetDkVD4bKHePXfWzd2a356jfCPtvaUMj8W7lP7FRx408A"
happy_url_myj = r"http://p221-caldav.icloud.com.cn/published/2/ODQxMTE2MTk0OTg0MTExNmmRQfdepP1yOTgzXuqBYGC9bbEniTWqhldVchEUH02T"
study_url_myj = r"http://p221-caldav.icloud.com.cn/published/2/ODQxMTE2MTk0OTg0MTExNmmRQfdepP1yOTgzXuqBYGAAZttDPyNyxr30A19yxhXmvM6yXTAcMEceC3izthUmCL9zU75dxWcrp5gpYeQgmQw"
datetime_now = datetime.now(tz=tz)


def hex_to_rgba(hex_code, alpha=1.0):
    """
    Convert a HEX color code to an RGBA tuple with the specified alpha value.
    """
    # Remove '#' if present
    hex_code = hex_code.lstrip('#')
    # Convert to RGBA
    rgb = tuple(int(hex_code[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return rgb + (alpha,)


class MultiCalendar:
    def __init__(self, url, *more_url):
        self.cals = []
        data = r.get(url)
        if data.status_code == 200:
            self.cals.append(icalendar.Calendar.from_ical(data.text))
        else:
            st.warning("妈的，有个日历没加载出来")
        if more_url:
            for l in more_url:
                data = r.get(l)
                if data.status_code == 200:
                    self.cals.append(icalendar.Calendar.from_ical(data.text))
                else:
                    st.warning("妈的，有个日历没加载出来")

    def analyze(self, dt, verbal=True):
        result = {}
        ts = []
        for c in self.cals:
            name = get_name(c)
            events = get_events(c, dt)
            t = sum([e[3] for e in events], timedelta())
            result.setdefault(name, t / timedelta(hours=15) * 100)
            ts.append(t / timedelta(hours=15) * 100)
            if verbal:
                print(f"{name}占据了{t / timedelta(hours=15) * 100:.2f}%")
        result["碎片（发呆赖床）"] = 100 - sum(ts)
        if verbal:
            print(f"碎片（发呆赖床）占据了{100 - sum(ts):.2f}%")
        return result


def get_events(cal, dt: datetime):
    events = []
    name = cal['X-WR-CALNAME'].to_ical().decode('utf-8')
    for event in cal.walk('VEVENT'):
        # 获取事件的开始和结束时间
        start_time = event.get('DTSTART').dt
        end_time = event.get('DTEND').dt
        # is all day event
        if not isinstance(start_time, datetime):
            continue
        else:
            if not start_time.tzinfo:
                start_time = start_time.replace(tzinfo=tz)
                end_time = end_time.replace(tzinfo=tz)
        # 输出事件信息
        if start_time.day == dt.day and start_time.month == dt.month and start_time.year == dt.year:
            events.append((event.get('SUMMARY'), start_time, end_time, end_time - start_time))
    return events


def get_name(cal):
    return cal['X-WR-CALNAME'].to_ical().decode('utf-8')


def draw_bar(df):
    options = {
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
        "legend": {
            "data": df.columns.values.tolist()
        },
        "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
        "xAxis": {"type": "value"},
        "yAxis": {
            "type": "category",
            "data": df.index.values.tolist(),
        },
        "series": [
            {
                "name": colname,
                "type": "bar",
                "stack": "total",
                "label": {"show": True},
                "emphasis": {"focus": "series"},
                "data": df.loc[:, colname].values.tolist(),
            } for colname in df.columns

        ],
        "color": ['#E53935', '#43A047', '#1E88E5', '#546E7A'],
    }
    st_echarts(options=options, height="500px")

def draw_pie(df):
    options = {
        "title": {"text": "日历活动比例分布", "subtext": "Howard", "left": "center"},
        "tooltip": {"trigger": "item"},
        "legend": {"orient": "vertical", "left": "left", },
        "series": [
            {
                "name": "活动类型",
                "type": "pie",
                "radius": "50%",
                "data": [
                    {"value": df.loc[:, colname].sum(), "name": colname} for colname in df.columns
                ],
                "emphasis": {
                    "itemStyle": {
                        "shadowBlur": 10,
                        "shadowOffsetX": 0,
                        "shadowColor": "rgba(0, 0, 0, 0.5)",
                    }
                },
                "color": ['#E53935', '#43A047', '#1E88E5', '#546E7A'],

            }
        ],
    }
    st_echarts(
        options=options, height="600px",
    )

if __name__ == '__main__':
    mc = MultiCalendar(work_url_hh, happy_url_hh, study_url_hh)
    for d in range(7):
        data = mc.analyze(datetime_now - timedelta(days=d), verbal=False)
        print(data)
    mc = MultiCalendar(work_url_myj, happy_url_myj, study_url_myj)
    for d in range(7):
        data = mc.analyze(datetime_now - timedelta(days=d), verbal=False)
        print(data)
