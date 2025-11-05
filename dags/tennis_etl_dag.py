from __future__ import annotations

import os
import io
import re
import json
import logging
import zipfile
from datetime import datetime, timedelta
from typing import List, Tuple

import pandas as pd
import requests
from dateutil import tz

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator

# =========================
# Config
# =========================

LOCAL_TZ = tz.gettz("America/Argentina/Mendoza")

DEFAULT_YEARS = "2023,2024,2025"
YEARS = [y.strip() for y in os.getenv("YEARS", DEFAULT_YEARS).split(",") if y.strip()]

RAW_DIR = "/tmp/tennis_raw"
os.makedirs(RAW_DIR, exist_ok=True)

# Jeff Sackmann repos raw
ATP_BASE = "https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master"
# matches por año, p.ej. atp_matches_2024.csv
MATCHES_PATTERN = "atp_matches_{year}.csv"
# rankings por año en zips mensuales (para demo, usaremos archivo consolidado semanal)
RANKINGS_WEEKLY = f"{ATP_BASE}/atp_rankings_20s.csv"  # 2000-2099 semanas (consolidado por décadas) — usaremos 20s para demo

POSTGRES_CONN_ID = "postgres_tennis"

# =========================
# Utilidades
# =========================

def _download(url: str, dest_path: str) -> bool:
    """
    Descarga un recurso. Devuelve True si descargó, False si el recurso no existe (404).
    Lanza excepción solo para errores distintos de 404.
    """
    resp = requests.get(url, timeout=60)
    if resp.status_code == 404:
        logging.warning(f"Archivo no encontrado (404), se omite: {url}")
        return False
    resp.raise_for_status()

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "wb") as f:
        f.write(resp.content)
    logging.info(f"Descargado: {url} -> {dest_path} ({len(resp.content)} bytes)")
    return True


def download_data(**context):
    """
    Intenta bajar todos los años definidos en YEARS. Si un año no existe aún en el repo (404),
    lo salta sin fallar la task. También intenta bajar rankings; si falla, marca error.

    Va a GitHub de Jeff Sackmann (donde están los datos de tenis en CSV).

    Descarga archivos de partidos (atp_matches_2023.csv, etc.).

    Los guarda en la carpeta local de Airflow para usarlos.
    """
    downloaded_any = False

    # Partidos por año (omite 404)
    for y in YEARS:
        url = f"{ATP_BASE}/{MATCHES_PATTERN.format(year=y)}"
        out = os.path.join(RAW_DIR, f"atp_matches_{y}.csv")
        ok = _download(url, out)
        if ok:
            downloaded_any = True
        else:
            logging.warning(f"Se omite año {y} porque el CSV no está disponible todavía: {url}")

    if not downloaded_any:
        raise RuntimeError("No se descargó ningún archivo de partidos. Revisa YEARS o tu conectividad.")

    # Rankings (si falla aquí y no es 404, levantamos error; si fuese 404, también error)
    out_rank = os.path.join(RAW_DIR, "atp_rankings_20s.csv")
    ok_rank = _download(RANKINGS_WEEKLY, out_rank)
    if not ok_rank:
        raise RuntimeError("No se encontró el archivo de rankings atp_rankings_20s.csv en el repo remoto.")

# ===== Helpers de I/O y normalización =====



