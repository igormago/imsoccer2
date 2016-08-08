import matplotlib.pyplot as plt
from betExplorer.models import *
from pylab import xticks, yticks
import numpy as np

matches = Match().list()
goals = []
goalsHome = []
goalsAway = []
qtGoals = ('0','1','2','3','4','5','6','7','8','9','10')

for m in matches:
    goals.append(m.goalsHome + m.goalsAway)
    goalsHome.append(m.goalsHome)
    goalsAway.append(m.goalsAway)
    xy = [m.goalsHome,goalsAway]


def histograms():
    plt.hist(goals,bins=10)
    xticks(np.arange(11)+0.5,qtGoals)
    yticks(np.arange(0,2000,200))
    plt.show()

    plt.hist(goalsHome,bins=10)
    xticks(np.arange(11)+0.5,qtGoals)
    yticks(np.arange(0,3000,200))
    plt.show()

histograms()