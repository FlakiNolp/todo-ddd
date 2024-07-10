import asyncio

from infrastructure.repositories.models import Base
from infrastructure.repositories.base_sqlalchemy_repository import (
    BaseSQLAlchemyRepository,
)
from src.configs.config import ConfigSettings


async def create_schema():
    config = ConfigSettings()
    print(config)
    async with BaseSQLAlchemyRepository(
            _db_host=config.db_host,
            _db_port=config.db_port,
            _db_username=config.db_username,
            _db_password=config.db_password,
            _db_database=config.db_database,
    ).async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(create_schema())
