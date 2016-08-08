from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from bs4 import BeautifulSoup
from betExplorer.models import *
from utils import util
import os, requests, copy
from datetime import datetime
import json

def crawlerChampionshipFiles():

    tourneaments = { "serie-a", "serie-b" }

    for t in tourneaments:

        for year in range (2006,2016):

            tourneamentName = t + "-" + str(year)

            url = util.URL_BETEXPLORER + tourneamentName + "/results/"
            fileName = util.BETEXPLORER_FILES + "/championships/" + tourneamentName + ".html"

            if (os.path.exists(fileName)):
                print("JA EXISTE: ", fileName)
            else:
                r = requests.get(url, stream=True)

                file = open(fileName, 'wb')
                file.write(r.content)
                file.close()

                session.add(Championship(name=tourneamentName, year=year))
                session.commit()


def crawlerMatchFiles():

    matches = session.query(Match)

    for match in matches:

        url = "http://www.betexplorer.com//gres/ajax-matchodds.php"

        types = {'1x2', 'ou', 'ah', 'ha', 'dc', 'bts'}
        params = {}
        params['t'] = 'n'
        params['e'] = match.id

        for type in types:

            params['b'] = type
            fileName = util.BETEXPLORER_FILES + "/matches/" + match.id + "_" + type + ".html"

            if (os.path.exists(fileName)):
                print("JA EXISTE: ", )
            else:
                r = requests.get(url,params=params)

                file = open(fileName,'wb')
                file.write(r.content)
                file.close()

def scrapChampionshipFiles():

    championships = session.query(Championship)

    for c in championships:

        fileName = util.BETEXPLORER_FILES + "/championships/" + c.name + ".html"
        file = open(fileName, 'r')

        content = file.read()

        soup = BeautifulSoup(content, 'html.parser')

        text = soup.find(id="leagueresults_tbody")
        trs = text.find_all("tr")

        line = 0
        match = Match()

        for tr in trs:

            if (tr['class'][0] == 'rtitle'):
                round = tr.getText().split(".")[0]
            else:

                tds = tr.find_all('td')

                for td in tds:
                    line = line + 1
                    if (line == 1):
                        match = Match()

                        a = td.find('a')
                        match.id = a['href'].split("=")[1]

                        homeTeamName = td.getText().split(" - ")[0].strip()
                        awayTeamName = td.getText().split(" - ")[1].strip()

                        try:
                            homeTeam = session.query(Team).filter(Team.name==homeTeamName)
                            homeTeam = homeTeam.one()
                        except:
                            homeTeam = Team(name=homeTeamName)
                            session.add(homeTeam)
                            session.commit()

                        try:
                            awayTeam = session.query(Team).filter(Team.name==awayTeamName).one()
                        except:
                            awayTeam = Team(name=awayTeamName)
                            session.add(awayTeam)
                            session.commit()

                        match.homeTeamId = homeTeam.id
                        match.awayTeamId = awayTeam.id
                        match.round = round
                        match.championshipId = c.id

                    elif (line == 2):
                        match.goalsHome = td.getText().split(':')[0]
                        match.goalsAway = td.getText().split(':')[1].split()[0]

                    elif (line == 3):
                        try:
                            match.oddsHome = td['data-odd']
                        except:
                            match.oddsHome = None

                    elif (line == 4):
                        try:
                            match.oddsDraw = td['data-odd']
                        except:
                            match.oddsDraw = None

                    elif (line == 5):
                        try:
                            match.oddsAway = td['data-odd']
                        except:
                            match.oddsAway = None

                    elif (line == 6):
                        dateStr = td.getText()
                        match.matchDate = datetime.strptime(dateStr,"%d.%m.%Y")
                        line = 0

                        try:
                            session.add(match)
                            session.commit()
                        except:
                            session.rollback()
                            match = session.query(Match).filter(Match.id==match.id)