def _read_matches() -> pd.DataFrame:
    """Lee CSVs de partidos (años definidos en YEARS), normaliza tipos básicos,
    elimina duplicados y filtra retiros/walkovers/defaults."""
    dfs = []
    for y in YEARS:
        p = os.path.join(RAW_DIR, f"atp_matches_{y}.csv")
        if os.path.exists(p):
            df = pd.read_csv(p)
            dfs.append(df)
        else:
            logging.warning(f"[matches] no existe archivo: {p}")
    if not dfs:
        raise RuntimeError("No se encontraron archivos de partidos en RAW_DIR.")

    df = pd.concat(dfs, ignore_index=True)

    # tourney_date: entero YYYYMMDD -> date
    if "tourney_date" in df.columns:
        df["tourney_date"] = pd.to_datetime(df["tourney_date"], format="%Y%m%d", errors="coerce").dt.date

    # match_num a int seguro
    if "match_num" in df.columns:
        df["match_num"] = pd.to_numeric(df["match_num"], errors="coerce").fillna(0).astype(int)
    else:
        df["match_num"] = range(1, len(df) + 1)

    # match_id estable para esta etapa
    df["tourney_id"] = df["tourney_id"].astype(str)
    df["match_id"] = df["tourney_id"] + "-" + df["match_num"].astype(str)

    # eliminar duplicados exactos
    dup_keys = [c for c in ["match_id", "winner_id", "loser_id"] if c in df.columns]
    if dup_keys:
        before = len(df)
        df = df.drop_duplicates(subset=dup_keys)
        logging.info(f"[matches] drop_duplicates {dup_keys}: {before} -> {len(df)} filas")

    # filtrar RET / W/O / DEF en score
    def is_invalid_score(s):
        if pd.isna(s):
            return False
        s = str(s).upper()
        return ("RET" in s) or ("W/O" in s) or ("DEF" in s)

    if "score" in df.columns:
        before = len(df)
        df = df[~df["score"].apply(is_invalid_score)].copy()
        logging.info(f"[matches] filtro RET/W/O/DEF: {before} -> {len(df)} filas")

    # normalizar numéricos principales (si existen)
    for c in [
        "winner_id", "loser_id", "winner_rank", "loser_rank",
        "winner_rank_points", "loser_rank_points",
        "minutes", "winner_ht", "loser_ht",
        "best_of"
    ]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # columnas mínimas para esta etapa
    keep = [
        "match_id", "tourney_id", "tourney_name", "surface", "tourney_level", "tourney_date",
        "match_num", "best_of", "round", "minutes",
        "winner_id", "winner_name", "winner_hand", "winner_ht", "winner_age", "winner_rank", "winner_rank_points",
        "loser_id",  "loser_name",  "loser_hand",  "loser_ht",  "loser_age",  "loser_rank",  "loser_rank_points",
        "score"
    ]
    cols = [c for c in keep if c in df.columns]
    df = df[cols].copy()

    logging.info(f"[matches] listo: filas={len(df)} cols={len(df.columns)}")
    return df


def _read_rankings() -> pd.DataFrame:
    """Lee y concatena todos los archivos atp_rankings_*.csv,
    normaliza columnas y loguea qué columnas detecta en cada archivo.
    """
    import glob

    paths = sorted(glob.glob(os.path.join(RAW_DIR, "atp_rankings_*.csv")))
    if not paths:
        raise RuntimeError("No se encontraron archivos de rankings en RAW_DIR.")

    frames = []
    for p in paths:
        r = pd.read_csv(p)
        logging.info(f"[rankings] file {os.path.basename(p)} columnas: {list(r.columns)}")

        # Normalizar nombres de columnas
        lower_cols = {c.lower(): c for c in r.columns}
        if "player" in lower_cols:  # algunos CSV usan 'player'
            r = r.rename(columns={lower_cols["player"]: "player_id"})
        if "player_id" not in r.columns:
            raise RuntimeError(f"El archivo {p} no tiene 'player_id' ni 'player'.")

        if "ranking_date" in r.columns:
            r["ranking_date"] = pd.to_datetime(r["ranking_date"], format="%Y%m%d", errors="coerce")

        r = r.dropna(subset=["player_id", "ranking_date"])
        r["player_id"] = pd.to_numeric(r["player_id"], errors="coerce")
        r = r.dropna(subset=["player_id"])
        r = r.astype({"player_id": "int64"})
        # rank/points a numéricos
        if "rank" in r.columns:
            r["rank"] = pd.to_numeric(r["rank"], errors="coerce")
        if "points" in r.columns:
            r["points"] = pd.to_numeric(r["points"], errors="coerce")
        frames.append(r)

    rankings = pd.concat(frames, ignore_index=True)
    # Dedup prudente por (player_id, ranking_date)
    rankings = rankings.sort_values(["player_id", "ranking_date", "rank", "points"])
    rankings = rankings.drop_duplicates(subset=["player_id", "ranking_date"], keep="last")
    rankings = rankings.sort_values(["player_id", "ranking_date"]).reset_index(drop=True)

    logging.info(f"[rankings] concatenado: filas={len(rankings)} cols={len(rankings.columns)}")
    return rankings


