import datetime
from datetime import datetime, timedelta, date
from zoneinfo import ZoneInfo
import requests as r
import icalendar

tz = ZoneInfo("Asia/Shanghai")
work_url = r"http://p45-caldav.icloud.com.cn/published/2/MTAyMTY4NDI5NjQxMDIxNg7mk8kqxapws55OOPjqcgOXmRhGVc3dF9eOX0ffGpOg"
happy_url = r"http://p220-caldav.icloud.com.cn/published/2/MTAyMTY4NDI5NjQxMDIxNg7mk8kqxapws55OOPjqcgM6V2h_Dd_m0eiqmceMwF9vDmA08jWqeFqmTKsJN_9MI4Pe1EUF89sc5vbKn5ogYb4"
study_url = r"http://p220-caldav.icloud.com.cn/published/2/MTAyMTY4NDI5NjQxMDIxNg7mk8kqxapws55OOPjqcgNVwYPqz3tAV6cRsBBHIg8wkh6DpdABxQXPH1T_kkkPSdsRSBGWlbSSpN9d2QljP80"
datetime_now = datetime.now(tz=tz)


class MultiCalendar:

    def __init__(self, url, *more_url):
        self.cals = []
        data = r.get(url)
        self.cals.append(icalendar.Calendar.from_ical(data.text))
        if more_url:
            for l in more_url:
                data = r.get(l)
                self.cals.append(icalendar.Calendar.from_ical(data.text))

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


if __name__ == '__main__':
    mc = MultiCalendar(work_url, happy_url, study_url)
    for d in range(7):
        data = mc.analyze(datetime_now-timedelta(days=d), verbal=False)
        print(data)
