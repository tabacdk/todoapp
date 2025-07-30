import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session, init_db
from app.models.user import User
from app.models.todo import Todo
from app.security import hash_password

async def insert_fixtures():
    await init_db()
    async with get_session() as session:
        user1 = User(
            username="alice",
            hashed_password=hash_password("alice123"),  # eller "plain_password" hvis ikke implementeret endnu
        )
        user2 = User(
            username="bob",
            hashed_password=hash_password("bob123"),
        )

        session.add_all([user1, user2])
        await session.flush()  # for at få user1.id og user2.id

        # Todos
        todo1 = Todo(title="Buy milk", description="Stop by market and pick up milk", user_id=user1.id)
        todo2 = Todo(title="Mow lawn", description="Do before 5 PM", completed=True, user_id=user1.id)
        todo3 = Todo(title="Call Mom", description="Ask about Christmas plans", user_id=user2.id)

        session.add_all([todo1, todo2, todo3])

        await session.commit()
        print("Fixtures inserted ✅")

if __name__ == "__main__":
    asyncio.run(insert_fixtures())
