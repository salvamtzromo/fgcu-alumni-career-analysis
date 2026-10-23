"""
Generates a SYNTHETIC alumni dataset for this repo.

The real project used private records of former FGCU men's soccer players.
That data contains phone numbers and emails, so it is not published here.
This script creates fake people with the same columns, the same kinds of
messy values, and the same overall counts, so every query in /sql runs and
produces the findings described in the README.

Run:  python scripts/generate_synthetic_data.py
"""
import csv, random

random.seed(42)

FIRST = ["Alex","Brian","Carlos","Daniel","Eric","Fabian","Gabriel","Hugo","Ivan","Jonas",
         "Kevin","Lucas","Mateo","Nolan","Oscar","Pablo","Quinn","Rafael","Sam","Tomas",
         "Victor","Wesley","Xavier","Yusuf","Zane","Andre","Ben","Chris","Diego","Ethan"]
LAST = ["Alvarez","Brooks","Carter","Dominguez","Ellis","Foster","Gutierrez","Hayes","Ibarra","Jensen",
        "Keller","Lopez","Morales","Nguyen","Ortega","Patel","Quintero","Reyes","Santos","Turner",
        "Underwood","Vargas","Whitaker","Young","Zimmer","Bauer","Costa","Dietrich","Engel","Fischer"]

# Same career-field counts as the real project (109 confirmed careers)
CATEGORIES = {
    "Sales & Business Development": 19,
    "Professional Soccer": 17,
    "Coaching, Performance & Sports Industry": 16,
    "Finance, Accounting & Insurance": 9,
    "Real Estate & Construction": 9,
    "Marketing, Media & Creative": 8,
    "Technology & Engineering": 7,
    "Business, Consulting & Talent": 7,
    "Hospitality, Public Service & Other": 7,
    "Graduate School & Continuing Ed": 4,
    "Entrepreneurs & Owners": 3,
    "Healthcare & Health Sciences": 3,
}
JOBS = {
    "Sales & Business Development": ["Account Executive at Northwind Logistics", "Territory Manager", "Business Development Representative at Brightline", "Sales Consultant"],
    "Professional Soccer": ["Professional Soccer Player", "Professional Footballer at Coastal FC", "Goalkeeper at Metro United"],
    "Coaching, Performance & Sports Industry": ["Youth Academy Coach", "Performance Specialist at Apex Training", "Soccer Agent", "Assistant Coach, Pro Club"],
    "Finance, Accounting & Insurance": ["Staff Accountant at Harbor & Co", "Financial Representative", "Fraud Specialist at First Regional Bank"],
    "Real Estate & Construction": ["Real Estate Agent", "General Contractor", "Licensed Realtor"],
    "Marketing, Media & Creative": ["Digital Marketing Manager", "Freelance Videographer", "Product Marketing Manager"],
    "Technology & Engineering": ["Civil Engineer", "IT Auditor", "Software Developer"],
    "Business, Consulting & Talent": ["Business Analyst", "Recruiting Specialist", "Project Manager at Cobalt Consulting"],
    "Hospitality, Public Service & Other": ["Guest Services Agent", "Firefighter", "Student Pilot"],
    "Graduate School & Continuing Ed": ["Graduate student", "J.D. candidate", "PhD candidate"],
    "Entrepreneurs & Owners": ["Owner and Founder, local business", "Business Owner"],
    "Healthcare & Health Sciences": ["Resident Physician", "Public Health Sanitarian", "Equipment Specialist at Regional Health"],
}
CITIES = ["Tampa","Miami","Orlando","Fort Myers","Naples","Atlanta","Austin","Charlotte","Denver",
          "Brazil","Spain","France","Germany","Canada","Mexico","Costa Rica","Guatemala","New Zealand"]
TERMS = ["Spring","Summer","Fall"]

N, N_CONF, N_REACH = 176, 109, 136
N_EMAIL, N_PHONE, N_LINKEDIN, N_IG = 105, 92, 102, 88

