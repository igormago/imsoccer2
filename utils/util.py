
PROJECT_PATH = "/home/igormago/PycharmProjects/doutorado"
FILES_PATH = PROJECT_PATH + "/files"
BETEXPLORER_FILES = FILES_PATH + "/betExplorer"
URL_BETEXPLORER="http://www.betexplorer.com/soccer/brazil/"

TYPE_1x2 = '1x2'
TYPE_OU = 'ou'
TYPE_AH = 'ah'
TYPE_DNB = 'ha'
TYPE_DC = 'dc'
TYPE_BTS = 'bts'

ODD_AVG = 'avg'
ODD_MAX = 'max'
ODD_MIN = 'min'

ODDS_TYPES = {TYPE_1x2, TYPE_OU, TYPE_AH, TYPE_DNB, TYPE_DC, TYPE_BTS}

def replaceDotToComman(odd):
    return str(odd).replace('.',',')

def result(match):

    if (match.goalsHome > match.goalsAway):
        return 0
    elif (match.goalsHome < match.goalsAway):
        return 2
    else:
        return 1
