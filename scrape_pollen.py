import json
import requests

from bs4 import BeautifulSoup
from datetime import datetime


class PollenResult(dict):
    def __init__(self, region, date_for, measurement):
        dict.__init__(self, region=region, date_for=date_for,
                      measurement=measurement)


standard_date = '%Y-%d-%m'  # ISO 8601
met_date = '%d-%m-%Y'
URL = "https://www.met.ie/forecasts/pollen"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(class_="pollen")

result_table = results.find("table")

rows = result_table.findChildren('tr')

date_row = rows[1].findChildren('th')

date_res = []
for i in range(1, len(date_row)):
    date_res.append(datetime.strptime(date_row[i].string, met_date))


region_rows = rows[2:]
pollen_results = []

for region_row in region_rows:
    data_fields = region_row.findChildren('td')
    region = data_fields[0].string
    for i in range(1, len(date_row)):
        pollen_results.append(PollenResult(region,
                              date_res[i-1].strftime(standard_date),
                              data_fields[i].string))
