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

        # Rule 1: Exclude "Senior/Lead" roles immediately
        if matches_any(title, excluded):
            continue

        # Rule 2: Must be Python/Backend/Automation related
        has_primary = matches_any(title, primary)
        
        # Rule 3: Check for Junior/Entry level markers
        has_level = matches_any(title, levels)

        # Logic: It must be a Primary job AND (either it's explicitly Junior OR it doesn't specify Senior)
        # Since we already excluded Senior in Rule 1, we just need to ensure it's a Primary job.
        # We can make it stricter: if they mention 'junior', we definitely want it.
        
        if has_primary:
            filtered.append(job)
        elif has_level:
            # Even if it doesn't say "Python" but says "Junior Backend", we might want it
            filtered.append(job)

    return filtered
