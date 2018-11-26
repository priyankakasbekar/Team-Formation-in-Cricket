from bs4 import BeautifulSoup
import csv
import urllib.request

def ExtractPlayersFromCountry(country_name):
    with open('playerdetails.csv', 'r') as csv_file:
        team_Info = []
        for row in csv.reader(csv_file):
            if row[2] == ' '+country_name+' ':
                team_Info.append(row)
        return(team_Info)

def ExtractNumOfMatches(player_id,player_involve_id):
    player_url = 'http://stats.espncricinfo.com/ci/engine/player/'
    player_id = player_id
    other_filters_url = '.html?class=3;filter=advanced;opposition=1;opposition=2;opposition=25;opposition=3;opposition=4;opposition=40;opposition=5;opposition=7;opposition=8;orderby=default;player_involve='
    player_involve = player_involve_id
    remaining_url = ';spanmax1=31+Dec+2017;spanmin1=01+Jan+2016;spanval1=span;template=results;type=allround'
    complete_url = player_url + player_id + other_filters_url + player_involve + remaining_url
    page = urllib.request.urlopen(complete_url)
    soup = BeautifulSoup(page, 'html.parser')
    table = soup.findAll('table')[2]
    if table.find('thead'):
        header_info = table.findAll('thead')[0]
        header_text = header_info.findAll('th')[2].string

        for row in soup.findAll('table')[2].findAll('tr')[2:]:
            if header_text == 'Mat':
                cells = row.findAll('td')[2].string
            else:
                cells = row.findAll('td')[1].string
        return cells
    else:
        return 0;

def ExtractPlayerInvolveId(player_name):
    initial_url = 'http://stats.espncricinfo.com/ci/engine/player/33335.html?class=3;filter=advanced;orderby=default;'
    if " " in player_name:
        search_player = player_name.split()
        player_name = search_player[0] + '+' + search_player[1]
    final_url = initial_url + 'search_player=' + player_name + ';type=allround'
    url = urllib.request.urlopen(final_url)
    soup1 = BeautifulSoup(url, 'html.parser')
    form = soup1.find('form',attrs={'name': 'gurumenu'})
    table = form.findAll('table')[0]
    row = table.findAll('tr')[30]
    cells = row.findAll('td')[1]
    chkbox = cells.find('input', attrs = {'name':'player_involve'})
    if chkbox is not None:
        player_involve_id = chkbox.get('value')
        return(player_involve_id)
    else:
        return 0

def store_data(filename, rowentry):
    with open(filename, 'a') as csv_file:
        writer = csv.writer(csv_file)
        for value in rowentry:
            writer.writerow(value)

def CreateTeamWiseStats(country_name):
    team_info = ExtractPlayersFromCountry(country_name)
    with open('player_records_'+country_name+'.csv', 'w') as csvfile:
        csvfile.truncate()
        i = 0;
    for player in team_info:
        i = i+1;
        for associated_player in team_info[i:]:
            if player[0] != associated_player[0]:
                player_involve_id = ExtractPlayerInvolveId(associated_player[1])
                if player_involve_id is not 0:
                    num_of_matches = ExtractNumOfMatches(player[0],player_involve_id)
                    with open('player_records_'+country_name+'.csv', 'a') as csvfile:
                        writer = csv.writer(csvfile, delimiter=',')
                        writer.writerow([player[1],associated_player[1],str(num_of_matches)])
                else:
                    continue

def CreatePlayerStats():
    countries[] = ['India','Australia','South Africa','Pakistan','Sri Lanka','Afghanistan','Bangladesh','West Indies','New Zealand','England']
    opposition_dict = { }
    opposition_dict['India'] = '6'
    opposition_dict['Australia'] = '2'
    opposition_dict['South Africa'] = '3'
    opposition_dict['Pakistan'] = '7'
    opposition_dict['Sri Lanka']= '8'
    opposition_dict['New Zealand'] = '5'
    opposition_dict['Afghanistan'] = '40'
    opposition_dict['West Indies'] = '4'
    opposition_dict['England']= '1'
    opposition_dict['Bangladesh'] = '25'
CreateTeamWiseStats('India')
