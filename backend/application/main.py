"""Entrypoint of the application."""

import fastapi
import slowapi
import slowapi.errors
import uvicorn

import db.qdrant_repo
import models.place_payload
import schemas.user_io
import services.limiter
import services.ml
import services.utils

app = fastapi.FastAPI()

app.state.limiter = services.limiter.limiter

app.add_exception_handler(
    slowapi.errors.RateLimitExceeded,
    slowapi._rate_limit_exceeded_handler)


@app.post('/handle')
@services.limiter.limiter.limit('3/second')
def handle_input(
    request: fastapi.Request,
    data: schemas.user_io.UserInput,
) -> schemas.user_io.UserOutput:
    """Endpoint for receiving user input from frontend."""

    embedding: list[float] = services.ml.embedding_model(data.prompt)
    repository: db.qdrant_repo.QdrantRepository = db.qdrant_repo.QdrantRepository()
    places: models.place_payload.PlacePayload = repository.search(embedding)
    route_info: tuple[list[models.place_payload.PlacePayload], int] = services.utils.get_best_route(
        places,
        data.time_for_walk,
        data.latitude,
        data.longitude,
    )
    best_route: list[models.place_payload.PlacePayload] = route_info[0]
    best_time: int = route_info[1]
    # print(best_route)
    # print(len(best_route))
    print(best_time)
    if best_route is not None:
        explanation = services.ml.text_generation_model.get_desc_selection(
            data.prompt,
            best_route,
            )
        print(explanation)
        
        return {
            'walking_time': best_time,
            'walking_path': best_route,
            'explanation': explanation,
        }
                
    
    return schemas.user_io.UserOutput(
        walking_time=None,
        walking_path=[],
        explanation=[
            'There are no places that matches your description.'
            ' Please try to search something else.',
            ],
    )


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
