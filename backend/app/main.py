from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import crud, schemas
from app.logic.grammar import analyze_text
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # или "*" временно за тест
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TextOnly(BaseModel):
    content: str

@app.post("/analyze-and-save", response_model=schemas.TextEntryOut)
async def analyze_and_save(text: TextOnly, db: Session = Depends(get_db)):
    issues = analyze_text(text.content)
    entry = schemas.TextEntryCreate(content=text.content, issues=issues)
    return crud.create_text_entry(db, entry)

@app.get("/entries", response_model=list[schemas.TextEntryOut])
def list_entries(db: Session = Depends(get_db)):
    return crud.get_all_entries(db)
