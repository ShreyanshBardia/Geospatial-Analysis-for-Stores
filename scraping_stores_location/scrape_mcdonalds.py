import re
import requests
import csv

response = requests.get(
    "https://www.mcdonaldsindia.com/googlemap.php?state=Maharashtra")

m = re.search(r"<h3>Mumbai</h3>"+r"(.+?)"+r"<h3>Nasik</h3>",
              response.text, flags=re.DOTALL,)

lat_long_list = re.findall(r"lat="+r"(.+)"+r"</li>", m[1])

address = re.findall(r"<h2>"+r"(.+?)"+r"<", m[1], flags=re.DOTALL)

lat_longs = list(
    map(lambda x: (float(x.split("'")[1]), float(x.split("'")[3])), lat_long_list))


header = ['Latitude', 'Longitude', "Address"]
with open('mcdonalds_latlong1.csv', 'w', newline='') as f:

    writer = csv.writer(f)
    writer.writerow(header)

    for i in range(len(lat_longs)):
        writer.writerow((*lat_longs[i], address[i].replace("\n", "")))
