import requests
from bs4 import BeautifulSoup

URL = "https://www.met.ie/forecasts/pollen"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(class_="pollen")

print(results.prettify())

