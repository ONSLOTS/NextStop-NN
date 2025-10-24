import itertools
import math
import pathlib
import pickle

import pandas as pd

import models.place_payload

MAX_PLACES_COUNT = 5
MAX_SHIFT = 4
COUNT_PLACES = 258
REACHABILITY_MATRIX: list[list[float]] = [
    [0.] * COUNT_PLACES for _ in range(COUNT_PLACES)
]
VISITING_TIMINGS = [0] * COUNT_PLACES
BACKEND_ROOT = pathlib.Path(
        __file__,
    ).parent.parent.parent

try:
    reachability_path = BACKEND_ROOT / 'open_street_map.pkl'
    with open(reachability_path, 'rb') as f:
        REACHABILITY_MATRIX = pickle.load(f)
    for row in range(len(REACHABILITY_MATRIX)):
        for col in range(len(REACHABILITY_MATRIX[0])):
            REACHABILITY_MATRIX[row][col] //= 60
except FileNotFoundError:
    print('File not found')
except pickle.UnpicklingError:
    print('Error while attempting to load pkl file')

BACKEND_ROOT = pathlib.Path(__file__).parent.parent.parent
try:
    visiting_timings_path = BACKEND_ROOT / 'visiting_time.csv'
    
    df = pd.read_csv(visiting_timings_path, header=None, names=['data'], sep=';')
    last_values = df['data'].apply(lambda x: x.split(',')[-1] if isinstance(x, str) else x)
    VISITING_TIMINGS = [[int(value)] for value in last_values[1:]]

    
except FileNotFoundError:
    print('File not found')


def simple_manhattan_distance(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
    ) -> float:

    lat_km = abs(lat2 - lat1) * 111
    lon_km = abs(lon2 - lon1) * 111 * math.cos(math.radians((lat1 + lat2) / 2))
    
    return (lat_km + lon_km) * 1000 // 100


def get_best_route(
    places: list[models.place_payload.PlacePayload],
    time_for_walk: int,
    lat: float,
    lon: float,
) -> list[models.place_payload.PlacePayload] | None:
    """Get best route for user."""
    if not places:
        return None
    
    time_for_walk *= 60
    len_perm = min(MAX_PLACES_COUNT, len(places))
    shift: int = 0
    best_score: int = 0
    best_permutation: list[models.place_payload.PlacePayload] = []
    while shift <= MAX_SHIFT and len_perm - shift >= 0:
        permutations: itertools.permutations[models.place_payload.PlacePayload] = (
            itertools.permutations(places, len_perm - shift)
            )

        for perm in permutations:
            time_to_pass: int = 0
            perm_score: float = 0
            for i, place in enumerate(perm):
                perm_score += place.score
                time_to_pass += VISITING_TIMINGS[place.id][0]
                if i == 0:
                    time_to_reach_first_place = simple_manhattan_distance(
                        lat, 
                        lon, 
                        place.latitude, 
                        place.longitude,
                        )
                    time_to_pass += time_to_reach_first_place
                    continue
                time_to_pass += REACHABILITY_MATRIX[perm[i - 1].id][place.id]
            if time_to_pass - 60 > time_for_walk:
                continue

            if perm_score > best_score:
                best_permutation = list(perm)
                best_score = perm_score
        shift += 1
    

    return best_permutation if best_permutation else None
