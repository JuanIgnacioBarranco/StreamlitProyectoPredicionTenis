CREATE SCHEMA IF NOT EXISTS tennis;

CREATE TABLE IF NOT EXISTS tennis.matches_cleaned (
    match_id           TEXT PRIMARY KEY,
    tourney_id         TEXT,
    tourney_name       TEXT,
    surface            TEXT,
    tourney_level      TEXT,
    tourney_date       DATE,
    match_num          INT,
    best_of            INT,
    round              TEXT,
    minutes            INT,

    winner_id          INT,
    winner_name        TEXT,
    winner_hand        TEXT,
    winner_ht          INT,
    winner_age         REAL,
    winner_rank        INT,
    winner_rank_points INT,

    loser_id           INT,
    loser_name         TEXT,
    loser_hand         TEXT,
    loser_ht           INT,
    loser_age          REAL,
    loser_rank         INT,
    loser_rank_points  INT,

    score              TEXT,

    winner_rank_prev   INT,
    loser_rank_prev    INT,
    winner_pts_prev    INT,
    loser_pts_prev     INT,

    created_at         TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tennis.matches_staging (LIKE tennis.matches_cleaned INCLUDING ALL);
TRUNCATE tennis.matches_staging;