def extractRankingPerMatch():

    championships = session.query(Championship)

    for c in championships:
        print(c)

        teams = session.query(distinct(Team.id)).filter(or_(Match.awayTeamId == Team.id, Match.homeTeamId == Team.id),\
                                                        Match.championshipId == c.id)

        for t in teams:
            print(t)

            matches = session.query(Match).filter(or_(Match.awayTeamId == t[0], Match.homeTeamId == t[0]),\
                                                  Match.championshipId == c.id)\
            .order_by(Match.matchDate)

            winnersHome = 0
            winnersAway = 0
            losesHome = 0
            losesAway = 0
            drawsHome = 0
            drawsAway = 0
            goalsConceded = goalsScored = 0
            goalsScoredHome = 0
            goalsScoredAway = 0
            goalsConcededHome = 0
            goalsConcededAway = 0
            matchesPlayed = lastMatchesNum = 0
            matchesPlayedHome = 0
            matchesPlayedAway = 0
            winners = loses =  draws =  points = 0
            points = pointsHome = pointsAway = 0

            for m in matches:

                r = Ranking()
                r.matchId = m.id
                r.teamId = t[0]
                r.winners = winners
                r.draws = draws
                r.loses = loses
                r.points = points
                r.goalsConceded = goalsConceded
                r.goalsScored = goalsScored
                r.local = 'B'
                r.matchesPlayed = matchesPlayed
                r.lastMatchesNum = matchesPlayed
                session.add(r)
                session.commit()

                if (m.homeTeamId == t[0]):
                    r = Ranking()
                    r.matchId = m.id
                    r.teamId = t[0]
                    r.winners = winnersHome
                    r.draws = drawsHome
                    r.loses = losesHome
                    r.points = pointsHome
                    r.goalsScored = goalsScoredHome
                    r.goalsConceded = goalsConcededHome
                    r.local = 'H'
                    r.matchesPlayed = matchesPlayedHome
                    r.lastMatchesNum = matchesPlayedHome

                    session.add(r)
                    session.commit()

                    matchesPlayedHome = matchesPlayedHome + 1

                    goalsScoredHome = goalsScoredHome + m.goalsHome
                    goalsConcededHome = goalsConcededHome + m.goalsAway

                    if (m.goalsHome > m.goalsAway):
                        winnersHome = winnersHome + 1
                    elif (m.goalsHome < m.goalsAway):
                        losesHome = losesHome + 1
                    else:
                        drawsHome = drawsHome + 1

                    pointsHome = winnersHome*3 + drawsHome

                else:
                    r = Ranking()
                    r.matchId = m.id
                    r.teamId = t[0]
                    r.winners = winnersAway
                    r.draws = drawsAway
                    r.loses = losesAway
                    r.points = pointsAway
                    r.goalsScored = goalsScoredAway
                    r.goalsConceded = goalsConcededAway
                    r.local = 'A'
                    r.matchesPlayed = matchesPlayedAway
                    r.lastMatchesNum = matchesPlayedAway

                    session.add(r)
                    session.commit()

                    matchesPlayedAway = matchesPlayedAway + 1
                    goalsScoredAway = goalsScoredAway + m.goalsAway
                    goalsConcededAway = goalsConcededAway + m.goalsHome

                    if (m.goalsAway > m.goalsHome):
                        winnersAway = winnersAway + 1
                    elif (m.goalsAway < m.goalsHome):
                        losesAway = losesAway + 1
                    else:
                        drawsAway = drawsAway + 1

                    pointsAway = winnersAway*3 + drawsAway

                winners = winnersHome + winnersAway
                loses = losesHome + losesAway
                draws = drawsHome + drawsAway
                goalsScored = goalsScoredHome + goalsScoredAway
                goalsConceded = goalsConcededHome + goalsConcededAway
                points = pointsHome + pointsAway
                matchesPlayed = matchesPlayedHome + matchesPlayedAway

