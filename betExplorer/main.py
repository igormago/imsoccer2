from betExplorer import services
import time

def main():
    ini = time.time()
    #services.crawlerChampionshipFiles()
    #services.scrapChampionshipFiles()
    #services.crawlerMatchFiles()
    #services.betRelativeLastMatches()
    #services.betRelativeLastMatchesLocal()
    #services.extractRankingPerMatch()
    #services.extractRankingRelativeLastMatches()
    #services.confirmBet()
    #services.updateMatchResults()
    #services.updateMatchResults()
    fim = time.time()

    print((fim-ini)/60)

if __name__ == "__main__":
    main()