from contextlib import asynccontextmanager
from uvicorn import run
from fastapi import FastAPI
from app.v1 import user, todo  # importer modulerne
from app.database import init_db, get_session

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    try:
        yield
    finally:
        # Forsøg at commit og lukke session, hvis der er en åben
        async with get_session() as session:
            try:
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

app = FastAPI(lifespan=lifespan)

# Routere til /v1/user og /v1/todo
app.include_router(user.router, prefix="/v1/user", tags=["user"])
app.include_router(todo.router, prefix="/v1/todo", tags=["todo"])


def main():
    run(app, host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()