ids = list(range(1, N + 1))
random.shuffle(ids)
reachable = set(ids[:N_REACH])
confirmed = set(random.sample(sorted(reachable), N_CONF))   # every confirmed person is reachable
unreachable = set(ids) - reachable

# Contact methods: sized to the real counts, and every reachable person has at least one
email = set(random.sample(sorted(reachable), N_EMAIL))
need_other = sorted(reachable - email)
phone = set(need_other) | set(random.sample(sorted(email), N_PHONE - len(need_other)))
linkedin = set(random.sample(sorted(reachable), N_LINKEDIN))
instagram = set(random.sample(sorted(reachable), N_IG))
assert (email | phone) >= reachable

# Career fields
cat_list = [c for c, n in CATEGORIES.items() for _ in range(n)]
random.shuffle(cat_list)
cat_of = dict(zip(sorted(confirmed), cat_list))

# Graduation: 109 have a term on record. All 40 unreachable do not.
no_grad = set(unreachable) | set(random.sample(sorted(reachable), 27))
assert len(no_grad) == 67

def messy_phone(i):
    d = f"{random.randint(200,999)}{random.randint(200,999)}{random.randint(1000,9999)}"
    style = random.choice(["plain", "paren", "dash", "intl"])
    if style == "plain": return d
    if style == "paren": return f"({d[:3]}) {d[3:6]}-{d[6:]}"
    if style == "dash":  return f"{d[:3]}-{d[3:6]}-{d[6:]}"
    return f"00+{random.choice(['34','55','49','33'])} {random.randint(600,699)} {random.randint(10,99)} {random.randint(10,99)} {random.randint(10,99)}"

rows, lookup, used = [], [], set()
for i in range(1, N + 1):
    while True:
        name = f"{random.choice(FIRST)} {random.choice(LAST)}"
        if name not in used: used.add(name); break
    slug = name.lower().replace(" ", ".")
    pe = f"{slug}@example.com" if (i in email and random.random() < 0.75) else ""
    se = f"{slug.replace('.', '')[:8]}{random.randint(1000,9999)}@school.example.edu" if (i in email and not pe) or (i in reachable and random.random() < 0.5) else ""
    if i in email and not (pe or se): pe = f"{slug}@example.com"
    # personal-or-school email must exist exactly when i in email
    if i not in email: pe, se = "", ""
    grad = "n/a" if i in no_grad else f"{random.choice(TERMS)} {random.randint(2011, 2026)}"
    uin = "NO MATCH" if random.random() < 0.02 else str(900000000 + random.randint(0, 99999999))
    job = random.choice(JOBS[cat_of[i]]) if i in confirmed else ""
    loc = random.choice(CITIES) if i in confirmed and random.random() > 0.1 else ("?" if i in confirmed else "")
    rows.append([i, name, random.choice(["GK","D","MF","F"]), random.choice(CITIES), grad,
                 random.choice(["Management","Marketing","Finance","Communication","Integrated Studies"]),
                 uin, pe, se,
                 messy_phone(i) if i in phone else "",
                 ("@" if random.random() < .2 else "") + slug.replace(".", "_")[:14] if i in instagram else "",
                 f"https://www.linkedin.com/in/{slug.replace('.', '-')}-{random.randint(10000,99999)}/" if i in linkedin else "",
                 job, loc])
    if i in confirmed: lookup.append([i, name, cat_of[i]])

cols = ["alumni_id","full_name","position","hometown","grad_term","degree_major","uin",
        "personal_email","school_email","phone","instagram","linkedin","job","location"]
with open("data/raw_alumni_synthetic.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(cols); w.writerows(rows)
with open("data/category_lookup_synthetic.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["alumni_id","full_name","category"]); w.writerows(lookup)
print(f"wrote {len(rows)} alumni, {len(lookup)} with a confirmed career")
