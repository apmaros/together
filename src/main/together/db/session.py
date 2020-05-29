from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
import logging

from config.db_config import DbConfig, get_db_url

logger = logging.getLogger(__name__)


def get_session(config: DbConfig) -> Session:
    logger.info(f'creating db connection '
                f'database={config.database} '
                f'address={config.host}:{config.port}')

    url = get_db_url(config)
    engine = create_engine(
        url,
        echo=config.echo_queries,
        pool_size=10
    )
    session_class = sessionmaker(bind=engine)
    return session_class()