# Función normalize_types 
def normalize_types(df: pd.DataFrame, null_policy: str = "zero_fill") -> pd.DataFrame:
    """
    Normaliza tipos de datos del dataset de tenis para que sean compatibles con Postgres.
    - Convierte IDs, ranks y contadores a int
    - Convierte métricas continuas a float
    - Strings se aseguran como object/str
    - Aplica política de nulos (cero por defecto)
    """
    out = df.copy()

    # --- IDs y metadatos ---
    id_cols = ["match_id", "tourney_id", "winner_id", "loser_id"]
    for c in id_cols:
        if c in out.columns:
            out[c] = out[c].astype(str)

    # --- Columnas enteras (duraciones, números de partido, rankings, alturas, puntos) ---
    int_cols = [
        "minutes", "match_num", "best_of",
        "winner_ht", "loser_ht",
        "winner_rank", "loser_rank",
        "winner_rank_points", "loser_rank_points",
        "winner_rank_prev", "loser_rank_prev",
        "winner_pts_prev", "loser_pts_prev"
    ]
    for c in int_cols:
        if c in out.columns:
            out[c] = pd.to_numeric(out[c], errors="coerce")
            if null_policy == "zero_fill":
                out[c] = out[c].fillna(0).astype(int)
            else:
                out[c] = out[c].astype("Int64")  # soporta nulls

    # --- Columnas decimales (edades, métricas continuas) ---
    float_cols = ["winner_age", "loser_age"]
    for c in float_cols:
        if c in out.columns:
            out[c] = pd.to_numeric(out[c], errors="coerce")
            if null_policy == "zero_fill":
                out[c] = out[c].fillna(0).astype(float)

    # --- Métricas de juego (aces, dobles faltas, servicios, etc.) ---
    stats_cols = [
        "w_ace", "w_df", "w_svpt", "w_1stIn", "w_1stWon", "w_2ndWon",
        "w_svGms", "w_bpSaved", "w_bpFaced",
        "l_ace", "l_df", "l_svpt", "l_1stIn", "l_1stWon", "l_2ndWon",
        "l_svGms", "l_bpSaved", "l_bpFaced"
    ]
    for c in stats_cols:
        if c in out.columns:
            out[c] = pd.to_numeric(out[c], errors="coerce")
            if null_policy == "zero_fill":
                out[c] = out[c].fillna(0).astype(int)
            else:
                out[c] = out[c].astype("Int64")

    # --- Texto / categóricas ---
    str_cols = [
        "tourney_name", "surface", "tourney_level",
        "round", "winner_name", "winner_hand",
        "loser_name", "loser_hand", "score"
    ]
    for c in str_cols:
        if c in out.columns:
            out[c] = out[c].astype(str)

    # --- Fecha ---
    if "tourney_date" in out.columns:
        out["tourney_date"] = pd.to_datetime(out["tourney_date"], errors="coerce")

    return out

