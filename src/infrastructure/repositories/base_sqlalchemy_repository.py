import abc
from dataclasses import dataclass
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncEngine, create_async_engine
from sqlalchemy import URL


@dataclass
class BaseSQLAlchemyRepository(abc.ABC):
    _db_host: str
    _db_port: int
    _db_username: str
    _db_password: str
    _db_database: str

    def __post_init__(self):
        self._async_engine: AsyncEngine = create_async_engine(
            URL.create(
                drivername="postgresql+asyncpg",
                host=self._db_host,
                port=self._db_port,
                username=self._db_username,
                password=self._db_password,
                database=self._db_database,
            )
        )
        self._async_session_maker = async_sessionmaker(
            self._async_engine, expire_on_commit=False
        )

    @property
    def async_engine(self):
        return self._async_engine
