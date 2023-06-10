import json
import csv
import os 
 
shouldConvertTeams = False
shouldConvertPlayers = False
shouldConvertStats = True
shouldConvertSchedules = False
shouldConvertGames = False

if shouldConvertTeams:
    with open('teams\\teams.json') as json_file:
        jsondata = json.load(json_file)
     
    data_file = open('teams.csv', 'w', newline='')
    csv_writer = csv.writer(data_file)
     
    count = 0
    for data in jsondata['teams']:
        if count == 0:
            header = data.keys()
            csv_writer.writerow(header)
            count += 1
        csv_writer.writerow(data.values())
     
    data_file.close()
    
if shouldConvertPlayers:
    data_file = open('players.csv', 'w', newline='')
    count = 0
    for playerFile in os.listdir('players'):
        with open('players\\' + str(playerFile)) as json_file:
            jsondata = json.load(json_file)
         
        csv_writer = csv.writer(data_file)
        for data in jsondata['people']:
            if count == 0:
                header = data.keys()
                csv_writer.writerow(header)
                count += 1
            csv_writer.writerow(data.values())
         
    data_file.close()
    
if shouldConvertStats:
    data_file = open('stats.csv', 'w', newline='')
    count = 0
    for year in os.listdir('stats'):
        for statFile in os.listdir('stats\\' + str(year)):
            with open('stats\\' + str(year) + '\\' + str(statFile)) as json_file:
                jsondata = json.load(json_file)
             
            csv_writer = csv.writer(data_file)
            allStats = jsondata['stats'][0]
            if len(allStats['splits']) == 0:
                continue
            data = allStats['splits'][0]['stat']
            if count == 0:
                header = data.keys()
                csv_writer.writerow(header)
                count += 1
            csv_writer.writerow(data.values())
         
    data_file.close()