# Función adicional para debugging 
def inspect_csv_before_load():
    """Función temporal para inspeccionar el CSV generado"""
    csv_path = os.path.join(RAW_DIR, "matches_staging.csv")
    
    if not os.path.exists(csv_path):
        logging.error(f"CSV no existe: {csv_path}")
        return
    
    # Leer solo las primeras líneas
    with open(csv_path, 'r') as f:
        lines = [f.readline().strip() for _ in range(5)]
    
    logging.info(f"Primeras 5 líneas del CSV:")
    for i, line in enumerate(lines):
        logging.info(f"Línea {i}: {line}")
        
    # También usar pandas para ver tipos
    df_check = pd.read_csv(csv_path, nrows=10)
    logging.info(f"Tipos detectados por pandas: {dict(df_check.dtypes)}")
    
    # Mostrar valores de las columnas problemáticas
    prob_cols = ['winner_rank_prev', 'loser_rank_prev']
    for col in prob_cols:
        if col in df_check.columns:
            logging.info(f"{col} valores: {df_check[col].tolist()}")


# ===== Tarea principal: Transform & Enrich =====

def transform_and_enrich(**context):
    """
    - Lee partidos (limpios) y rankings (normalizados).
    - Enlaza ranking previo de winner/loser con merge_asof global + fallback por jugador.
    - Normaliza tipos para que el COPY a Postgres no falle.
    - Exporta /tmp/tennis_raw/matches_staging.csv.
    -----
    Mas simplemente:
    Abre esos CSV y los lee con pandas.

    Normaliza tipos de datos (fechas → fecha, rankings → enteros, edad → float, nombres → texto).

    Limpia datos sucios (ej: partidos con “W/O” o “RET” que no sirven).

    Agrega rankings previos y puntos previos.
    """
    def _ensure_sorted(df, keys):
        return df.sort_values(keys).reset_index(drop=True)

        # Función _asof_with_fallback 
    def _asof_with_fallback(keys_df, r_df, side_prefix):
        """
        keys_df: [match_id, player_id, match_dt]
        r_df:    [player_id, ranking_date, rank, points]
        side_prefix: 'winner' | 'loser'
        """
        # Crear una copia para no modificar el original
        r = r_df.copy()
        
        # Asegurar que las columnas necesarias existen
        required_cols = ['player_id', 'ranking_date', 'rank', 'points']
        missing_cols = [col for col in required_cols if col not in r.columns]
        if missing_cols:
            logging.error(f"Columnas faltantes en rankings: {missing_cols}")
            logging.error(f"Columnas disponibles: {list(r.columns)}")
            raise ValueError(f"Columnas faltantes en rankings: {missing_cols}")
        
        # Renombrar solo ranking_date para evitar confusiones
        r = r.rename(columns={"ranking_date": "rank_dt"})
        
        try:
            # Asegurar ordenamiento correcto
            left = _ensure_sorted(keys_df, ["player_id", "match_dt"])
            right = _ensure_sorted(r, ["player_id", "rank_dt"])
            
            # Hacer el merge_asof
            joined = pd.merge_asof(
                left, right,
                left_on="match_dt", right_on="rank_dt",
                by="player_id", direction="backward", allow_exact_matches=True
            )
            
            logging.info(f"[{side_prefix}] merge_asof exitoso: {len(joined)} filas")
            
        except Exception as e:
            logging.warning(f"[{side_prefix}] merge_asof global falló ({e}); usando fallback por jugador.")
            parts = []
            for pid, g in keys_df.groupby("player_id", sort=True):
                if pd.isna(pid):
                    continue
                g2 = g.sort_values("match_dt").copy()
                r2 = r[r["player_id"] == pid].sort_values("rank_dt").copy()
                
                if r2.empty:
                    # No hay datos de ranking para este jugador
                    tmp = g2.copy()
                    tmp["rank"] = pd.NA
                    tmp["points"] = pd.NA
                    parts.append(tmp[["match_id", "rank", "points"]])
                else:
                    # Hacer merge_asof por jugador individual
                    j = pd.merge_asof(
                        g2, r2,
                        left_on="match_dt", right_on="rank_dt",
                        direction="backward", allow_exact_matches=True
                    )
                    parts.append(j[["match_id", "rank", "points"]])
            
            if parts:
                joined = pd.concat(parts, ignore_index=True)
            else:
                # Si no hay partes, crear un DataFrame vacío con las columnas correctas
                joined = keys_df.copy()
                joined["rank"] = pd.NA
                joined["points"] = pd.NA

        # Renombrar las columnas finales SOLO las de rank y points
        rename_dict = {
            "rank": f"{side_prefix}_rank_prev",
            "points": f"{side_prefix}_pts_prev"
        }
        joined = joined.rename(columns=rename_dict)
        
        # Retornar solo las columnas que necesitamos
        result_cols = ["match_id", f"{side_prefix}_rank_prev", f"{side_prefix}_pts_prev"]
        result = joined[result_cols].copy()
        
        logging.info(f"[{side_prefix}] resultado final: {len(result)} filas, columnas: {list(result.columns)}")
        
        return result

    # 1) Data base
    matches = _read_matches()      # filtra RET/W/O/DEF y normaliza básicas
    rankings = _read_rankings()    # normaliza columnas/tipos y loguea columnas

    logging.info(f"[transform] matches: filas={len(matches)} cols={matches.shape[1]}")
    logging.info(f"[transform] rankings: filas={len(rankings)} cols={rankings.shape[1]}")

    # 2) Claves y tipos mínimos
    matches["tourney_datetime"] = pd.to_datetime(matches["tourney_date"], errors="coerce")
    for c in ("winner_id", "loser_id"):
        if c in matches.columns:
            matches[c] = pd.to_numeric(matches[c], errors="coerce")

    rankings = rankings.dropna(subset=["player_id", "ranking_date"]).copy()
    rankings["player_id"] = pd.to_numeric(rankings["player_id"], errors="coerce")
    rankings = rankings.dropna(subset=["player_id"]).copy()
    rankings["player_id"] = rankings["player_id"].astype("int64")

    # 3) Keys winner/loser
    win_key = matches[["match_id", "winner_id", "tourney_datetime"]].rename(
        columns={"winner_id": "player_id", "tourney_datetime": "match_dt"}
    ).dropna(subset=["player_id", "match_dt"]).copy()
    win_key["player_id"] = pd.to_numeric(win_key["player_id"], errors="coerce").astype("int64")

    los_key = matches[["match_id", "loser_id", "tourney_datetime"]].rename(
        columns={"loser_id": "player_id", "tourney_datetime": "match_dt"}
    ).dropna(subset=["player_id", "match_dt"]).copy()
    los_key["player_id"] = pd.to_numeric(los_key["player_id"], errors="coerce").astype("int64")

    logging.info(f"[transform] win_key filas={len(win_key)}, los_key filas={len(los_key)} | rankings filas={len(rankings)}")

    # 4) Enriquecimiento con ranking previo
    win_join = _asof_with_fallback(win_key, rankings, "winner")
    los_join = _asof_with_fallback(los_key, rankings, "loser")

    # 5) Merge final
    out = matches.merge(win_join, on="match_id", how="left").merge(los_join, on="match_id", how="left")

    # 6) Normalización completa para COPY
    out = normalize_types(out, null_policy="zero_fill")  # o "nullable" si preferís conservar NULLs en previos

    
    cols_for_staging = [
    "match_id","tourney_id","tourney_name","surface","tourney_level","tourney_date",
    "match_num","best_of","round","minutes",
    "winner_id","winner_name","winner_hand","winner_ht","winner_age","winner_rank","winner_rank_points",
    "loser_id","loser_name","loser_hand","loser_ht","loser_age","loser_rank","loser_rank_points",
    "score",
    "winner_rank_prev","winner_pts_prev","loser_rank_prev","loser_pts_prev"
    ]

    out = out[[c for c in cols_for_staging if c in out.columns]].copy()

    # 7) Export CSV staging
    csv_path = os.path.join(RAW_DIR, "matches_staging.csv")
    out.to_csv(csv_path, index=False)

    # Además, exportar un CSV limpio para la entrega (persistente en el host)
    deliver_dir = "/opt/airflow/dags/exports"
    os.makedirs(deliver_dir, exist_ok=True)
    deliver_path = os.path.join(deliver_dir, "matches_cleaned.csv")
    out.to_csv(deliver_path, index=False)
    logging.info("[transform] CSV limpio exportado para entrega: %s", deliver_path)

    logging.info(
        "[transform] Staging generado: %s | filas=%d, cols=%d | NaNs winner_rank_prev=%d, loser_rank_prev=%d",
        csv_path, len(out), out.shape[1],
        out["winner_rank_prev"].isna().sum() if "winner_rank_prev" in out else -1,
        out["loser_rank_prev"].isna().sum() if "loser_rank_prev" in out else -1
    )

