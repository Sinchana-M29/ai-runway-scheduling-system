# Wake turbulence separation rules (minutes)

SEPARATION_MATRIX = {

    ("heavy", "heavy"): 3,
    ("heavy", "medium"): 3,
    ("heavy", "light"): 4,

    ("medium", "heavy"): 2,
    ("medium", "medium"): 2,
    ("medium", "light"): 3,

    ("light", "heavy"): 2,
    ("light", "medium"): 2,
    ("light", "light"): 2

}


def get_separation_time(leading, following):
    """
    Returns minimum separation time between two aircraft
    based on wake turbulence categories.
    """

    return SEPARATION_MATRIX.get((leading, following), 2)
