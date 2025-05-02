import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings

from app.db.base_class import Base
from app.models.part import Part

try:
    # Create the SQLAlchemy engine
    engine = create_engine(
        settings.DATABASE_URL, connect_args={"check_same_thread": False}
    )
    with engine.connect() as conn:
        logging.info("Conexão com o banco de dados estabelecida com sucesso")
except SQLAlchemyError as e:
    logging.error(f"Erro de conexão com o banco de dados: {str(e)}")

# The connect_args parameter is needed only for SQLite. For other databases like PostgreSQL, remove it.

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class
Base = declarative_base()
