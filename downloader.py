import requests
import json
import os
from os.path import exists
headers = {
    "Host": "statsapi.web.nhl.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}
shouldDownloadTeams = False
shouldDownloadPlayers = False
shouldDownloadSchedules = False
shouldDownloadStats = False
shouldDownloadGames = False
startYear = 2010
endYear = 2023

def download():
    #TEAMS
    if shouldDownloadTeams: 
        resp = requests.get("https://statsapi.web.nhl.com/api/v1/teams/", headers=headers)
        if not os.path.exists(".\\teams"):
            os.makedirs(".\\teams")
        with open("teams\\teams.json", "w") as my_file:
            my_file.write(resp.text)

    f = open('teams\\teams.json')
    data = json.load(f)

    for i in data['teams']:
        resp = requests.get("https://statsapi.web.nhl.com/api/v1/teams/" + str(i['id']) + "?expand=team.roster", headers=headers)
        with open("teams\\" + str(i['id']) + ".json", "w") as my_file:
            my_file.write(resp.text)
            
        #SCHEDULES
        t = open("teams\\" + str(i['id']) + ".json")
        tdata = json.load(t)

        for year in range(endYear, startYear, -1):
            if shouldDownloadSchedules:
                resp = requests.get("https://statsapi.web.nhl.com/api/v1/schedule?teamId=" + str(i['id']) + "&startDate=" + str(year-1) + "-10-01&endDate=" + str(year) + "-10-01&gameType=R", headers=headers)
                if not os.path.exists(".\\schedules"):
                    os.makedirs(".\\schedules")
                if not os.path.exists(".\\schedules\\" + str(year)):
                    os.makedirs(".\\schedules\\" + str(year))
                with open(".\\schedules\\" + str(year) + "\\" + str(i['id']) + ".json", "w") as my_file:
                    my_file.write(resp.text)
                    
            #GAMES
            s = open(".\\schedules\\" + str(year) + "\\" + str(i['id']) + ".json")
            sdata = json.load(s)

            for date in sdata['dates']:
                for game in date['games']:
                    if shouldDownloadGames and not exists(".\\games\\" + str(year) + "\\" + str(game['gamePk']) + ".json"):
                        resp = requests.get("https://statsapi.web.nhl.com/api/v1/game/" + str(game['gamePk']) + "/feed/live", headers=headers)
                        if not os.path.exists(".\\games"):
                            os.makedirs(".\\games")
                        if not os.path.exists(".\\games\\" + str(year)):
                            os.makedirs(".\\games\\" + str(year))
                        with open(".\\games\\" + str(year) + "\\" + str(game['gamePk']) + ".json", "w") as my_file:
                            my_file.write(resp.text)
            
        #PLAYERS
        t = open("teams\\" + str(i['id']) + ".json")
        tdata = json.load(t)

        for team in tdata['teams']:
            for player in team['roster']['roster']:
                if shouldDownloadPlayers:
                    resp = requests.get("https://statsapi.web.nhl.com/api/v1/people/" + str(player['person']['id']), headers=headers)
                    if not os.path.exists(".\\players"):
                        os.makedirs(".\\players")
                    with open(".\\players\\" + str(player['person']['id']) + ".json", "w") as my_file:
                        my_file.write(resp.text)
                    
                #STATS
                for year in range(endYear, startYear, -1):
                    if shouldDownloadStats:
                        resp = requests.get("https://statsapi.web.nhl.com/api/v1/people/" + str(player['person']['id']) + "/stats?stats=statsSingleSeason&season=" + str(year-1) + str(year), headers=headers)
                        if not os.path.exists(".\\stats"):
                            os.makedirs(".\\stats")
                        if not os.path.exists(".\\stats\\" + str(year)):
                            os.makedirs(".\\stats\\" + str(year))
                        with open(".\\stats\\" + str(year) + "\\" + str(player['person']['id']) + ".json", "w") as my_file:
                            my_file.write(resp.text)
                        
        t.close()
    f.close()
  
download()