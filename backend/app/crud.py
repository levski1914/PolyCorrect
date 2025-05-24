from sqlalchemy.orm import Session
from . import models, schemas

def create_text_entry(db: Session, entry: schemas.TextEntryCreate):
    db_entry = models.TextEntry(
        content=entry.content,
        issues=[issue.dict() for issue in entry.issues]
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

def get_all_entries(db: Session):
    return db.query(models.TextEntry).all()
