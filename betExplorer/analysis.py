from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from bs4 import BeautifulSoup
from betExplorer.models import *
from utils import util
import os, requests, copy
from datetime import datetime
from decimal import *
import statistics
from tabulate import tabulate

def simpleHomeDrawAway():

    championships = session.query(Championship)
    table = []

    for c in championships:

        matches = session.query(Match).filter(Match.championshipId == c.id)

        profits = [0,0,0]
        results = [0,0,0]
        odds = [Decimal(0),Decimal(0),Decimal(0)]

        games = 0
        for match in matches:

            if (match.oddsHome is None):
                oddsHome = 0
            else:
                games = games + 1
                oddsHome = match.oddsHome

            if (match.oddsHome is None):
                oddsAway = 0
            else:
                oddsAway = match.oddsAway

            if (match.oddsDraw is None):
                oddsDraw = 0
            else:
                oddsDraw = match.oddsDraw

            #Quantidade de jogos | apostas casa/local/visitante
            if (match.goalsHome > match.goalsAway):
                results[0] = results[0] + 1
                odds[0] = odds[0] + oddsHome
                #maxOdd = session.query(func.max(Odds.oddsHome)).filter(Odds.matchId == c.id)
                #print (match, maxOdd)

            elif (match.goalsHome < match.goalsAway):
                results[2] = results[2] + 1
                odds[2] = odds[2] + oddsAway
            else:
                results[1] = results[1] + 1
                odds[1] = odds[1] + oddsDraw

        profits[0]=odds[0] - games
        profits[1]=odds[1] - games
        profits[2]=odds[2] - games

        table.append([c.name, \
                      games, \
                      results[0], results[1], results[2], \
                      util.replaceDotToComman(round(results[0] / 3.8, 2)), \
                      util.replaceDotToComman(round(results[1] / 3.8, 2)), \
                      util.replaceDotToComman(round(results[2] / 3.8, 2)), \
                      util.replaceDotToComman(odds[0]), util.replaceDotToComman(odds[1]), util.replaceDotToComman(odds[2]), \
                      util.replaceDotToComman(profits[0]), util.replaceDotToComman(profits[1]), util.replaceDotToComman(profits[2])
                      ])

    print(tabulate(table, headers=["Championship","Matches","Home","Draw","Away",\
                                   "Home(%)","Draw(%)", "Away(%)",\
                                   "Odds Home","Odds Draw","Odds Away",\
                                   "Profit Home","Profit Draw","Profit Away"
                                   ]))

def simpleHomeDrawAwayMaxOdds():

    championships = session.query(Championship)
    table = []

    for c in championships:

        matches = session.query(Match).filter(Match.championshipId == c.id)

        profits = [0,0,0]
        results = [0,0,0]
        odds = [Decimal(0),Decimal(0),Decimal(0)]

        games = 0
        for match in matches:
            try:
                maxOdds = ResumeOdds.get(match.id)
                if (match.oddsHome is None):
                    oddsHome = 0
                else:
                    games = games + 1
                    oddsHome = maxOdds.maxHome

                if (match.oddsHome is None):
                    oddsAway = 0
                else:
                    oddsAway = maxOdds.maxAway

                if (match.oddsDraw is None):
                    oddsDraw = 0
                else:
                    oddsDraw = maxOdds.maxDraw
            except:
                oddsHome = 0
                oddsAway = 0
                oddsDraw = 0

            #Quantidade de jogos | apostas casa/local/visitante
            if (match.goalsHome > match.goalsAway):
                results[0] = results[0] + 1
                odds[0] = odds[0] + oddsHome
                #maxOdd = session.query(func.max(Odds.oddsHome)).filter(Odds.matchId == c.id)
                #print (match, maxOdd)

            elif (match.goalsHome < match.goalsAway):
                results[2] = results[2] + 1
                odds[2] = odds[2] + oddsAway
            else:
                results[1] = results[1] + 1
                odds[1] = odds[1] + oddsDraw

        profits[0]=odds[0] - games
        profits[1]=odds[1] - games
        profits[2]=odds[2] - games

        table.append([c.name, \
                      games, \
                      results[0], results[1], results[2], \
                      util.replaceDotToComman(round(results[0] / 3.8, 2)), \
                      util.replaceDotToComman(round(results[1] / 3.8, 2)), \
                      util.replaceDotToComman(round(results[2] / 3.8, 2)), \
                      util.replaceDotToComman(odds[0]), util.replaceDotToComman(odds[1]), util.replaceDotToComman(odds[2]), \
                      util.replaceDotToComman(profits[0]), util.replaceDotToComman(profits[1]), util.replaceDotToComman(profits[2])
                      ])

    print(tabulate(table, headers=["Championship","Matches","Home","Draw","Away",\
                                   "Home(%)","Draw(%)", "Away(%)",\
                                   "Odds Home","Odds Draw","Odds Away",\
                                   "Profit Home","Profit Draw","Profit Away"
                                   ]))

