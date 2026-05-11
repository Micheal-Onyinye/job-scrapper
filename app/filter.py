from config import PRIMARY_KEYWORDS, LEVEL_KEYWORDS, EXCLUDED_KEYWORDS

def normalize(text):
    return text.lower().strip()

def matches_any(title, keyword_list):
    title = normalize(title)
    # Check if any keyword in the list is a substring of the title
    for keyword in keyword_list:
        if keyword in title:
            return True
    return False

def filter_jobs(jobs, keywords_ignored=None):
    """
    Filters jobs based on specific rules:
    1. Must contain a PRIMARY keyword (python, backend, automation).
    2. Must NOT contain an EXCLUDED keyword (senior, lead, etc.).
    3. If LEVEL keywords exist, prioritize them (optional but recommended).
    """
    filtered = []
    
    primary = [normalize(k) for k in PRIMARY_KEYWORDS]
    levels = [normalize(k) for k in LEVEL_KEYWORDS]
    excluded = [normalize(k) for k in EXCLUDED_KEYWORDS]

    for job in jobs:
        title = normalize(job["title"])

        if matches_any(title, excluded):
            continue

        has_primary = matches_any(title, primary)
        
        has_level = matches_any(title, levels)


        
        if has_primary:
            filtered.append(job)
        elif has_level:
            filtered.append(job)

    return filtered
