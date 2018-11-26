import requests
import csv

details = []
with open('playerdetails.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        d = [row[0], row[1], row[2], row[3]]
        details.append(d)

url = 'http://analytics05.cricket.net/xquery/espn/player'
for i, d in enumerate(details):
    payload = "{\"type\":\"player-year\",\"format\":\"t20\",\"player_id\":\""+str(d[3])+"\",\"ttl\":300,\"year\":[\"2016\",\"2017\"]}"
    headers = {
        'Cache-Control': "no-cache",
        'Postman-Token': "3c425c86-f3bd-4542-9342-acc1147eb269"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    if response.status_code != 200:
        continue
    parsedata = response.json()
    wickets = 0
    runs = 0
    for data in parsedata:
        if not data['bowler/wickets']:
            data['bowler/wickets'] = 0
        if not data['batsman/runs']:
            data['batsman/runs'] = 0
        wickets += int(data['bowler/wickets'])
        runs += int(data['batsman/runs'])
    d.append(runs)
    d.append(wickets)

with open('playerstats.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    for d in details:
        if d[-1] >= 35 or d[-2] >= 900:
            writer.writerow(d)