def matchHomeDrawAway(type):

    championships = session.query(Championship).filter()
    table = []

    for c in championships:

        matches = session.query(Match).filter(Match.championshipId == c.id)

        games = 0
        results = [0,0,0]
        profits = [0,0,0]
        odds = [Decimal(0),Decimal(0),Decimal(0)]

        if (type == util.ODD_AVG):

            for match in matches:

                try:
                    #matchOdds = ResumeOdds.get(match.id)
                    oddsHome = match.oddsHome
                    oddsDraw = match.oddsDraw
                    oddsAway = match.oddsAway

                    if (match.result == 0):
                        results[0] = results[0] + 1
                        odds[0] = odds[0] + oddsHome
                    elif (match.result == 1):
                        results[1] = results[1] + 1
                        odds[1] = odds[1] + oddsDraw
                    else:
                        results[2] = results[2] + 1
                        odds[2] = odds[2] + oddsAway
                    games = games + 1
                except:
                    pass
        else:

            for match in matches:

                try:
                    matchOdds = ResumeOdds.get(match.id)
                    oddsHome = matchOdds.maxHome
                    oddsDraw = matchOdds.maxDraw
                    oddsAway = matchOdds.maxAway

                    if (match.result == 0):
                        results[0] = results[0] + 1
                        odds[0] = odds[0] + oddsHome
                    elif (match.result == 1):
                        results[1] = results[1] + 1
                        odds[1] = odds[1] + oddsDraw
                    else:
                        results[2] = results[2] + 1
                        odds[2] = odds[2] + oddsAway
                    games = games + 1
                except:
                    pass

        profits[0]=odds[0] - games
        profits[1]=odds[1] - games
        profits[2]=odds[2] - games

        table.append([c.name, \
                      games, \
                      results[0], results[1], results[2], \
                      util.replaceDotToComman(round(results[0] / 3.8, 2)), \
                      util.replaceDotToComman(round(results[1] / 3.8, 2)), \
                      util.replaceDotToComman(round(results[2] / 3.8, 2)), \
                      util.replaceDotToComman(odds[0]), util.replaceDotToComman(odds[1]), util.replaceDotToComman(odds[2]), \
                      util.replaceDotToComman(profits[0]), util.replaceDotToComman(profits[1]), util.replaceDotToComman(profits[2])
                      ])

    print(tabulate(table, headers=["Championship","Matches","Home","Draw","Away",\
                                   "Home(%)","Draw(%)", "Away(%)",\
                                   "Odds Home","Odds Draw","Odds Away",\
                                   "Profit Home","Profit Draw","Profit Away"
                                   ]))