def extractRankingRelativeLastMatches():

    championships = session.query(Championship)
    locals = {'B','H','A'}

    for c in championships:
        print(c)

        teams = session.query(distinct(Team.id)).filter(or_(Match.awayTeamId == Team.id, Match.homeTeamId == Team.id),\
                                                            Match.championshipId == c.id)

        for t in teams:
            print(t)

            for local in locals:

                rankings = session.query(Ranking).filter(Ranking.teamId == t[0], Match.id == Ranking.matchId,\
                                                     Match.championshipId == c.id,\
                                                     Ranking.local == local).order_by(Ranking.matchesPlayed)

                newRankings = extractRanking(rankings,local)
                session.add_all(newRankings)
                session.commit()


def extractRanking(rankings,local):

    nr = []

    for r in rankings:

        for i in range(1, r.matchesPlayed):
            ranking = Ranking()
            ranking.matchId = r.matchId
            ranking.teamId = r.teamId
            ranking.winners = r.winners - rankings[r.matchesPlayed - i].winners
            ranking.draws = r.draws - rankings[r.matchesPlayed - i].draws
            ranking.loses = r.loses - rankings[r.matchesPlayed - i].loses
            ranking.points = r.points - rankings[r.matchesPlayed - i].points
            ranking.goalsScored = r.goalsScored - rankings[r.matchesPlayed - i].goalsScored
            ranking.goalsConceded = r.goalsConceded - rankings[r.matchesPlayed - i].goalsConceded
            ranking.local = local
            ranking.matchesPlayed = r.matchesPlayed
            ranking.lastMatchesNum = i

            nr.append(ranking)

    return nr

def betRelativeLastMatches():

    matches = session.query(Match)
    x = 0

    for match in matches:
        x = x+1
        print(x)

        rankingsHome = session.query(Ranking).\
            filter(Ranking.teamId == match.homeTeamId,\
                                                    Ranking.matchId == match.id,\
                                                    Ranking.local == 'B')

        rankingsAway = session.query(Ranking).\
            filter(Ranking.teamId == match.awayTeamId,\
                                                    Ranking.matchId == match.id,\
                                                    Ranking.local == 'B')
        for rHome in rankingsHome:
            try:
                rAway = rankingsAway.filter(Ranking.lastMatchesNum == rHome.lastMatchesNum).one()

                bet = Bet()
                bet.matchId = match.id
                bet.local = 0
                bet.lastMatchesNum = rHome.lastMatchesNum

                if (rHome.points > rAway.points):
                    bet.betColumn = 0
                elif (rAway.points > rHome.points):
                    bet.betColumn = 2
                else:
                    bet.betColumn = 1

                session.add(bet)
            except:
                print ("Nao encontrou: ", rHome)

        session.commit()

def betRelativeLastMatchesLocal():

    matches = session.query(Match)
    x = 0

    for match in matches:
        x = x+1
        print(x)

        rankingsHome = session.query(Ranking).\
            filter(Ranking.teamId == match.homeTeamId,\
                                                    Ranking.matchId == match.id,\
                                                    Ranking.local == 'H')

        rankingsAway = session.query(Ranking).\
            filter(Ranking.teamId == match.awayTeamId,\
                                                    Ranking.matchId == match.id,\
                                                    Ranking.local == 'A')
        for rHome in rankingsHome:
            try:
                rAway = rankingsAway.filter(Ranking.lastMatchesNum == rHome.lastMatchesNum).one()

                bet = Bet()
                bet.matchId = match.id
                bet.local = 1
                bet.lastMatchesNum = rHome.lastMatchesNum

                if (rHome.points > rAway.points):
                    bet.betColumn = 0
                elif (rAway.points > rHome.points):
                    bet.betColumn = 2
                else:
                    bet.betColumn = 1

                session.add(bet)
            except:
                print ("Nao encontrou: ", rHome)

        session.commit()

def confirmBet():

    bets = session.query(Bet)

    for b in bets:

        match = session.query(Match).filter(Match.id == b.matchId).one()

        if (match.result == b.betColumn):
            b.hit = 1
        else:
            b.hit = 0

    session.commit()

