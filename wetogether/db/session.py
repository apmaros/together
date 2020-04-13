from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.db_config import DbConfig, get_db_url
import logging

logger = logging.getLogger(__name__)


def get_session(config: DbConfig):
    logger.info(f'creating db connection '
                f'database={config.database} '
                f'address={config.host}:{config.port}')

    url = get_db_url(config)
    engine = create_engine(url, echo=True, pool_size=10)
    Session = sessionmaker(bind=engine)
    return Session()
