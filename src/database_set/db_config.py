from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import MetaData
from sqlalchemy.orm.session import sessionmaker


from src.core.config import database_config


engine = create_async_engine(database_config.async_db_url)
metadata = MetaData()

session_factory: sessionmaker = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
)
