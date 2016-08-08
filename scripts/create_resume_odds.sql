delete from resume_odds;
delete from resume_odds_BTS;
delete from resume_odds_OU;
delete from resume_odds_AH;
delete from resume_odds_DC;
delete from resume_odds_DNB;

INSERT INTO resume_odds
 Select match_id,
 ROUND(AVG(odds_home),2), ROUND(AVG(odds_draw),2), ROUND(AVG(odds_away),2),
 ROUND(MAX(odds_home),2), ROUND(MAX(odds_draw),2), ROUND(MAX(odds_away),2),
 ROUND(MIN(odds_home),2) , ROUND(MIN(odds_draw),2), ROUND(MIN(odds_away),2),
 COUNT(*) from odds
 group by match_id;

INSERT INTO resume_odds_BTS
Select match_id,
 ROUND(AVG(odds_yes),2), ROUND(AVG(odds_no),2),
 ROUND(MAX(odds_yes),2) , ROUND(MAX(odds_no),2),
 ROUND(MIN(odds_yes),2), ROUND(MIN(odds_no),2),
 COUNT(*) from odds_BTS
 group by match_id;

 INSERT INTO resume_odds_OU
 Select match_id, goals_num,
 ROUND(AVG(odds_over),2), ROUND(AVG(odds_under),2),
 ROUND(MAX(odds_over),2), ROUND(MAX(odds_under),2),
 ROUND(MIN(odds_over),2) , ROUND(MIN(odds_under),2),
 COUNT(*) from odds_OU
 group by match_id, goals_num;

 INSERT INTO resume_odds_AH
 Select match_id, handicap,
 ROUND(AVG(odds_home),2), ROUND(AVG(odds_away),2),
 ROUND(MAX(odds_home),2), ROUND(MAX(odds_away),2),
 ROUND(MIN(odds_home),2), ROUND(MIN(odds_away),2),
 COUNT(*) from odds_AH
 group by match_id, handicap;

 INSERT INTO resume_odds_DC
 Select match_id,
 ROUND(AVG(odds_home_draw),2), ROUND(AVG(odds_home_away),2), ROUND(AVG(odds_away_draw),2),
 ROUND(MAX(odds_home_draw),2), ROUND(MAX(odds_home_away),2), ROUND(MAX(odds_away_draw),2),
 ROUND(MIN(odds_home_draw),2) , ROUND(MIN(odds_home_away),2), ROUND(MIN(odds_away_draw),2),
 COUNT(*) from odds_DC
 group by match_id;

 INSERT INTO resume_odds_DNB
 Select match_id,
 ROUND(AVG(odds_home),2), ROUND(AVG(odds_away),2),
 ROUND(MAX(odds_home),2), ROUND(MAX(odds_away),2),
 ROUND(MIN(odds_home),2), ROUND(MIN(odds_away),2),
 COUNT(*) from odds_DNB
 group by match_id;