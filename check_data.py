
import csv
from pathlib import Path

HERE = Path(__file__).parent
FILE = HERE / "data" / "hko-daily-rainfall-all-years.csv"

with open(FILE, encoding="utf-8-sig") as f:
    reader = csv.reader(f)

    for row in reader:


        if row and row[0] == "2025":
       
            print(row)

            rainfall = row[3]

            if rainfall == "Trace":
                rainfall = 0.0
            else:
                rainfall = float(rainfall)

            print("Type:", type(rainfall))
            print("Rainfall:", rainfall)

            break
