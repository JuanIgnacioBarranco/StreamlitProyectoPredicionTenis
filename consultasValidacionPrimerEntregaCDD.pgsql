-- 1. Unicidad del ID de partido
SELECT COUNT(*)                                           AS total,
       COUNT(DISTINCT match_id)                           AS distintos,
       COUNT(*) - COUNT(DISTINCT match_id)                AS duplicados
FROM tennis.matches_cleaned;

-- 2. Fechas válidas y rango esperado
SELECT MIN(tourney_date) AS min_date, MAX(tourney_date) AS max_date
FROM tennis.matches_cleaned;

-- 3. Sin retiros/walkovers/defaults (limpieza aplicada)
SELECT COUNT(*) AS sospechosos
FROM tennis.matches_cleaned
WHERE UPPER(score) LIKE '%RET%' OR UPPER(score) LIKE '%W/O%' OR UPPER(score) LIKE '%DEF%';

-- 4. Tipos: minutos y best_of coherentes
SELECT SUM(CASE WHEN minutes < 0 THEN 1 ELSE 0 END) AS minutos_negativos,
       COUNT(*) FILTER (WHERE best_of NOT IN (3,5)) AS best_of_raro
FROM tennis.matches_cleaned;

-- 5. Ranks y puntos no negativos
SELECT
  COUNT(*) FILTER (WHERE winner_rank < 0 OR loser_rank < 0) AS rank_neg,
  COUNT(*) FILTER (WHERE winner_rank_points < 0 OR loser_rank_points < 0) AS pts_neg
FROM tennis.matches_cleaned;

-- 6. Integridad de previos (si no hay histórico, deberían ser 0 o NULL según tu política)
SELECT
  COUNT(*) FILTER (WHERE winner_rank_prev IS NULL) AS nulls_win_prev,
  COUNT(*) FILTER (WHERE loser_rank_prev IS NULL)  AS nulls_lose_prev
FROM tennis.matches_cleaned;

-- 7. Distribución por superficie, nivel y año (detección de cargas parciales)
SELECT surface, tourney_level, EXTRACT(YEAR FROM tourney_date) AS anio, COUNT(*) cnt
FROM tennis.matches_cleaned
GROUP BY 1,2,3
ORDER BY 3,2,1;

-- 8. Mismo jugador en winner/loser (no debería pasar)
SELECT COUNT(*) AS mismo_jugador
FROM tennis.matches_cleaned
WHERE winner_id = loser_id;


--Checks de “join de ranking previo”
-- ¿qué proporción de partidos consiguió ranking previo para ambos jugadores?
SELECT
  COUNT(*) AS total,
  COUNT(*) FILTER (WHERE winner_rank_prev IS NOT NULL AND loser_rank_prev IS NOT NULL) AS ambos_prev,
  ROUND(100.0 * COUNT(*) FILTER (WHERE winner_rank_prev IS NOT NULL AND loser_rank_prev IS NOT NULL) / NULLIF(COUNT(*),0), 2) AS pct_ambos_prev
FROM tennis.matches_cleaned;