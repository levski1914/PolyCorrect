from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import crud, schemas
# from app.logic.grammar import check_adj_noun_agreement
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.auth import get_current_user
from app.analyzer.analyze_text import analyze_text
import stanza



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextRequest(BaseModel):
    content: str

@app.post("/analyze")
def analyze(request: TextRequest):
    result = analyze_text(request.content)
    return result
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# class TextOnly(BaseModel):
#     content: str

# @app.post("/analyze-and-save")
# def analyze_and_save(
#     text: TextOnly,
#     db: Session = Depends(get_db),
#     user_id: str = Depends(get_current_user),
# ):
#     doc = nlp(text.content)
#     issues = []
#     issues.extend(check_adj_noun_agreement(doc))

#     for token in doc:
#         print(token.text, token.pos_, token.morph)
#     entry = schemas.TextEntryCreate(content=text.content, issues=issues)
#     return crud.create_text_entry(db, entry, user_id=user_id)

# @app.get("/entries", response_model=list[schemas.TextEntryOut])
# def list_entries(db: Session = Depends(get_db)):
#     return crud.get_all_entries(db)