def matchFavoriteMediumUnderdog(type):

    championships = session.query(Championship).filter()
    table = []

    for c in championships:

        matches = session.query(Match).filter(Match.championshipId == c.id)

        games = 0
        results = [0,0,0]
        profits = [0,0,0]
        odds = [Decimal(0),Decimal(0),Decimal(0)]

        for match in matches:

            if (type == 'max'):
                try:
                    maxOdds = ResumeOdds.get(match.id)
                    if (match.oddsHome is None):
                        oddsHome = 0
                    else:
                        games = games + 1
                        oddsHome = maxOdds.maxHome

                    if (match.oddsHome is None):
                        oddsAway = 0
                    else:
                        oddsAway = maxOdds.maxAway

                    if (match.oddsDraw is None):
                        oddsDraw = 0
                    else:
                        oddsDraw = maxOdds.maxDraw
                except:
                    oddsHome = 0
                    oddsAway = 0
                    oddsDraw = 0
            else:
                if (match.oddsHome is None):
                    oddsHome = 0
                else:
                    games = games + 1
                    oddsHome = match.oddsHome

                if (match.oddsAway is None):
                    oddsAway = 0
                else:
                    oddsAway = match.oddsAway

                if (match.oddsDraw is None):
                    oddsDraw = 0
                else:
                    oddsDraw = match.oddsDraw

            oddsMatch = [oddsHome,oddsDraw,oddsAway]

            #Apostas favorito/azarao
            if (match.oddsHome is not None):

                oddsFavorite = min(oddsMatch)
                oddsMedium = statistics.median(oddsMatch)
                oddsUnderdog = max(oddsMatch)

                favorite = oddsMatch.index(oddsFavorite)
                medium = oddsMatch.index(oddsMedium)
                underdog = oddsMatch.index(oddsUnderdog)

                if (match.goalsHome > match.goalsAway):
                    result = 0
                elif (match.goalsAway > match.goalsHome):
                    result = 2
                else:
                    result = 1

                if (result == favorite):
                    results[0] = results[0] + 1
                    odds[0] = odds[0] + oddsFavorite
                elif (result == medium):
                    results[1] = results[1] + 1
                    odds[1] = odds[1] + oddsMedium
                else:
                    results[2] = results[2] + 1
                    odds[2] = odds[2] + oddsUnderdog

        profits[0]=odds[0] - games
        profits[1]=odds[1] - games
        profits[2]=odds[2] - games

        table.append([c.name, \
                      games, \
                      results[0], results[1], results[2], \
                      util.replaceDotToComman(round(results[0] / 3.8, 2)), \
                      util.replaceDotToComman(round(results[1] / 3.8, 2)), \
                      util.replaceDotToComman(round(results[2] / 3.8, 2)), \
                      util.replaceDotToComman(odds[0]), util.replaceDotToComman(odds[1]), util.replaceDotToComman(odds[2]), \
                      util.replaceDotToComman(profits[0]), util.replaceDotToComman(profits[1]), util.replaceDotToComman(profits[2])
                      ])

    print(tabulate(table, headers=["Championship","Matches","Favorite","Medium","Underdog",\
                                   "Favorite(%)","Medium(%)", "Underdog(%)",\
                                   "Odds Favorite","Odds Medium","Odds Underdog",\
                                   "Profit Favorite","Profit Medium","Profit Underdog"
                                   ]))

def bothTeamScoreYesNo(type):

    championships = session.query(Championship).filter()
    table = []

    for c in championships:

        matches = c.listMatches()

        games = 0
        results = [0,0]
        profits = [0,0]
        odds = [Decimal(0),Decimal(0)]

        if (type == util.ODD_AVG):

            for match in matches:

                try:
                    btsOdds = ResumeOddsBTS.get(match.id)
                    oddsYes = btsOdds.avgYes
                    oddsNo = btsOdds.avgNo

                    if (match.goalsHome > 0 and match.goalsAway > 0):
                        results[0] = results[0] + 1
                        odds[0] = odds[0] + oddsYes
                    else:
                        results[1] = results[1] + 1
                        odds[1] = odds[1] + oddsNo
                    games = games + 1

                except:
                    pass

        else:

            for match in matches:

                try:
                    btsOdds = ResumeOddsBTS.get(match.id)
                    oddsYes = btsOdds.maxYes
                    oddsNo = btsOdds.maxNo

                    if (match.goalsHome > 0 and match.goalsAway > 0):
                        results[0] = results[0] + 1
                        odds[0] = odds[0] + oddsYes
                    else:
                        results[1] = results[1] + 1
                        odds[1] = odds[1] + oddsNo
                    games = games + 1

                except:
                    pass

        profits[0]=odds[0] - games
        profits[1]=odds[1] - games
        percents = [0,0]
        if (games == 0):
            percents[0] = 0
            percents[1] = 0
        else:
            percents[0] = util.replaceDotToComman(round(results[0] / (games/100), 2))
            percents[1] = util.replaceDotToComman(round(results[1] / (games/100), 2))
        table.append([c.name, \
                  games, \
                  results[0], results[1],\
                  percents[0], percents[1],\
                  util.replaceDotToComman(odds[0]), util.replaceDotToComman(odds[1]),\
                  util.replaceDotToComman(profits[0]), util.replaceDotToComman(profits[1])
                  ])


    print(tabulate(table, headers=["Championship","Matches","Yes","No",\
                                   "Yes(%)","No(%)",\
                                   "Odds Yes","Odds No",\
                                   "Profit Yes","Profit No",
                                   ]))