def updateMatchResults():

    matches = session.query(Match)

    for m in matches:

        if (m.goalsHome > m.goalsAway):
            m.result = 0
        elif (m.goalsHome == m.goalsAway):
            m.result = 1
        else:
            m.result = 2


    session.commit()

def scrapOdds():

    championships = session.query(Championship).filter()

    for c in championships:

        print(c)

        matches = session.query(Match).filter(Match.championshipId == c.id)

        for match in matches:

            for type in util.ODDS_TYPES:

                nomeArquivo = util.BETEXPLORER_FILES + "/matches/" + match.id + "_" + type + ".html"

                file = open(nomeArquivo,'r')
                content = file.read()
                content = json.loads(content)
                soup = BeautifulSoup(content['odds'], 'html.parser')

                tbodys = soup.find_all('tbody')

                if (tbodys is not None):
                    for tbody in tbodys:
                        trs = tbody.find_all('tr')
                        createOdds(match, trs, type)


def createOdds(match, trs, type):

    for tr in trs:
        bookmakerName = tr.find('a').getText().strip()
        infos = []
        tds = tr.find_all('td')

        try:
            bookmaker = Bookmaker.get(bookmakerName)
        except:
            bookmaker = Bookmaker(name=bookmakerName)
            session.add(bookmaker)
            session.commit()

        if (type == util.TYPE_OU or type == util.TYPE_AH):
            infos.append(tds[1].getText())
            try:
                infos.append(tds[2]['data-odd'])
            except:
                infos.append(None)
            try:
                infos.append(tds[3]['data-odd'])
            except:
                infos.append(None)
        else:
            size = len(tds)
            for i in range (1,size):
                try:
                    infos.append(tds[i]['data-odd'])
                except:
                    infos.append(None)


        if (type == util.TYPE_1x2):
            odds = Odds(matchId=match.id,bookmakerId=bookmaker.id,\
                        oddsHome=infos[0], oddsDraw=infos[1],oddsAway=infos[2])
        elif (type == util.TYPE_OU):
            odds = OddsOU(matchId=match.id,bookmakerId=bookmaker.id,\
                              goals=infos[0],oddsOver=infos[1],oddsUnder=infos[2])
        elif (type == util.TYPE_AH):
            odds = OddsAH(matchId=match.id,bookmakerId=bookmaker.id,\
                          handicap=infos[0],oddsHome=infos[1],oddsAway=infos[2])
        elif (type == util.TYPE_DNB):
            odds = OddsDNB(matchId=match.id,bookmakerId=bookmaker.id,\
                        oddsHome=infos[0], oddsAway=infos[1])
        elif (type == util.TYPE_DC):
             odds = OddsDC(matchId=match.id,bookmakerId=bookmaker.id,\
                        oddsHomeDraw=infos[0], oddsHomeAway=infos[1], oddsAwayDraw=infos[2])
        elif (type == util.TYPE_BTS):
            odds = OddsBTS(matchId=match.id,bookmakerId=bookmaker.id,\
                        oddsYes=infos[0], oddsNo=infos[1])

        try:
            odds.save()
            session.commit()
        except:
            session.rollback()


def fixRounds2008 ():

    fileName = 'rounds2008.txt'

    round_num = 1
    games = 1
    c = Championship().get("serie-a-2008")

    matches = c.listMatches()
    with open(fileName, 'r') as rows:
        for r in rows:

            teamHome = r.split(" – ")[1].split("x")[0][:-1].strip()
            teamAway = r.split(" – ")[1].split("x")[1][2:].strip()
            teamHome = Team().get(teamName=teamHome)
            teamAway = Team().get(teamName=teamAway)

            for m in matches:
                if (m.homeTeamId == teamHome.id and m.awayTeamId == teamAway.id):
                    print("entrou")
                    if (games == 11):
                        round_num = round_num + 1
                        games = 1
                    m.round = round_num
                    games = games + 1
                    m.save()


    session.commit()






fixRounds2008()


