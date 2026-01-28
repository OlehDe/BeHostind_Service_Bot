import aiosqlite

DB_HOSTING = "database.db"

async def init_db():
    async with aiosqlite.connect(DB_HOSTING) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            tg_id INTEGER UNIQUE,
            balance REAL DEFAULT 0
        )
        """)
        await db.commit()
