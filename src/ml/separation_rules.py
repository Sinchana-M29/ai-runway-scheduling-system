SEPARATION_RULES = {
    ("Heavy", "Light"): 240,
    ("Medium", "Light"): 156,
    ("Heavy", "Medium"): 180,
    ("Heavy", "Heavy"): 180,
    ("Medium", "Medium"): 120,
    ("Light", "Light"): 90
}

def get_separation_time(leading, following):
    return SEPARATION_RULES.get((leading, following), 120)