def bothTeamScoreFavoriteUnderdog(type):

    championships = session.query(Championship).filter()
    table = []

    for c in championships:

        matches = c.listMatches()

        games = 0
        results = [0,0]
        profits = [0,0]
        odds = [Decimal(0),Decimal(0)]

        if (type == util.ODD_AVG):

            for match in matches:

                try:
                    btsOdds = ResumeOddsBTS.get(match.id)
                    oddsYes = btsOdds.avgYes
                    oddsNo = btsOdds.avgNo

                    if (match.goalsHome > 0 and match.goalsAway > 0):
                        if (oddsYes > oddsNo):
                            results[0] = results[0] + 1
                            odds[0] = odds[0] + oddsYes
                        else:
                            results[1] = results[1] + 1
                            odds[1] = odds[1] + oddsNo
                    else:
                        if (oddsNo > oddsYes):
                            results[0] = results[0] + 1
                            odds[0] = odds[0] + oddsYes
                        else:
                            results[1] = results[1] + 1
                            odds[1] = odds[1] + oddsNo
                    games = games + 1

                except:
                    pass

        else:

            for match in matches:

                try:
                    btsOdds = ResumeOddsBTS.get(match.id)
                    oddsYes = btsOdds.maxYes
                    oddsNo = btsOdds.maxNo

                    if (match.goalsHome > 0 and match.goalsAway > 0):
                        if (oddsYes > oddsNo):
                            results[0] = results[0] + 1
                            odds[0] = odds[0] + oddsYes
                        else:
                            results[1] = results[1] + 1
                            odds[1] = odds[1] + oddsNo
                    else:
                        if (oddsNo > oddsYes):
                            results[0] = results[0] + 1
                            odds[0] = odds[0] + oddsYes
                        else:
                            results[1] = results[1] + 1
                            odds[1] = odds[1] + oddsNo
                    games = games + 1

                except:
                    pass

        profits[0]=odds[0] - games
        profits[1]=odds[1] - games
        percents = [0,0]
        if (games == 0):
            percents[0] = 0
            percents[1] = 0
        else:
            percents[0] = util.replaceDotToComman(round(results[0] / (games/100), 2))
            percents[1] = util.replaceDotToComman(round(results[1] / (games/100), 2))
        table.append([c.name, \
                  games, \
                  results[0], results[1],\
                  percents[0], percents[1],\
                  util.replaceDotToComman(odds[0]), util.replaceDotToComman(odds[1]),\
                  util.replaceDotToComman(profits[0]), util.replaceDotToComman(profits[1])
                  ])


    print(tabulate(table, headers=["Championship","Matches","Yes","No",\
                                   "Favorite(%)","Underdog(%)",\
                                   "Odds Favorite","Odds Underdog",\
                                   "Profit Favorite","Profit Underdog",
                                   ]))

def drawNoBetHomeAway(type):

    championships = session.query(Championship).filter()
    table = []

    for c in championships:

        matches = c.listMatches()

        games = 0
        draws = 0
        results = [0,0]
        profits = [0,0]
        odds = [Decimal(0),Decimal(0)]

        if (type == util.ODD_AVG):

            for match in matches:

                try:
                    dnbOdds = ResumeOddsDNB.get(match.id)
                    oddsHome = dnbOdds.avgHome
                    oddsAway = dnbOdds.avgAway

                    if (match.result == 0):
                        results[0] = results[0] + 1
                        odds[0] = odds[0] + oddsHome
                        games = games + 1
                    elif (match.result == 2):
                        results[1] = results[1] + 1
                        odds[1] = odds[1] + oddsAway
                        games = games + 1
                    else:
                        draws = draws + 1


                except:
                    pass

        else:

            for match in matches:

                try:
                    dnbOdds = ResumeOddsDNB.get(match.id)
                    oddsHome = dnbOdds.maxHome
                    oddsAway = dnbOdds.maxAway

                    if (match.result == 0):
                        results[0] = results[0] + 1
                        odds[0] = odds[0] + oddsHome
                        games = games + 1
                    elif (match.result == 2):
                        results[1] = results[1] + 1
                        odds[1] = odds[1] + oddsAway
                        games = games + 1
                    else:
                        draws = draws + 1


                except:
                    pass

        profits[0]=odds[0] - games
        profits[1]=odds[1] - games
        percents = [0,0]
        if (games == 0):
            percents[0] = 0
            percents[1] = 0
        else:
            percents[0] = util.replaceDotToComman(round(results[0] / (games/100), 2))
            percents[1] = util.replaceDotToComman(round(results[1] / (games/100), 2))
        table.append([c.name, \
                  games, \
                  results[0], results[1],\
                  percents[0], percents[1],\
                  util.replaceDotToComman(odds[0]), util.replaceDotToComman(odds[1]),\
                  util.replaceDotToComman(profits[0]), util.replaceDotToComman(profits[1])
                  ])


    print(tabulate(table, headers=["CHAMP","MATCHES","HOM","AWA",\
                                   "HOM(%)","AWA(%)",\
                                   "ODDS HOM","ODDS AWA",\
                                   "PROFIT HOM","PROFIT AWA",
                                   ]))

