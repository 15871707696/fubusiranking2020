# 爬虫代码
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
    'Host': 'www.forbeschina.com'
}
url = 'https://www.forbeschina.com/lists/1733'
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
items = soup.find_all('tr')
result = []
for item in items[:-1]:
    result.append([i.text for i in item.find_all('td')])
with open('2020年福布斯排行榜.csv', 'a+', newline='')as f:
    f_csv = csv.writer(f)
    f_csv.writerows(result)
# 一、福布斯排行榜各国家人数占比
# 1.数据处理
data = pd.read_csv('2020年福布斯排行榜.csv', encoding='gbk')
list_country = list(set(list(data['国家和地区'])))  # 去重
dict_country = {}
list_country_count = [list(data['国家和地区']).count(i) for i in list_country]
for i, j in zip(list_country, list_country_count):
    dict_country[i] = j
tuple_country = sorted(dict_country.items(), key=lambda x: x[1], reverse=True)
# 2.数据分析
from pyecharts import options as opts
from pyecharts.charts import Pie
pie = (
    Pie()
        .add(
        "",
        tuple_country[:20],
        radius=["30%", "75%"],
        rosetype="radius",
        label_opts=opts.LabelOpts(is_show=False),
    )
        .set_global_opts(
        title_opts=opts.TitleOpts(title="全球各国福布斯排行人数统计"),
        legend_opts=opts.LegendOpts(type_="scroll", pos_left="90%", orient="vertical"),
    )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}，{d}%"))
)
pie.render('./sumpeople.html')
# 二、分析各国亿万富豪平均身价
# 1.数据处理
import pandas as pd
import numpy as np
data = pd.read_csv('2020年福布斯排行榜.csv', encoding='gbk')
# 各国占比
list_country = list(set(list(data['国家和地区'])))  # 去重
dict_country = {}
list_country_count = [list(data['国家和地区']).count(i) for i in list_country]
for i, j in zip(list_country, list_country_count):
    dict_country[i] = j
tuple_country = sorted(dict_country.items(), key=lambda x: x[1], reverse=True)
dict_money = {}
for i, j in tuple_country:
    arr = list(data[data['国家和地区'].eq(i)]['财富（亿美元）'].str.replace(',', '').astype(float))
    arr = list(map(int, arr))
    eve_money = np.sum(np.array(arr)) / j
    # eve_money = sum(float(n) for n in list(data[data['国家和地区'].eq(i)]['财富（亿美元）'])) / j
    dict_money[i] = eve_money
tuple_money = sorted(dict_money.items(), key=lambda x: x[1], reverse=True)
# 2.数据分析
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.globals import ThemeType

l1 = [i[0] for i in tuple_money]
l2 = [i[1] for i in tuple_money]
bar = (
    Bar({"theme": ThemeType.MACARONS})
        .add_xaxis(l1)
        .add_yaxis("", l2)
        .set_global_opts(title_opts=opts.TitleOpts(title="各国亿万富豪平均身价"),
                         datazoom_opts=opts.DataZoomOpts(type_="slider"),
                         yaxis_opts=opts.AxisOpts(name="亿元"),
                         xaxis_opts=opts.AxisOpts(name="国家"))
)
bar.render('./averagewealth.html')
# 三、统计分析哪个行业亿万富豪最多
# 1.数据处理
import pandas as pd

data = pd.read_csv('2020年福布斯排行榜.csv', encoding='gbk')
list_country = list(set(list(data['财富来源'])))  # 去重
dict_country = {}
list_country_count = [list(data['财富来源']).count(i) for i in list_country]
for i, j in zip(list_country, list_country_count):
    dict_country[i] = j
tuple_kind = sorted(dict_country.items(), key=lambda x: x[1], reverse=True)
# 2.数据分析
from pyecharts import options as opts
from pyecharts.charts import Pie
from pyecharts.globals import ThemeType

pie = (
    Pie({"theme": ThemeType.DARK})
        .add(
        "",
        tuple_kind[:20],
        radius=["30%", "75%"],
        rosetype="radius",
        label_opts=opts.LabelOpts(is_show=False),
    )
        .set_global_opts(
        title_opts=opts.TitleOpts(title="各行业亿万富豪占比统计"),
        legend_opts=opts.LegendOpts(type_="scroll", pos_left="90%", orient="vertical"),
    )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}，{d}%"))
)
pie.render('./IndustryBillionaire.html')
