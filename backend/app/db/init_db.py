from app.db.database import engine
from app.db.database import Base

from app.db.models.translation_record import TranslationRecord


def initialize_database():

    Base.metadata.create_all(bind=engine)