def create_schema_task():
    # Ejecuta los SQL de schema y truncate staging
    pass

# Función load_to_staging mejorada (opcional, con debugging)
def load_to_staging_with_debug(**context):
    """Versión con debugging de load_to_staging"""
    
    # Primero inspeccionar el CSV
    inspect_csv_before_load()
    
    # Luego proceder con el COPY
    pg = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
    csv_path = os.path.join(RAW_DIR, "matches_staging.csv")
    if not os.path.exists(csv_path):
        raise RuntimeError("No existe matches_staging.csv")
    
    with pg.get_conn() as conn, conn.cursor() as cur, open(csv_path, "r", encoding="utf-8") as f:
        # Truncar primero
        cur.execute("TRUNCATE tennis.matches_staging;")
        
        # Luego hacer COPY
        cur.copy_expert(
            sql="""
            COPY tennis.matches_staging (
                match_id, tourney_id, tourney_name, surface, tourney_level, tourney_date,
                match_num, best_of, round, minutes,
                winner_id, winner_name, winner_hand, winner_ht, winner_age, winner_rank, winner_rank_points,
                loser_id, loser_name, loser_hand, loser_ht, loser_age, loser_rank, loser_rank_points,
                score,
                -- IMPORTANTE: este orden debe coincidir con el CSV
                winner_rank_prev, winner_pts_prev, loser_rank_prev, loser_pts_prev
            )
            FROM STDIN WITH (FORMAT csv, HEADER true, DELIMITER ',');
            """,
            file=f
        )
        conn.commit()
    
    logging.info("COPY completado exitosamente")

