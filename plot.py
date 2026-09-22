
# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///

"""
Hong Kong daily temperature and rainfall in 2025.

Read two raw CSV files, match them by date,
and draw a weather visualisation.
"""

import csv
from pathlib import Path
from datetime import date

import matplotlib.pyplot as plt
import matplotlib.dates as mdates



HERE = Path(__file__).parent
DATA = HERE / "data"
OUT = HERE / "out"

TEMP_FILE = DATA / "hko-daily-mean-temperature-2025.csv"

RAIN_FILE = DATA / "hko-daily-rainfall-all-years.csv"

PICTURE = "hk-weather-2025.png"


def rows(path):

    kept = []

    with path.open(
        encoding="utf-8-sig",
        newline=""
    ) as handle:

        for line in csv.reader(handle):

            if line and line[0].isdigit():
                kept.append(line)

    return kept



def to_number(value):

    if value == "Trace":
        return 0.0

    if value in ("***", "", "N/A"):
        return None

    return float(value)


def main():


    temp_table = rows(TEMP_FILE)
    rain_table = rows(RAIN_FILE)

    print("Temperature:", temp_table[0])
    print("Rainfall:", rain_table[0])



    temperatures = {}
    rainfall = {}



    for year, month, day, value, quality in temp_table:

        if year != "2025":
            continue

        number = to_number(value)

        if number is None:
            continue

        when = date(
            int(year),
            int(month),
            int(day)
        )

        temperatures[when] = number



    for year, month, day, value, quality in rain_table:

        if year != "2025":
            continue

        number = to_number(value)

        if number is None:
            continue

        when = date(
            int(year),
            int(month),
            int(day)
        )

        rainfall[when] = number



    dates = sorted(
        set(temperatures) & set(rainfall)
    )

    temp_values = [
        temperatures[d] for d in dates
    ]

    rain_values = [
        rainfall[d] for d in dates
    ]


    print("Matched days:", len(dates))

    print(
        "Temperature range:",
        min(temp_values),
        "to",
        max(temp_values)
    )

    print(
        "Rainfall range:",
        min(rain_values),
        "to",
        max(rain_values)
    )



    fig, ax1 = plt.subplots(
        figsize=(14, 6)
    )



    ax1.plot(
        dates,
        temp_values,
        color="#E76F51",
        linewidth=1.5,
        label="Temperature"
    )

    ax1.set_ylabel(
        "Daily Mean Temperature (°C)",
        color="#E76F51"
    )

    ax1.tick_params(
        axis="y",
        labelcolor="#E76F51"
    )



    ax2 = ax1.twinx()

    ax2.bar(
        dates,
        rain_values,
        color="#4EA8DE",
        alpha=0.5,
        width=1,
        label="Rainfall"
    )

    ax2.set_ylabel(
        "Daily Total Rainfall (mm)",
        color="#4EA8DE"
    )

    ax2.tick_params(
        axis="y",
        labelcolor="#4EA8DE"
    )


    ax1.set_title(
        "Hong Kong Weather in 2025\n"
        "Daily Temperature and Rainfall",
        fontsize=16
    )

    ax1.set_xlabel("Month")

    ax1.xaxis.set_major_locator(
        mdates.MonthLocator()
    )

    ax1.xaxis.set_major_formatter(
        mdates.DateFormatter("%b")
    )

    ax1.set_xlim(
        date(2025, 1, 1),
        date(2025, 12, 31)
    )

    ax1.grid(
        axis="y",
        alpha=0.2
    )



    fig.tight_layout()

    OUT.mkdir(exist_ok=True)

    fig.savefig(
        OUT / PICTURE,
        dpi=150
    )

    print(f"Saved out/{PICTURE}")

    plt.show()


if __name__ == "__main__":
    main()
