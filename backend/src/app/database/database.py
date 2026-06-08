from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.models import Base

DATABASE_URL = "sqlite:///./data/history.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """
    Crea las tablas en la base de datos si no existen.
    Se llama al arrancar el servidor.
    """
    Base.metadata.create_all(bind=engine)


def get_db():
    """
    Generador que provee una sesión de BD por request.
    FastAPI la inyecta automáticamente con Depends(get_db).
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()