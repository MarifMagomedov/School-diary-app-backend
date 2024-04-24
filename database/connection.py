from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import load_database_config

config = load_database_config()
url = f'postgresql+asyncpg://{config.db_user}:{config.db_pass}@{config.db_host}:{config.db_port}/{config.db_name}'
engine = create_async_engine(url)
session_factory = async_sessionmaker(engine)

