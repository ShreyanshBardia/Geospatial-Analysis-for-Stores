import requests
import json
import re
import csv
from bs4 import BeautifulSoup
import lxml


z1 = requests.get("https://www.dominos.co.in/store-locations/mumbai")
z2 = requests.get("https://www.dominos.co.in/store-locations/thane")
z3 = requests.get("https://www.dominos.co.in/store-locations/navi-mumbai")


soup1 = BeautifulSoup(z1.text, "lxml")
soup2 = BeautifulSoup(z2.text, "lxml")
soup3 = BeautifulSoup(z3.text, "lxml")

rows = [("Latitude", "Longitude", "Address")]

for soup in [soup1, soup2, soup3]:

    div_slider = soup.find('div', attrs={"class": "responsive"})

    location_divs = div_slider.find_all(
        'div', attrs={"class": "slider-content stores-slider"})

    links = map(lambda x: x.find("a", href=True)['href'], location_divs)

    for link in links:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'lxml')
        try:
            address_dict = json.loads(soup.find(
                'script', attrs={'type': "application/ld+json"}).text.replace("\\", "\\\\"))
        except Exception as e:
            print(e, soup.find('script', attrs={
                  'type': "application/ld+json"}).text)
        address = address_dict['address']['streetAddress']
        m = re.search(r"LatLng\("+r"(.+)"+r"\)", response.text)
        if m:
            found = m.group(1)
            lat, long = tuple(map(lambda x: x.strip(), found.split(",")))
            rows.append((lat, long, address))

with open('dominos_latlongadd_n.csv', 'w', newline='') as f:

    writer = csv.writer(f)

    for row in rows:
        writer.writerow(row)
