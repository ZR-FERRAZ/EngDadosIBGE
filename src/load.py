import os
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient
from sqlalchemy import create_engine

load_dotenv(override=True)


class Load:
    def load_mongo(self, data, db_name, collection_name):
        """Bronze: dado cru, como veio da API."""
        client = MongoClient(os.getenv("MONGO_URI"))
        try:
            col = client[db_name][collection_name]
            col.delete_many({})  # recarga completa: rodar de novo não duplica
            col.insert_many(data)
        finally:
            client.close()

    def load_sqlite(self, df, table="pnadc"):
        """Silver local (réplica em SQLite)."""
        path = os.getenv("SQLITE_PATH", "data/pnadc.db")
        Path(path).parent.mkdir(parents=True, exist_ok=True)

        engine = create_engine(f"sqlite:///{path}")
        try:
            df.to_sql(table, engine, if_exists="replace", index=False)
        finally:
            engine.dispose()

    def load_neon(self, df, table="pnadc"):
        """Silver na nuvem (Postgres)."""
        engine = create_engine(os.getenv("NEON_URL"))
        try:
            df.to_sql(table, engine, if_exists="replace", index=False)
        finally:
            engine.dispose()