def drawNoBetFavoriteUnderdog(type):

    championships = session.query(Championship).filter()
    table = []

    for c in championships:

        matches = c.listMatches()

        games = 0
        draws = 0
        results = [0,0]
        profits = [0,0]
        odds = [Decimal(0),Decimal(0)]

        if (type == util.ODD_AVG):

            for match in matches:

                try:
                    dnbOdds = ResumeOddsDNB.get(match.id)
                    oddsHome = dnbOdds.avgHome
                    oddsAway = dnbOdds.avgAway

                    if (match.result == 0):
                        results[0] = results[0] + 1
                        odds[0] = odds[0] + oddsHome
                        games = games + 1
                    elif (match.result == 2):
                        results[1] = results[1] + 1
                        odds[1] = odds[1] + oddsAway
                        games = games + 1
                    else:
                        draws = draws + 1


                except:
                    pass

        else:

            for match in matches:

                try:
                    dnbOdds = ResumeOddsDNB.get(match.id)
                    oddsHome = dnbOdds.maxHome
                    oddsAway = dnbOdds.maxAway

                    if (match.result == 0):
                        if (oddsHome < oddsAway):
                            results[0] = results[0] + 1
                            odds[0] = odds[0] + oddsHome
                        else:
                            results[1] = results[1] + 1
                            odds[1] = odds[1] + oddsAway
                        games = games + 1
                    elif (match.result == 2):
                        if (oddsAway < oddsHome):
                            results[0] = results[0] + 1
                            odds[0] = odds[0] + oddsHome
                        else:
                            results[1] = results[1] + 1
                            odds[1] = odds[1] + oddsAway
                        games = games + 1
                    else:
                        draws = draws + 1
                except:
                    pass

        profits[0]=odds[0] - games
        profits[1]=odds[1] - games
        percents = [0,0]
        if (games == 0):
            percents[0] = 0
            percents[1] = 0
        else:
            percents[0] = util.replaceDotToComman(round(results[0] / (games/100), 2))
            percents[1] = util.replaceDotToComman(round(results[1] / (games/100), 2))
        table.append([c.name, \
                  games, \
                  results[0], results[1],\
                  percents[0], percents[1],\
                  util.replaceDotToComman(odds[0]), util.replaceDotToComman(odds[1]),\
                  util.replaceDotToComman(profits[0]), util.replaceDotToComman(profits[1])
                  ])


    print(tabulate(table, headers=["CHAMP","MATCH","FAVO","UNDO",\
                                   "FAVO(%)","UNDO(%)",\
                                   "ODDS FAVO","ODDS UNDO",\
                                   "PROFIT FAVO","PROFIT UNDO",
                                   ]))

