"""Entrypoint of the application."""

import fastapi
import uvicorn

import schemas.user_input


app = fastapi.FastAPI()

mocked_bd = []


@app.post('/handle')
def handle_input(data: schemas.user_input.UserInput) -> dict:
    """Endpoint for receiving user input from frontend."""
    mocked_bd.append(data)
    
    return {
        'prompt': data.prompt,
        'time_for_walk': data.time_for_walk,
        'latitude': data.latitude,
        'longitude': data.longitude,
    }
    
    


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
