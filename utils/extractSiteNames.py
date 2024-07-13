import re

site_names = [
    "Aldgate",
    "Birmingham",
    "Bournemouth",
    "Canterbury",
    "Cardiff",
    "Chelmsford",
    "Ealing",
    "Edinburgh",
    "Exeter",
    "Glasgow",
    "Lakeside",
    "Leeds",
    "Liverpool",
    "Manchester",
    "Norwich",
    "Oxford Street",
    "Plymouth",
    "Southend",
    "Swindon",
    "The O2",
    "Wandsworth",
    "Watford",
    "Gifting",
    "St Patricks Day",
]


def extract_site_names(text, site_names):
    matched_site_names = []
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if "From" in line:
            for j in range(i-1, -1, -1):
                if any(keyword.lower() in lines[j].lower() for keyword in ["boom", "post"]):
                    for site in site_names:
                        if site.lower() in lines[j].lower():
                            amount = re.search(r'£(\d+\.\d{2})', lines[i]).group(1)
                            matched_site_names.append((site, amount))
                            break
                    break
    return matched_site_names