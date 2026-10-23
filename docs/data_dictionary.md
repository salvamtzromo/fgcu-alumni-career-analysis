# Data dictionary

## raw_alumni (as entered, nothing fixed)
| Column | Meaning |
|---|---|
| alumni_id | Row number in the source sheet |
| full_name | Player name |
| position | GK, D, MF or F |
| hometown | Hometown from the roster |
| grad_term | Graduation term as typed, such as `Summer 2018`, or `n/a` |
| degree_major | Degree or major |
| uin | University ID, or `NO MATCH` when the record match failed |
| personal_email / school_email | Two email fields, either may be blank |
| phone | Phone number in whatever format it was entered |
| instagram | Handle, sometimes with `@` |
| linkedin | Profile URL |
| job | Current role, as found on a public profile |
| location | Current city or country, or `?` if unknown |

## alumni_clean (built by sql/01_clean.sql)
| Column | Rule |
|---|---|
| grad_year | Last four digits of grad_term. `NULL` if none |
| uin | `NULL` when blank or `NO MATCH` |
| email | personal email, else school email |
| email_type | `personal` or `school` |
| phone | 10-digit US numbers formatted `(XXX) XXX-XXXX`. International numbers keep their format with `+` |
| instagram | Handle without `@` |
| category | Career field from category_lookup, or `Career not confirmed` |
| reachable | True if any of email, phone, Instagram or LinkedIn exists |

## category_lookup
One row per alumnus with a confirmed job: `alumni_id`, `full_name`, `category`.
Categories were assigned by reading each job title and choosing the closest of 12 fields.