def doubleChanceHomeDrawAway(type):

    championships = session.query(Championship).filter()
    table = []

    for c in championships:

        matches = session.query(Match).filter(Match.championshipId == c.id)

        games = 0
        results = [0,0,0]
        profits = [0,0,0]
        odds = [Decimal(0),Decimal(0),Decimal(0)]

        if (type == util.ODD_AVG):

            for match in matches:

                try:
                    matchOdds = ResumeOddsDC.get(match.id)
                    oddsHomeDraw = matchOdds.avgHomeDraw
                    oddsHomeAway = matchOdds.avgHomeAway
                    oddsAwayDraw = matchOdds.avgAwayDraw

                    if (oddsHomeDraw is None):
                        oddsHomeDraw = 0

                    if (oddsHomeAway is None):
                        oddsHomeAway = 0

                    if (oddsAwayDraw is None):
                        oddsAwayDraw = 0

                    if (match.result == 0):
                        results[0] = results[0] + 1
                        results[1] = results[1] + 1
                        odds[0] = odds[0] + oddsHomeDraw
                        odds[1] = odds[1] + oddsHomeAway
                    elif (match.result == 1):
                        results[0] = results[0] + 1
                        results[2] = results[2] + 1
                        odds[0] = odds[0] + oddsHomeDraw
                        odds[2] = odds[2] + oddsAwayDraw
                    else:
                        results[1] = results[1] + 1
                        results[2] = results[2] + 1
                        odds[1] = odds[1] + oddsHomeAway
                        odds[2] = odds[2] + oddsAwayDraw
                    games = games + 1
                except:
                    pass



        else:

            for match in matches:

                try:
                    matchOdds = ResumeOddsDC.get(match.id)
                    oddsHomeDraw = matchOdds.maxHomeDraw
                    oddsHomeAway = matchOdds.maxHomeAway
                    oddsAwayDraw = matchOdds.maxAwayDraw

                    if (match.result == 0):
                        results[0] = results[0] + 1
                        results[1] = results[1] + 1
                        odds[0] = odds[0] + oddsHomeDraw
                        odds[1] = odds[1] + oddsHomeAway
                    elif (match.result == 1):
                        results[0] = results[0] + 1
                        results[2] = results[2] + 1
                        odds[0] = odds[0] + oddsHomeDraw
                        odds[2] = odds[2] + oddsAwayDraw
                    else:
                        results[1] = results[1] + 1
                        results[2] = results[2] + 1
                        odds[1] = odds[1] + oddsHomeAway
                        odds[2] = odds[2] + oddsAwayDraw
                    games = games + 1
                except:
                    pass

        profits[0]=odds[0] - games
        profits[1]=odds[1] - games
        profits[2]=odds[2] - games

        table.append([c.name, \
                      games, \
                      results[0], results[1], results[2], \
                      util.replaceDotToComman(round(results[0] / 3.8, 2)), \
                      util.replaceDotToComman(round(results[1] / 3.8, 2)), \
                      util.replaceDotToComman(round(results[2] / 3.8, 2)), \
                      util.replaceDotToComman(odds[0]), util.replaceDotToComman(odds[1]), util.replaceDotToComman(odds[2]), \
                      util.replaceDotToComman(profits[0]), util.replaceDotToComman(profits[1]), util.replaceDotToComman(profits[2])
                      ])

    print(tabulate(table, headers=["Championship","Matches","HomeDraw","HomeAway","AwayDraw",\
                                   "HomeDraw(%)","HomeAway(%)", "AwayDraw(%)",\
                                   "Odds HomeDraw","Odds HomeAway","Odds AwayDraw",\
                                   "Profit HomeDraw","Profit HomeAway","Profit AwayDraw"
                                   ]))

def lastMatches(type):

    championships = session.query(Championship).filter()
    table = []
    table2 = []

    for c in championships:

        matches = c.listMatches()
        hits = [0]*38
        evaluates = [0]*38
        oddsExists = [0]*38
        odds = [0]*38
        profit = [0]*38

        for m in matches:

            bets = session.query(Bet).filter(Bet.matchId == m.id, Bet.local == 0)

            for b in bets:
                evaluates[b.lastMatchesNum] = evaluates[b.lastMatchesNum] + 1
                if (b.hit == 1):
                    hits[b.lastMatchesNum] = hits[b.lastMatchesNum] + 1

                if (type == util.ODD_AVG):
                    oddsHome = m.oddsHome
                    oddsDraw = m.oddsAway
                    oddsAway = m.oddsAway
                else:
                    try:
                        matchOdds = ResumeOdds.get(m.id)
                        oddsHome = matchOdds.maxHome
                        oddsDraw = matchOdds.maxDraw
                        oddsAway = matchOdds.maxAway
                    except:
                        oddsHome = None
                        oddsDraw = None
                        oddsAway = None

                if (oddsHome is not None and oddsDraw is not None and oddsAway is not None):
                    oddsExists[b.lastMatchesNum] = oddsExists[b.lastMatchesNum] + 1

                    if (b.hit == 1):
                        if (b.betColumn == 0):
                            odds[b.lastMatchesNum] = odds[b.lastMatchesNum] + oddsHome
                        elif (b.betColumn == 1):
                            odds[b.lastMatchesNum] = odds[b.lastMatchesNum] + oddsDraw
                        else:
                            odds[b.lastMatchesNum] = odds[b.lastMatchesNum] + oddsAway

        accuracy = [0]*38
        for i,h in enumerate(hits):
            try:
                accuracy[i] = round(h/evaluates[i],2)
            except:
                accuracy[i] = 0

        for i,h in enumerate(evaluates):
            try:
                profit[i] = odds[i] - oddsExists[i]
            except:
                profit[i] = 0


        table.append(accuracy)
        table2.append(profit)

    print (tabulate(table))
    print (tabulate(table2))

