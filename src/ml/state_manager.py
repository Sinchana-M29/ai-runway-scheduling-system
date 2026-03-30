def initialize_state():
    return {
        "runway_available_time": {
            "R1": 0,
            "R2": 0
        },
        "last_runway_time": {
            "R1": 0,
            "R2": 0
        },
        "queue": []
    }

def update_runway_state(state, runway, actual_time):
    state["runway_available_time"][runway] = actual_time
    state["last_runway_time"][runway] = actual_time
    return state