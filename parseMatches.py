from bs4 import BeautifulSoup
import csv
import urllib2

teamrowentry = []
playerrowentry = []
top10teams=['Afghanistan','Australia', 'Bangladesh', 'England', 'India', 'New Zealand', 'Pakistan', 'South Africa', 'Sri Lanka', 'West Indies']

def ExtractPlayerInvolveId(player_name):
    initial_url = 'http://stats.espncricinfo.com/ci/engine/player/33335.html?class=3;filter=advanced;orderby=default;'
    if " " in player_name:
        search_player = player_name.split()
        player_name = search_player[0] + '+' + search_player[1]
    final_url = initial_url + 'search_player=' + player_name + ';type=allround'
    url = urllib2.urlopen(final_url)
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
    with open(filename, 'wb') as csv_file:
        writer = csv.writer(csv_file)
        for value in rowentry:
            writer.writerow(value)


def populate_data(teamfilename, playerfilename):
    pages = [
        'http://stats.espncricinfo.com/ci/engine/stats/index.html?class=3;filter=advanced;orderby=start;size=200;spanmax1=31+Dec+2017;spanmin1=01+Jan+2016;spanval1=span;team=1;team=2;team=25;team=3;team=4;team=40;team=5;team=6;team=7;team=8;template=results;type=aggregate;view=results']
    numpages = 1
    # for p in range(1, int(numpages) + 1):
    pg = pages[0]
    # + '&page=' + str(p)
    page = urllib2.urlopen(pg)
    soup = BeautifulSoup(page, 'html.parser')
    table = soup.find_all('table', attrs={'class': 'engineTable'})
    showctr = 0
    for child in table:
        # find teams
        rows = child.find_all('td', attrs={'class': 'left'})
        for r in rows:
            text = r.getText()
            if 'Showing' in text and showctr == 0:
                numrows = int(text.split()[-1])
                showctr += 1
            teams = text.split(' v ')
            if len(teams) == 2:
                if teams[0] in top10teams and teams[1] in top10teams:
                    if numrows > 0:
                        if [teams[0], teams[1]] not in teamrowentry and \
                                    [teams[1], teams[0]] not in teamrowentry:
                            teamrowentry.append([teams[0], teams[1]])
                        numrows = numrows-1

    store_data(teamfilename, teamrowentry)

    # find players
    matchurls = []
    scorecards = soup.find_all('div', attrs={'class': 'engine-dd'})
    for child in scorecards:
        rows = child.find_all('a')
        for links in rows:
            if links.getText() == 'Match scorecard':
                matchurls.append('http://stats.espncricinfo.com' + links.get('href'))

    for match in matchurls:
        page = urllib2.urlopen(match)
        soup = BeautifulSoup(page, 'html.parser')

        batsmen = soup.find_all('div', attrs={'class': 'cell batsmen'})
        for child in batsmen:
            rows = child.find_all('a')
            for r in rows:
                names = r.getText().encode('ascii', 'ignore').split()
                if len(names) > 1:
                    name = names[0] + ' ' + names[1]
                else:
                    name = names[0]
                link = r.get('href')

                playerpage = urllib2.urlopen(link)
                playersoup = BeautifulSoup(playerpage, 'html.parser')
                countrytag = playersoup.find_all('div', attrs={'class': 'icc-home'})
                playerdetails = ['','','']
                for sub in countrytag:
                    subrows = sub.find_all('a')
                    for s in subrows:
                        playerdetails = s.getText().encode('ascii', 'ignore').split('/')
                country = playerdetails[1]
                if country.strip() not in top10teams:
                    continue
                playerInvolve = ExtractPlayerInvolveId(name)

                link = link.replace('/','.')
                links = link.split('.')
                playerid = int(links[-2])
                if [playerid, name, country, playerInvolve] not in playerrowentry:
                    playerrowentry.append([playerid, name, country, playerInvolve])

        store_data(playerfilename, playerrowentry)

        batsmen = soup.find_all('div', attrs={'class': 'cell'})
        for child in batsmen:
            rows = child.find_all('a')
            for r in rows:
                link = r.get('href')
                if link and link[0] == '#' or not link:
                    continue

                playerpage = urllib2.urlopen(link)
                playersoup = BeautifulSoup(playerpage, 'html.parser')
                countrytag = playersoup.find_all('div', attrs={'class': 'icc-home'})
                playerdetails = ['', '', '']
                for sub in countrytag:
                    subrows = sub.find_all('a')
                    for s in subrows:
                        playerdetails = s.getText().encode('ascii', 'ignore').split('/')
                country = playerdetails[1]
                if country.strip() not in top10teams:
                    continue

                link = link.replace('/', '.')
                links = link.split('.')
                playerid = int(links[-2])
                name = r.getText()
                name = name.replace(',', '')
                names = name.encode('ascii', 'ignore').split()
                if len(names) > 1:
                    name = names[0] + ' ' + names[1]
                else:
                    name = names[0]
                playerInvolve = ExtractPlayerInvolveId(name)
                if [playerid, name, country, playerInvolve] not in playerrowentry:
                    playerrowentry.append([playerid, name, country, playerInvolve])

        store_data(playerfilename, playerrowentry)

populate_data('teamvteam.csv', 'playerdetails.csv')
