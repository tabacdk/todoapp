from uvicorn import run
from fastapi import FastAPI
from app.v1 import user, todo  # importer modulerne
from app.database import lifespan


app = FastAPI(lifespan=lifespan)

# Routere til /v1/user og /v1/todo
app.include_router(user.router, prefix="/v1/user", tags=["user"])
app.include_router(todo.router, prefix="/v1/todo", tags=["todo"])


def main():
    run(app, host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()
