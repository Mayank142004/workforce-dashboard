import sqlite3
from config import DB_PATH


# --------------------------------------------------
# DB Connection (safe for background agent)
# --------------------------------------------------
def get_conn():
    return sqlite3.connect(DB_PATH, timeout=10)


# --------------------------------------------------
# Initialize / Upgrade DB
# --------------------------------------------------
def init_db():
    conn = get_conn()
    cur = conn.cursor()

    # Main table (single source of truth)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS daily_work (
            work_date TEXT PRIMARY KEY,
            normal_seconds INTEGER DEFAULT 0,
            ot_seconds INTEGER DEFAULT 0,
            first_seen TEXT,
            last_seen TEXT
        )
    """)

    # ---- SAFE UPGRADE FOR OLD DATABASES ----
    existing_cols = [row[1] for row in cur.execute("PRAGMA table_info(daily_work)")]

    if "first_seen" not in existing_cols:
        cur.execute("ALTER TABLE daily_work ADD COLUMN first_seen TEXT")

    if "last_seen" not in existing_cols:
        cur.execute("ALTER TABLE daily_work ADD COLUMN last_seen TEXT")

    conn.commit()
    conn.close()

    print("✅ Local DB initialized / upgraded (daily_work)")


# --------------------------------------------------
# Save / Update Day (called EVERY MINUTE by agent)
# --------------------------------------------------
def save_day(work_date, normal_sec, ot_sec, first_seen, last_seen):
    """
    work_date   : YYYY-MM-DD
    normal_sec  : seconds (max 8 hrs)
    ot_sec      : seconds (max 4 hrs)
    first_seen  : YYYY-MM-DD HH:MM:SS or None
    last_seen   : YYYY-MM-DD HH:MM:SS or None
    """

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO daily_work (
            work_date,
            normal_seconds,
            ot_seconds,
            first_seen,
            last_seen
        )
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(work_date)
        DO UPDATE SET
            normal_seconds = excluded.normal_seconds,
            ot_seconds     = excluded.ot_seconds,

            -- first_seen is set ONLY ONCE (first activity)
            first_seen = COALESCE(daily_work.first_seen, excluded.first_seen),

            -- last_seen ALWAYS moves forward (latest activity)
            last_seen  = excluded.last_seen
    """, (
        work_date,
        normal_sec,
        ot_sec,
        first_seen,
        last_seen
    ))

    conn.commit()
    conn.close()
