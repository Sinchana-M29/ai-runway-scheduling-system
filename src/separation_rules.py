def get_separation_time(prev_wake, current_wake):

    rules = {
        ("Heavy", "Heavy"): 3,
        ("Heavy", "Medium"): 4,
        ("Medium", "Heavy"): 3,
        ("Medium", "Medium"): 2
    }

    return rules.get((prev_wake, current_wake), 2)


def weather_separation_adjustment(weather):

    weather_rules = {
        "clear": 0,
        "rain": 1,
        "storm": 2,
        "fog": 1
    }

    return weather_rules.get(weather, 0)


def runway_occupancy_time(aircraft_type):

    occupancy = {
        "A320": 2,
        "A321": 2,
        "A319": 2,
        "B737": 2,
        "B787": 3,
        "B777": 3,
        "A350": 3,
        "A330": 3
    }

    return occupancy.get(aircraft_type, 2)
