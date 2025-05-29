from sqlalchemy.orm import Session
from . import models, schemas

def create_text_entry(db: Session, entry: schemas.TextEntryCreate, user_id: str):
    db_entry = models.TextEntry(
        content=entry.content,
        issues=entry.issues,
        user_id=user_id
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

def get_all_entries(db: Session):
    return db.query(models.TextEntry).all()
