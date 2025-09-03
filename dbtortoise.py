from tortoise.contrib.fastapi import register_tortoise

def init_db(app):
    register_tortoise(
        app,
        db_url="sqlite://db.sqlite3",  # or asyncpg://user:pass@localhost:5432/dbname
        modules={"models": ["modelstortoise"]},  # our models live in models.py
        generate_schemas=True,  # auto-generate tables
        add_exception_handlers=True,
    )

