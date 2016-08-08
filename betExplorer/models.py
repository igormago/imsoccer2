from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

engine = create_engine('mysql+mysqlconnector://root:root@localhost/betexplorer2')
Session = sessionmaker(bind=engine)
session = Session()

class ModelMixin(object):

    def save(self):
        session.add(self)

    def __init__(self,*args,**kwargs):
        pass

class Championship(Base):
    __tablename__ = 'championships'

    id = Column("championship_id",Integer, primary_key=True, autoincrement=True)
    name = Column("championship_name",String(100))
    year = Column(Integer)

    def __repr__(self):
        r = "Championship: ", self.id, self.name, self.year
        return (str(r))

    def get (self, championshipName):
        return session.query(Championship).filter(Championship.name == championshipName).one()

    def list (self):
        return session.query(Championship).filter().all()

    def listMatches (self):
        return session.query(Match).filter(Match.championshipId == self.id).order_by(Match.matchDate).all()

class Team(Base):
    __tablename__ = 'teams'

    id = Column ('team_id',Integer, primary_key=True, autoincrement=True )
    name = Column('team_name',String(45))

    def __repr__(self):
        r = "Team: ", self.id, self.name
        return (str(r))

    def get(self,teamName):
        return session.query(Team).filter(Team.name == teamName).one()

class Match(Base,ModelMixin):

    __tablename__ = 'matches'

    id = Column("match_id",String(45), primary_key=True)
    championshipId = Column("championship_id",Integer, ForeignKey('championships.championship_id'))
    homeTeamId = Column("home_team_id", Integer, ForeignKey('teams.team_id'))
    awayTeamId = Column("away_team_id", Integer,ForeignKey('teams.team_id'))
    goalsHome = Column("goals_home", Integer)
    goalsAway = Column("goals_away", Integer)
    result = Column("column_result",Integer)
    matchDate = Column("match_date",Date)
    round = Column("round_num",Integer)
    oddsHome = Column("odds_home",Numeric)
    oddsDraw = Column("odds_draw",Numeric)
    oddsAway = Column("odds_away",Numeric)

    def __repr__(self):
        return "ID: " + self.id  + ": " + str(self.homeTeamId) +\
        "(" + str(self.goalsHome) + ") x (" + str(self.goalsAway) + ")" + str(self.awayTeamId)

    def get (matchId):
        return session.query(Match).filter(Match.id==matchId).one()

    def list (self):
        return session.query(Match).filter().all()

class Bookmaker(Base,ModelMixin):

    __tablename__ = 'bookmakers'

    id = Column("bookmaker_id",Integer, primary_key=True, autoincrement=True)
    name = Column("bookmaker_name",String(45), unique=True)

    def __repr__(self):
        return "ID: " + str(self.id) + ",NAME: " + self.name

    def get (bookmakerName):
        return session.query(Bookmaker).filter(Bookmaker.name == bookmakerName).one()

    def list (self):
        return session.query(Bookmaker).filter().all()

class Odds(Base,ModelMixin):

    __tablename__ = 'odds'

    matchId = Column("match_id",String(45), ForeignKey('matches.match_id'), primary_key=True)
    bookmakerId = Column("bookmaker_id",Integer, ForeignKey('bookmakers.bookmaker_id'), primary_key=True)
    oddsHome = Column("odds_home",Numeric)
    oddsDraw = Column("odds_draw",Numeric)
    oddsAway = Column("odds_away",Numeric)

    def get (matchId, bookmakerId):
        return session.query(Odds).filter(Odds.matchId==matchId,Odds.bookmakerId==bookmakerId).one()

    def list(matchId):
         return session.query(Odds).filter(Odds.matchId==matchId).all()

class OddsOU(Base,ModelMixin):

    __tablename__ = 'odds_OU'

    matchId = Column("match_id",String(45), ForeignKey('matches.match_id'), primary_key=True)
    bookmakerId = Column("bookmaker_id",Integer, ForeignKey('bookmakers.bookmaker_id'), primary_key=True)
    goals = Column("goals_num",Numeric,primary_key=True)
    oddsOver = Column("odds_over",Numeric)
    oddsUnder = Column("odds_under",Numeric)

    def get (matchId, bookmakerId, goals):
        return session.query(OddsOU).filter(OddsOU.matchId==matchId,OddsOU.bookmakerId==bookmakerId,\
                                            OddsOU.goals==goals).one()

    def list(matchId):
         return session.query(OddsOU).filter(OddsOU.matchId==matchId).all()

