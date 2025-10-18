"""Entrypoint of the application."""

import itertools

import fastapi
import uvicorn

import db.qdrant_repo
import models.place_payload
import schemas.user_io
import services.ml

MAX_PLACES_COUNT = 5
MAX_SHIFT = 3

app = fastapi.FastAPI()


@app.post('/handle')
def handle_input(
    data: schemas.user_io.UserInput,
    )-> schemas.user_io.UserOutput:
    """Endpoint for receiving user input from frontend."""

    embedding: list[float] = services.ml.embedding_model(data.prompt)
    best_route: list[models.place_payload.PlacePayload] | None = (
        get_best_route(embedding, data.time_for_walk)
        )
    print(best_route)
    print(len(best_route))
    
    if best_route is not None:
        explanation = services.ml.text_generation_model.get_desc_selection(
            data.prompt, best_route,
            )
        print(explanation)
        
        return {
            'walking_time': data.time_for_walk + 1,
            'walking_path': best_route,
            'explanation': explanation,
        }
                
    
    return ValueError(
        'There are no places that matches your description. Please try to search something else.',
        )
    
def get_best_route(
    embedding: list[float],
    time_for_walk: int,
    ) -> list[models.place_payload.PlacePayload] | None:
    """Get best route for user."""
    repository: db.qdrant_repo.QdrantRepository = db.qdrant_repo.QdrantRepository()
    places: models.place_payload.PlacePayload = repository.search(embedding)

    if places:
        len_perm = min(MAX_PLACES_COUNT, len(places))
        shift: int = 0
        best_score: int = 0
        best_permutation: list[models.place_payload.PlacePayload] = []
        while shift <= MAX_SHIFT and len_perm - shift >= 0:
            print(shift)
            time_to_pass: int = len_perm - shift
            permutations: itertools.permutations[models.place_payload.PlacePayload] = (
                itertools.permutations(places, len_perm - shift)
                )
            
            for perm in permutations:
                if time_to_pass - 1 > time_for_walk:
                    continue
                perm_score = sum(item.score for item in perm)
                if perm_score > best_score:
                    best_permutation = perm[:]
                    best_score = perm_score
            shift += 1
        
        if not best_permutation:
            permutations: itertools.permutations[models.place_payload.PlacePayload] = (
                    itertools.permutations(places, 1)
                    )
            for perm in permutations:
                    if time_to_pass - 1 > time_for_walk:
                        continue
                    perm_score = sum(item.score for item in perm)
                    if perm_score > best_score:
                        best_permutation = perm[:]
                        best_score = perm_score
        return best_permutation if best_permutation else None
        
    return None
    


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
