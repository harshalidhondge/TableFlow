import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("bffeddbafa9ed3da1f67f383e939b34e3a3caf9b6ce6912fce02f07091417c30", "tableflow_secret_key")

    DATABASE_URL = os.getenv("postgresql://tableflow_db_s4rz_user:WhhPvVzNeD2mtY1tsHOggjNgfWj0PJyS@dpg-d9rkfuv10e5c7389rft0-a/tableflow_db_s4rz")

    if DATABASE_URL:
        DATABASE_URL = DATABASE_URL.replace(
            "postgres://", "postgresql://", 1
        )

    SQLALCHEMY_DATABASE_URI = DATABASE_URL

    SQLALCHEMY_TRACK_MODIFICATIONS = False
