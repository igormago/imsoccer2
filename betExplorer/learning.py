from sklearn.ensemble import RandomForestClassifier

from betExplorer.models import *

matches = Championship().get('serie-a-2015').listMatches()
matches = Match.list(Match)

train = []
target = []
test = []
target2 = []
realResult = []
realResult2 = []

total_games = 4000
for i,m in enumerate(matches):
    if (i < total_games):
        train.append([m.homeTeamId,m.awayTeamId])
        target.append([m.goalsHome,m.goalsAway])
        target2.append([m.result])
    else:
        test.append([m.homeTeamId,m.awayTeamId])
        realResult.append([m.goalsHome,m.goalsAway])
        realResult2.append([m.result])

est = RandomForestClassifier(n_estimators = 1000)
est.fit(train,target)
x = est.predict(test)

score = 0
for z in range(0,3600):
    if (x[z][0] > x[z][1] and realResult[z][0] > realResult[z][1]):
        score = score + 1
    elif (x[z][0] == x[z][1] and realResult[z][0] == realResult[z][1]):
        score = score + 1
    elif (x[z][0] < x[z][1] and realResult[z][0]< realResult[z][1]):
        score = score + 1
print(score/3600)

print(target2)
est2 = RandomForestClassifier(n_estimators = 1000)
est2.fit(train,target2)
x = est.predict(test)

score = 0
for z in range(0,3600):
    if (x[z][0] == realResult2[z][0]):
        score = score + 1

print(score/3600)