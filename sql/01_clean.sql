-- =====================================================================
-- STEP 1: CLEAN THE RAW DATA  (PostgreSQL)
-- Input : raw_alumni, category_lookup
-- Output: alumni_clean
-- Rule  : never edit raw_alumni. Always build a new table from it.
-- =====================================================================

DROP TABLE IF EXISTS alumni_clean;

CREATE TABLE alumni_clean AS
SELECT
    r.alumni_id,
    TRIM(r.full_name) AS full_name,

    -- "Summer 2016" -> 2016. "n/a" and blanks -> NULL
    CASE WHEN TRIM(r.grad_term) ~ '[0-9]{4}$'
         THEN RIGHT(TRIM(r.grad_term), 4)::INT END AS grad_year,

    -- "NO MATCH" in the ID column is a placeholder, not a real ID
    CASE WHEN TRIM(r.uin) IN ('', 'NO MATCH') THEN NULL ELSE TRIM(r.uin) END AS uin,

    -- prefer the personal email, fall back to the school one
    COALESCE(NULLIF(TRIM(r.personal_email), ''), NULLIF(TRIM(r.school_email), '')) AS email,
    CASE WHEN NULLIF(TRIM(r.personal_email), '') IS NOT NULL THEN 'personal'
         WHEN NULLIF(TRIM(r.school_email), '')   IS NOT NULL THEN 'school' END AS email_type,

    -- strip every non-digit, then format 10-digit US numbers
    CASE
      WHEN LENGTH(d.digits) = 10
        THEN '(' || SUBSTRING(d.digits,1,3) || ') ' || SUBSTRING(d.digits,4,3) || '-' || SUBSTRING(d.digits,7,4)
      WHEN NULLIF(TRIM(r.phone), '') IS NOT NULL
        THEN REPLACE(TRIM(r.phone), '00+', '+')   -- international: leave as entered
    END AS phone,

    NULLIF(REPLACE(TRIM(r.instagram), '@', ''), '') AS instagram,
    NULLIF(TRIM(r.linkedin), '')                    AS linkedin,
    NULLIF(TRIM(r.job), '')                         AS job,

    -- '?' means "we looked and don't know"
    CASE WHEN TRIM(r.location) IN ('', '?') THEN NULL ELSE TRIM(r.location) END AS location,

    COALESCE(c.category, 'Career not confirmed') AS category
FROM raw_alumni AS r
CROSS JOIN LATERAL (
    SELECT REGEXP_REPLACE(COALESCE(r.phone, ''), '\D', '', 'g') AS digits
) AS d
LEFT JOIN category_lookup AS c ON c.alumni_id = r.alumni_id;

-- Flag who we can actually reach
ALTER TABLE alumni_clean ADD COLUMN reachable BOOLEAN;
UPDATE alumni_clean
SET reachable = (email IS NOT NULL OR phone IS NOT NULL
              OR instagram IS NOT NULL OR linkedin IS NOT NULL);

-- Add a key so the table behaves like a real table
ALTER TABLE alumni_clean ADD PRIMARY KEY (alumni_id);
