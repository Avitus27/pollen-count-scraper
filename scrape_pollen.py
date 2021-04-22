import json
import requests

from bs4 import BeautifulSoup
from datetime import datetime

class PollenResult(dict):
    def __init__(self, region, date_for, measurement):
      dict.__init__(self, region = region, date_for = date_for, measurement = measurement)


standard_date = '%Y-%d-%m' # ISO 8601
URL = "https://www.met.ie/forecasts/pollen"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(class_="pollen")

result_table = results.find("table")

rows = result_table.findChildren('tr')

date_row = rows[1].findChildren('th')

first_date = datetime.strptime(date_row[1].string, '%d-%m-%Y')
second_date = datetime.strptime(date_row[2].string, '%d-%m-%Y')
third_date = datetime.strptime(date_row[3].string, '%d-%m-%Y')

# TODO: The dates should be put in a list to be refferred to later on.

region_rows = rows[2:]
pollen_results = []

for region_row in region_rows:
    data_fields = region_row.findChildren('td')
    region = data_fields[0].string
    # TODO: When the above TODO is fixed, this should be changed to iterate over each data_field[1-3], dates[0-2]
    pollen_results.append(PollenResult(region, first_date.strftime(standard_date), data_fields[1].string))
    pollen_results.append(PollenResult(region, second_date.strftime(standard_date), data_fields[2].string))
    pollen_results.append(PollenResult(region, third_date.strftime(standard_date), data_fields[3].string))

