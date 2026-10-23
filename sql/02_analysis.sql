-- =====================================================================
-- STEP 2: THE FINDINGS
-- Each query answers one number in the report. Run them one at a time.
-- Expected results are in the comments. If yours differ, find out why.
-- =====================================================================

-- 1. Total letterwinners                                  -- expect 176
SELECT COUNT(*) AS total_alumni FROM alumni_clean;

-- 2. Career paths confirmed                               -- expect 109
SELECT COUNT(*) AS careers_confirmed FROM alumni_clean WHERE job IS NOT NULL;

-- 3. Alumni we can reach (any contact method)             -- expect 136
SELECT COUNT(*) AS reachable FROM alumni_clean WHERE reachable;

-- 4. Alumni with no contact information at all            -- expect 40
SELECT COUNT(*) AS no_contact FROM alumni_clean WHERE NOT reachable;

-- 5. Contact coverage by type                             -- expect email 105, phone 92, linkedin 102, instagram 88
SELECT
    COUNT(email)     AS with_email,
    COUNT(phone)     AS with_phone,
    COUNT(linkedin)  AS with_linkedin,
    COUNT(instagram) AS with_instagram
FROM alumni_clean;

-- 6. What alumni do now                                   -- expect Sales 19, Pro Soccer 17, Coaching 16 ...
SELECT category, COUNT(*) AS alumni
FROM alumni_clean
WHERE job IS NOT NULL
GROUP BY category
ORDER BY alumni DESC;

-- 7. Still in soccer (playing, coaching or sports business)  -- expect 33
SELECT COUNT(*) AS still_in_soccer
FROM alumni_clean
WHERE category IN ('Professional Soccer', 'Coaching, Performance & Sports Industry');

-- 8. Share of confirmed alumni in each field (percent)
SELECT category,
       COUNT(*) AS alumni,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM alumni_clean WHERE job IS NOT NULL), 1) AS pct
FROM alumni_clean
WHERE job IS NOT NULL
GROUP BY category
ORDER BY alumni DESC;

-- 9. Reachable alumni whose career we haven't confirmed yet   -- the "go find them" list
SELECT full_name, grad_year, email, phone
FROM alumni_clean
WHERE reachable AND job IS NULL
ORDER BY grad_year DESC;

-- 10. Data quality check: contact coverage by graduating class
SELECT grad_year,
       COUNT(*) AS alumni,
       SUM(reachable::INT) AS reachable,
       ROUND(100.0 * SUM(reachable::INT) / COUNT(*), 0) AS pct_reachable
FROM alumni_clean
WHERE grad_year IS NOT NULL
GROUP BY grad_year
ORDER BY grad_year;