class OddsAH(Base,ModelMixin):

    __tablename__ = 'odds_AH'

    matchId = Column("match_id",String(45), ForeignKey('matches.match_id'), primary_key=True)
    bookmakerId = Column("bookmaker_id",Integer, ForeignKey('bookmakers.bookmaker_id'), primary_key=True)
    handicap = Column("handicap",String(45), primary_key=True)
    oddsHome = Column("odds_home",Numeric)
    oddsAway = Column("odds_away",Numeric)

    def get (matchId, bookmakerId, handicap):
        return session.query(OddsAH).filter(OddsAH.matchId==matchId,OddsAH.bookmakerId==bookmakerId,\
                                            OddsAH.handicap==handicap).one()

    def list(matchId):
         return session.query(OddsAH).filter(OddsAH.matchId==matchId).all()

class OddsDC(Base,ModelMixin):

    __tablename__ = 'odds_DC'

    matchId = Column("match_id",String(45), ForeignKey('matches.match_id'), primary_key=True)
    bookmakerId = Column("bookmaker_id",Integer, ForeignKey('bookmakers.bookmaker_id'), primary_key=True)
    oddsHomeDraw = Column("odds_home_draw",Numeric)
    oddsHomeAway = Column("odds_home_away",Numeric)
    oddsAwayDraw = Column("odds_away_draw",Numeric)

    def get (matchId, bookmakerId):
        return session.query(OddsDC).filter(OddsDC.matchId==matchId,OddsDC.bookmakerId==bookmakerId).one()

    def list(matchId):
         return session.query(OddsDC).filter(OddsDC.matchId==matchId).all()

class OddsDNB(Base,ModelMixin):

    __tablename__ = 'odds_DNB'

    matchId = Column("match_id",String(45), ForeignKey('matches.match_id'), primary_key=True)
    bookmakerId = Column("bookmaker_id",Integer, ForeignKey('bookmakers.bookmaker_id'), primary_key=True)
    oddsHome = Column("odds_home",Numeric)
    oddsAway = Column("odds_away",Numeric)

    def get (matchId, bookmakerId):
        return session.query(OddsDNB).filter(OddsDNB.matchId==matchId,OddsDNB.bookmakerId==bookmakerId).one()

    def list(matchId):
         return session.query(OddsDNB).filter(OddsDNB.matchId==matchId).all()

class OddsBTS(Base,ModelMixin):

    __tablename__ = 'odds_BTS'

    matchId = Column("match_id",String(45), ForeignKey('matches.match_id'), primary_key=True)
    bookmakerId = Column("bookmaker_id",Integer, ForeignKey('bookmakers.bookmaker_id'), primary_key=True)
    oddsYes = Column("odds_yes",Numeric)
    oddsNo = Column("odds_no",Numeric)

    def get (matchId, bookmakerId):
        return session.query(OddsBTS).filter(OddsBTS.matchId==matchId,OddsBTS.bookmakerId==bookmakerId).one()

    def list(matchId):
         return session.query(OddsBTS).filter(OddsBTS.matchId==matchId).all()

class Ranking(Base):

    __tablename__ = 'ranking'
    matchId = Column("match_id",String(45),ForeignKey('matches.match_id'),primary_key=True)
    teamId = Column("team_id",Integer,ForeignKey('teams.team_id'),primary_key=True)
    local = Column("local",String(1),primary_key=True)
    matchesPlayed = Column("matches_played",Integer,primary_key=True)
    lastMatchesNum = Column("last_matches_num",Integer,primary_key=True)
    winners = Column(String)
    draws = Column(Integer)
    loses = Column(Integer)
    goalsScored = Column("goals_scored",Integer)
    goalsConceded = Column("goals_conceded",Integer)
    points = Column("points", Integer)

    def __repr__(self):
        r =  self.matchId, self.teamId, self.local, self.matchesPlayed, self.lastMatchesNum,\
                self.winners, self.draws, self.loses, self.goalsScored, self.goalsConceded, self.points
        return str(r)

class Bet(Base):

    __tablename__ = 'bet_match'
    matchId = Column("match_id",String(45),ForeignKey('matches.match_id'),primary_key=True)
    lastMatchesNum = Column("last_matches_num",Integer,primary_key=True)
    local = Column(Boolean,primary_key=True)
    betColumn = Column("bet_column",Integer)
    hit = Column(Boolean)

    def __repr__(self):
        return "(ID: " + self.matchId + ", MATCHES: " + str(self.lastMatchesNum) + ", LOCAL: " +\
         str(self.local) + ", BET: " + str(self.betColumn) +  ", HIT: " + str(self.hit) +')'

