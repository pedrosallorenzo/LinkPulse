from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Link

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/add")
def add_link(url: str, db: Session = Depends(get_db)):
    link = Link(url=url, status="Checking")
    db.add(link)
    db.commit()
    db.refresh(link)
    return {"message": "Link adicionado"}

@router.get("/status")
def get_links(db: Session = Depends(get_db)):
    return db.query(Link).all()