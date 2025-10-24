"""Entrypoint of the application."""

import fastapi
import uvicorn

import db.qdrant_repo
import models.place_payload
import schemas.user_io
import services.ml
import services.utils

MAX_PLACES_COUNT = 5
MAX_SHIFT = 3

app = fastapi.FastAPI()


@app.post('/handle')
def handle_input(
    data: schemas.user_io.UserInput,
) -> schemas.user_io.UserOutput:
    """Endpoint for receiving user input from frontend."""

    embedding: list[float] = services.ml.embedding_model(data.prompt)
    repository: db.qdrant_repo.QdrantRepository = db.qdrant_repo.QdrantRepository()
    places: models.place_payload.PlacePayload = repository.search(embedding)
    best_route: list[models.place_payload.PlacePayload] | None = services.utils.get_best_route(
        places,
        data.time_for_walk,
        data.latitude,
        data.longitude,
    )
    print(best_route)
    print(len(best_route))
    if best_route is not None:
        explanation = services.ml.text_generation_model.get_desc_selection(
            data.prompt,
            best_route,
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


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