# =========================
# DAG
# =========================

default_args = {
    "owner": "Juan Ignacio Barranco Bastán",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}

with DAG(
    dag_id="tennis_data_ingestion_dag",
    start_date=datetime(2025, 9, 1),
    schedule_interval="@weekly",  # cumple la consigna de ejecución periódica
    catchup=False,
    default_args=default_args,
    description="ETL Tennis ATP (Sackmann) -> Postgres con limpieza y ranking previo",
    tags=["tennis", "ao26", "etl", "airflow"],
    template_searchpath=["/opt/airflow/include/sql"]
) as dag:

    t_download = PythonOperator(
        task_id="download_sources",
        python_callable=download_data
    )

    t_transform = PythonOperator(
        task_id="transform_and_enrich",
        python_callable=transform_and_enrich
    )

    t_create_schema = PostgresOperator(
        task_id="create_schema",
        postgres_conn_id=POSTGRES_CONN_ID,
        sql="00_create_schema.sql"
    )

    t_load_staging = PythonOperator(
        task_id="load_to_staging",
        python_callable=load_to_staging_with_debug  
    )

    t_upsert = PostgresOperator(
        task_id="upsert_into_production",
        postgres_conn_id=POSTGRES_CONN_ID,
        sql="10_upsert_matches.sql"
    )

    t_download >> t_transform >> t_create_schema >> t_load_staging >> t_upsert
