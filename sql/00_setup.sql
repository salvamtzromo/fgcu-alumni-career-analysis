-- =====================================================================
-- STEP 0: CREATE THE DATABASE TABLES
-- Run this once. Every raw column is TEXT on purpose: raw data is messy,
-- and we fix types in the cleaning step, not at import.
-- =====================================================================

DROP TABLE IF EXISTS raw_alumni;
CREATE TABLE raw_alumni (
    alumni_id       INTEGER,
    full_name       TEXT,
    position        TEXT,
    hometown        TEXT,
    grad_term       TEXT,
    degree_major    TEXT,
    uin             TEXT,
    personal_email  TEXT,
    school_email    TEXT,
    phone           TEXT,
    instagram       TEXT,
    linkedin        TEXT,
    job             TEXT,
    location        TEXT
);

DROP TABLE IF EXISTS category_lookup;
CREATE TABLE category_lookup (
    alumni_id   INTEGER PRIMARY KEY,
    full_name   TEXT,
    category    TEXT
);
