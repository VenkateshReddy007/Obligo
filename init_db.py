"""Create all database tables from SQLAlchemy models."""
import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'services', 'api')))

from database import Base, engine

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("All database tables created successfully.")
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(init_db())