def lastMatchesLocal(type):

    championships = session.query(Championship).filter()
    table = []
    table2 = []

    for c in championships:

        matches = c.listMatches()
        hits = [0]*38
        evaluates = [0]*38
        oddsExists = [0]*38
        odds = [0]*38
        profit = [0]*38

        for m in matches:

            bets = session.query(Bet).filter(Bet.matchId == m.id, Bet.local == 1)

            for b in bets:
                evaluates[b.lastMatchesNum] = evaluates[b.lastMatchesNum] + 1

                if (b.hit == 1):
                    hits[b.lastMatchesNum] = hits[b.lastMatchesNum] + 1

                if (type == util.ODD_AVG):
                    oddsHome = m.oddsHome
                    oddsDraw = m.oddsAway
                    oddsAway = m.oddsAway
                else:
                    try:
                        matchOdds = ResumeOdds.get(m.id)
                        oddsHome = matchOdds.maxHome
                        oddsDraw = matchOdds.maxDraw
                        oddsAway = matchOdds.maxAway
                    except:
                        oddsHome = None
                        oddsDraw = None
                        oddsAway = None

                if (oddsHome is not None and oddsDraw is not None and oddsAway is not None):
                    oddsExists[b.lastMatchesNum] = oddsExists[b.lastMatchesNum] + 1

                    if (b.hit == 1):
                        if (b.betColumn == 0):
                            odds[b.lastMatchesNum] = odds[b.lastMatchesNum] + oddsHome
                        elif (b.betColumn == 1):
                            odds[b.lastMatchesNum] = odds[b.lastMatchesNum] + oddsDraw
                        else:
                            odds[b.lastMatchesNum] = odds[b.lastMatchesNum] + oddsAway



        accuracy = [0]*38
        for i,h in enumerate(hits):
            try:
                accuracy[i] = round(h/evaluates[i],2)
            except:
                accuracy[i] = 0

        for i,h in enumerate(evaluates):
            try:
                profit[i] = odds[i] - oddsExists[i]
            except:
                profit[i] = 0


        table.append(accuracy)
        table2.append(profit)

    print (tabulate(table))
    print (tabulate(table2))


def evaluateOdds():

    matches = Match().list()

    for m in matches:

        oddsHome = m.oddsHome
        oddsDraw = m.oddsDraw
        oddsAway = m.oddsAway

        if (oddsHome is not None and oddsDraw is not None and oddsAway is not None):

            oddsHome = 100/oddsHome
            oddsDraw = 100/oddsDraw
            oddsAway = 100/oddsAway

            if (oddsHome+oddsDraw+oddsAway < 98):
                print(oddsHome,oddsDraw,oddsAway)
                print(oddsHome+oddsDraw+oddsAway)
                print (m)

evaluateOdds()
#lastMatches()

#bothTeamScore('avg')
#bothTeamScoreYesNo('avg')
#bothTeamScoreYesNo('max')
#drawNoBetHomeAway('avg')
#drawNoBetHomeAway('max')
#drawNoBetFavoriteUnderdog('avg')
#drawNoBetFavoriteUnderdog('max')
#bothTeamScoreFavoriteUnderdog('avg')
#bothTeamScoreFavoriteUnderdog('max')
#simpleFavoriteMediumUnderdog('avg')
#simpleFavoriteMediumUnderdog('max')
#simpleHomeDrawAway()
#simpleFavoriteMediumUnderdog()

#doubleChanceHomeDrawAway('avg')
#doubleChanceHomeDrawAway('max')
#lastMatches('avg')
#lastMatchesLocal('avg')