import csv
with open("starbucks_response.txt") as file:
    list_string = file.read()


location_dicts_list = eval(list_string)


lat_longs = list(map(lambda x: (
    x['latitude'], x['longitude'], x['address']), location_dicts_list))

header = ['Latitude', 'Longitude', "Address"]
with open('starbucks_latlong1.csv', 'w', newline='') as f:

    writer = csv.writer(f)
    writer.writerow(header)

    for lat_long in lat_longs:
        writer.writerow(lat_long)
