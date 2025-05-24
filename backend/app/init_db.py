from app.database import engine
from app.models import Base

# Това ще създаде всички таблици, дефинирани с Base
Base.metadata.create_all(bind=engine)
