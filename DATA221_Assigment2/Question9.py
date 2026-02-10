import csv
import requests
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/Machine_learning"

# IMPORTANT: add User-Agent
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, "html.parser")

# main content area
content_div = soup.find("div", id="mw-content-text")

# find the first table with at least 3 data rows
target_table = None

for table in content_div.find_all("table"):
    rows = table.find_all("tr")
    data_row_count = 0

    for r in rows:
        if r.find_all("td"):
            data_row_count += 1

    if data_row_count >= 3:
        target_table = table
        break

# get all rows from the chosen table
rows = target_table.find_all("tr")

# extract headers
header_cells = rows[0].find_all("th")
if header_cells:
    headers = [h.get_text(strip=True) for h in header_cells]
else:
    max_cols = 0
    for r in rows:
        cols = r.find_all("td")
        max_cols = max(max_cols, len(cols))
    headers = [f"col{i+1}" for i in range(max_cols)]

# extract table data
data = []
max_cols = len(headers)

for r in rows:
    cells = r.find_all("td")
    if not cells:
        continue

    row_text = [c.get_text(" ", strip=True) for c in cells]

    # pad missing columns
    if len(row_text) < max_cols:
        row_text += [""] * (max_cols - len(row_text))
    elif len(row_text) > max_cols:
        row_text = row_text[:max_cols]

    data.append(row_text)

# save to CSV
with open("wiki_table.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(data)

print("Saved table to wiki_table.csv")
print("Rows saved:", len(data))

