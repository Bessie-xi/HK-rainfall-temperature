
# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.cm import ScalarMappable
import csv


HERE = Path(__file__).parent
OUT = HERE / "out"

RAIN_FILE = HERE / "data" / "hko-daily-rainfall-all-years.csv"
TEMP_FILE = HERE / "data" / "hko-daily-mean-temperature-2025.csv"

DAYS = 365


rainfall = []

with open(
    RAIN_FILE,
    encoding="utf-8-sig",
    newline=""
) as file:

    reader = csv.reader(file)

    for row in reader:

        if not row or row[0] != "2025":
            continue

        value = row[3].strip()

        if value == "Trace":
            value = 0.0

        elif value in ("***", "", "N/A"):
            value = None

        else:
            value = float(value)

        rainfall.append(value)


# ------------------------------------
# 读取2025年每天的平均气温
# ------------------------------------

temperature = []

with open(
    TEMP_FILE,
    encoding="utf-8-sig",
    newline=""
) as file:

    reader = csv.reader(file)

    for row in reader:

        # 只读取2025年的数据
        if not row or row[0] != "2025":
            continue

        value = row[3].strip()

        # 跳过缺失的气温数据
        if value in ("***", "", "N/A"):
            value = None
        else:
            value = float(value)

        temperature.append(value)

print("Number of temperature days:", len(temperature))

if len(temperature) != DAYS:
    raise ValueError("Expected 365 days of temperature data")

if any(value is None for value in temperature):
    raise ValueError("Some temperature values are missing")


print("Number of days:", len(rainfall))

if len(rainfall) != DAYS:
    raise ValueError("Expected 365 days of rainfall data")

if any(value is None for value in rainfall):
    raise ValueError("Some rainfall values are missing")



weekly_rainfall = []

for i in range(0, DAYS, 7):

    one_week = rainfall[i:i + 7]

    total_rain = sum(one_week)

    weekly_rainfall.append(total_rain)

print("Number of weeks:", len(weekly_rainfall))
print("Weekly rainfall:", weekly_rainfall)


# ------------------------------------
# 计算每周平均气温
# ------------------------------------

weekly_temperature = []

for i in range(0, DAYS, 7):

    # 取出这一周每天的气温
    one_week = temperature[i:i + 7]

    # 计算这一周的平均气温
    average_temp = sum(one_week) / len(one_week)

    # 保存这一周的平均气温
    weekly_temperature.append(average_temp)

print("Number of temperature weeks:", len(weekly_temperature))
print("Weekly temperature:", weekly_temperature)



fig, ax = plt.subplots(figsize=(10, 6))

WEEKS = len(weekly_rainfall)

# 控制线条间距，数字越小，排列越紧密
SPACING = 0.65

weeks = np.arange(WEEKS) * SPACING


lengths = []

for rain in weekly_rainfall:

  
    length = 0.5 + np.sqrt(rain) * 0.2

    lengths.append(length)


# 创建从浅红色到深红色的渐变

temperature_colors = LinearSegmentedColormap.from_list(
    "HongKongTemperature",
    [
        "#FFF5F5",  # 最低温：接近白色的浅红
        "#F4A3A3",  # 中间温度：粉红色
        "#B91C1C"   # 最高温：深红色
    ]
)

# 找到全年最低和最高的周平均气温
min_temp = min(weekly_temperature)
max_temp = max(weekly_temperature)

# 把气温转换成0到1之间的数字
temp_norm = Normalize(
    vmin=min_temp,
    vmax=max_temp
)



# 每周降雨量决定长度
# 每周平均气温决定颜色

for week, length, temp in zip(
    weeks,
    lengths,
    weekly_temperature
):

    # 把这一周的气温转换成红色
    line_color = temperature_colors(
        temp_norm(temp)
    )

    # 绘制上下对称的线条
    ax.plot(
        [week, week],
        [-length / 2, length / 2],
        color=line_color,
        linewidth=10,
        solid_capstyle="round"
    )



max_length = max(lengths)


ax.set_ylim(
    -max_length * 0.6,
    max_length * 0.6
)

ax.set_xlim(
    -SPACING,
    weeks[-1] + SPACING
)


ax.set_xticks(
    weeks[[0, 13, 26, 39, 52]]
)
ax.set_xticklabels(
    ["Jan", "Apr", "Jul", "Oct", "Dec"],
    fontsize=12
)

ax.set_xlabel(
    "Week of 2025",
    fontsize=12,
    labelpad=15
)

ax.set_yticks([])

for spine in ax.spines.values():
    spine.set_visible(False)

ax.tick_params(axis="x", length=0)



# ------------------------------------
# 添加右下角的温度颜色图例
# ------------------------------------

# 创建颜色图例的数据对象
sm = ScalarMappable(
    norm=temp_norm,
    cmap=temperature_colors
)

# 在图表右下角创建一个小区域
legend_ax = ax.inset_axes(
    [0.73, 0.06, 0.24, 0.025]
)

# 绘制横向渐变颜色条
colorbar = fig.colorbar(
    sm,
    cax=legend_ax,
    orientation="horizontal"
)

# 显示最低和最高周平均气温
colorbar.set_ticks([
    min_temp,
    max_temp
])

colorbar.set_ticklabels([
    f"{min_temp:.1f}°C",
    f"{max_temp:.1f}°C"
])

# 在颜色条上方添加标题
colorbar.ax.set_title(
    "Weekly Mean Temperature",
    fontsize=9,
    pad=8
)

# 调整数字大小
colorbar.ax.tick_params(
    labelsize=8,
    length=0
)

# 去掉颜色条的黑色边框
colorbar.outline.set_visible(False)

ax.set_title(
    "Hong Kong Weather Rhythm\n"
    "53 Weekly Rainfall Groups in 2025",
    fontsize=20,
    pad=30
)

fig.tight_layout()

OUT.mkdir(exist_ok=True)

fig.savefig(
    OUT / "weather-rhythm-2025.png",
    dpi=200,
    bbox_inches="tight"
)

print("Saved out/weather-rhythm-2025.png")

plt.show()
