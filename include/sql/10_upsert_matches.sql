INSERT INTO tennis.matches_cleaned AS t (
    match_id, tourney_id, tourney_name, surface, tourney_level, tourney_date,
    match_num, best_of, round, minutes,
    winner_id, winner_name, winner_hand, winner_ht, winner_age, winner_rank, winner_rank_points,
    loser_id,  loser_name,  loser_hand,  loser_ht,  loser_age,  loser_rank,  loser_rank_points,
    score, winner_rank_prev, loser_rank_prev, winner_pts_prev, loser_pts_prev, created_at
)
SELECT
    match_id, tourney_id, tourney_name, surface, tourney_level, tourney_date,
    match_num, best_of, round, minutes,
    winner_id, winner_name, winner_hand, winner_ht, winner_age, winner_rank, winner_rank_points,
    loser_id,  loser_name,  loser_hand,  loser_ht,  loser_age,  loser_rank,  loser_rank_points,
    score, winner_rank_prev, loser_rank_prev, winner_pts_prev, loser_pts_prev, NOW()
FROM tennis.matches_staging
ON CONFLICT (match_id) DO UPDATE SET
    tourney_name       = EXCLUDED.tourney_name,
    surface            = EXCLUDED.surface,
    tourney_level      = EXCLUDED.tourney_level,
    tourney_date       = EXCLUDED.tourney_date,
    match_num          = EXCLUDED.match_num,
    best_of            = EXCLUDED.best_of,
    round              = EXCLUDED.round,
    minutes            = EXCLUDED.minutes,
    winner_rank        = EXCLUDED.winner_rank,
    winner_rank_points = EXCLUDED.winner_rank_points,
    loser_rank         = EXCLUDED.loser_rank,
    loser_rank_points  = EXCLUDED.loser_rank_points,
    score              = EXCLUDED.score,
    winner_rank_prev   = EXCLUDED.winner_rank_prev,
    loser_rank_prev    = EXCLUDED.loser_rank_prev,
    winner_pts_prev    = EXCLUDED.winner_pts_prev,
    loser_pts_prev     = EXCLUDED.loser_pts_prev,
    created_at         = NOW();
