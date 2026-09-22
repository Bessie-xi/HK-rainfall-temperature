
# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import csv

HERE = Path(__file__).parent
OUT = HERE / "out"
RAIN_FILE = HERE / "data" / "hko-daily-rainfall-all-years.csv"

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

print("Number of days:", len(rainfall))
print("First 10 rainfall values:", rainfall[:10])

if len(rainfall) != DAYS:
    raise ValueError("Expected 365 days of rainfall data")

if any(value is None for value in rainfall):
    raise ValueError("Some rainfall values are missing")


fig, ax = plt.subplots(figsize=(10, 10))

ax.set_aspect("equal")

angles = np.linspace(
    0,
    2 * np.pi,
    DAYS,
    endpoint=False
)


# 画365片花瓣
for angle, rain in zip(angles, rainfall):

    # 每片花瓣的长度由降雨量决定
    length = 0.25 + rain / 100

    x = length * np.cos(angle)
    y = length * np.sin(angle)

    ax.plot(
        [0, x],
        [0, y],
        color="#E9A6B0",
        linewidth=2,
        solid_capstyle="round"
    )


flower_center = plt.Circle(
    (0, 0),
    0.12,
    color="#F6D77A"
)

ax.add_patch(flower_center)

ax.axis("off")

max_length = 0.25 + max(rainfall) / 100
limit = max_length * 1.1

ax.set_xlim(-limit, limit)
ax.set_ylim(-limit, limit)

ax.set_title(
    "Hong Kong Weather Flower\n365 Days, One Bloom",
    fontsize=18
)

OUT.mkdir(exist_ok=True)

fig.savefig(
    OUT / "weather-flower-2025.png",
    dpi=200,
    bbox_inches="tight"
)

print("Saved out/weather-flower-2025.png")

plt.show()