class ResumeOdds (Base,ModelMixin):

    __tablename__ = 'resume_odds'

    matchId = Column("match_id",String(45),ForeignKey('matches.match_id'),primary_key=True)
    avgHome = Column("avg_home",Numeric)
    avgDraw = Column("avg_draw",Numeric)
    avgAway = Column("avg_away",Numeric)
    maxHome = Column("max_home",Numeric)
    maxDraw = Column("max_draw",Numeric)
    maxAway = Column("max_away",Numeric)
    minHome = Column("min_home",Numeric)
    minDraw = Column("min_draw",Numeric)
    minAway = Column("min_away",Numeric)
    count = Column("count",Integer)

    def get (matchId):
        return session.query(ResumeOdds).filter(ResumeOdds.matchId==matchId).one()

    def list(self):
        return session.query(ResumeOdds).filter().all()

class ResumeOddsBTS (Base,ModelMixin):

    __tablename__ = 'resume_odds_BTS'

    matchId = Column("match_id",String(45),ForeignKey('matches.match_id'),primary_key=True)
    avgYes = Column("avg_yes",Numeric)
    avgNo = Column("avg_no",Numeric)
    maxYes = Column("max_yes",Numeric)
    maxNo = Column("max_no",Numeric)
    minYes = Column("min_yes",Numeric)
    minNo = Column("min_no",Numeric)
    count = Column("count",Integer)

    def get (matchId):
        return session.query(ResumeOddsBTS).filter(ResumeOddsBTS.matchId==matchId).one()

    def list(self):
        return session.query(ResumeOddsBTS).filter().all()


class ResumeOddsOU (Base,ModelMixin):

    __tablename__ = 'resume_odds_OU'

    matchId = Column("match_id",String(45),ForeignKey('matches.match_id'),primary_key=True)
    goals = Column("goals_num",Integer,primary_key=True)
    avgOver = Column("avg_over",Numeric)
    avgUnder = Column("avg_under",Numeric)
    maxOver = Column("max_over",Numeric)
    maxUnder = Column("max_under",Numeric)
    minOver = Column("min_over",Numeric)
    minUnder = Column("min_under",Numeric)
    count = Column("count",Integer)

    def get (self,matchId, goals):
        return session.query(ResumeOddsOU).filter(ResumeOddsOU.matchId==matchId, ResumeOddsOU.goals==goals).one()

    def listByMatch (self,matchId):
        return session.query(ResumeOddsOU).filter(ResumeOddsOU.matchId==matchId).all()

    def list (self):
        return session.query(ResumeOddsOU).filter().all()

class ResumeOddsAH (Base,ModelMixin):

    __tablename__ = 'resume_odds_AH'

    matchId = Column("match_id",String(45),ForeignKey('matches.match_id'),primary_key=True)
    handicap = Column("handicap",String(45),primary_key=True)
    avgHome = Column("avg_home",Numeric)
    avgAway = Column("avg_away",Numeric)
    maxHome = Column("max_home",Numeric)
    maxAway = Column("max_away",Numeric)
    minHome = Column("min_home",Numeric)
    minAway = Column("min_away",Numeric)
    count = Column("count",Integer)

    def get (self,matchId, handicap):
        return session.query(ResumeOddsAH).filter(ResumeOddsAH.matchId==matchId, ResumeOddsAH.handicap==handicap).one()

    def listByMatch (self,matchId):
        return session.query(ResumeOddsAH).filter(ResumeOddsAH.matchId==matchId).all()

class ResumeOddsDNB (Base,ModelMixin):

    __tablename__ = 'resume_odds_DNB'

    matchId = Column("match_id",String(45),ForeignKey('matches.match_id'),primary_key=True)
    avgHome = Column("avg_home",Numeric)
    avgAway = Column("avg_away",Numeric)
    maxHome = Column("max_home",Numeric)
    maxAway = Column("max_away",Numeric)
    minHome = Column("min_home",Numeric)
    minAway = Column("min_away",Numeric)
    count = Column("count",Integer)

    def get (matchId):
        return session.query(ResumeOddsDNB).filter(ResumeOddsDNB.matchId==matchId).one()

class ResumeOddsDC (Base,ModelMixin):

    __tablename__ = 'resume_odds_DC'

    matchId = Column("match_id",String(45),ForeignKey('matches.match_id'),primary_key=True)
    avgHomeAway = Column("avg_home_away",Numeric)
    avgHomeDraw= Column("avg_home_draw",Numeric)
    avgAwayDraw = Column("avg_away_draw",Numeric)
    maxHomeDraw = Column("max_home_draw",Numeric)
    maxHomeAway = Column("max_home_away",Numeric)
    maxAwayDraw = Column("max_away_draw",Numeric)
    minHomeDraw = Column("min_home_draw",Numeric)
    minHomeAway = Column("min_home_away",Numeric)
    minAwayDraw = Column("min_away_draw",Numeric)
    count = Column("count",Integer)

    def get (matchId):
        return session.query(ResumeOddsDC).filter(ResumeOddsDC.matchId==matchId).one()