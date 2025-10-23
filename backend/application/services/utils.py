import itertools
import pathlib
import pickle

import models.place_payload

MAX_PLACES_COUNT = 5
MAX_SHIFT = 3
COUNT_PLACES = 258
REACHABILITY_MATRIX: list[list[float]] = [
    [0.] * COUNT_PLACES for _ in range(COUNT_PLACES)
]
try:
    file_path = pathlib.Path(
        __file__,
    ).parent.parent.parent / 'open_street_map.pkl'
    with open(file_path, 'rb') as f:
        REACHABILITY_MATRIX = pickle.load(f)
    for row in range(len(REACHABILITY_MATRIX)):
        for col in range(len(REACHABILITY_MATRIX[0])):
            REACHABILITY_MATRIX[row][col] = max(
                0.2,
                REACHABILITY_MATRIX[row][col] // 3600,
            )
except FileNotFoundError:
    print('File not found')
except pickle.UnpicklingError:
    print('Error while attempting to load pkl file')


def get_best_route(
    places: list[models.place_payload.PlacePayload],
    time_for_walk: int,
) -> list[models.place_payload.PlacePayload] | None:
    """Get best route for user."""
    if not places:
        return None

    len_perm = min(MAX_PLACES_COUNT, len(places))
    shift: int = 0
    best_score: int = 0
    best_permutation: list[models.place_payload.PlacePayload] = []
    while shift <= MAX_SHIFT and len_perm - shift >= 0:
        print(shift)
        permutations: itertools.permutations[models.place_payload.PlacePayload] = (
            itertools.permutations(places, len_perm - shift)
            )

        for perm in permutations:
            time_to_pass: int = 0
            perm_score: float = 0
            for i, place in enumerate(perm):
                if i == 0:
                    perm_score += place.score
                    continue
                perm_score += place.score
                time_to_pass += REACHABILITY_MATRIX[perm[i - 1].id][place.id]
            if time_to_pass - 1 > time_for_walk:
                continue
            if perm_score > best_score:
                best_permutation = list(perm)
                best_score = perm_score
        shift += 1
    
    if not best_permutation:
        permutations: itertools.permutations[models.place_payload.PlacePayload] = (
                itertools.permutations(places, 1)
                )
        for perm in permutations:
            time_to_pass: int = 0
            perm_score: float = 0
            for i, place in enumerate(perm):
                if i == 0:
                    perm_score += place.score
                    continue
                perm_score += place.score
                time_to_pass += REACHABILITY_MATRIX[perm[i - 1].id][place.id]
            if time_to_pass - 1 > time_for_walk:
                continue
            if perm_score > best_score:
                best_permutation = list(perm)
                best_score = perm_score

    return best_permutation if best_permutation else None
