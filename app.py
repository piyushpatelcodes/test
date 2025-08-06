from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

import uvicorn

# --- Setup FastAPI ---
app = FastAPI()

# --- Setup DB ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}"

engine = create_engine(DB_PATH, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- DB Model ---
class Person(Base):
    __tablename__ = "people"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

Base.metadata.create_all(bind=engine)

# --- HTML Templates ---
templates = Jinja2Templates(directory="templates")

# --- Route ---
@app.get("/test")
def root():
    return {"message": "Hello from FastAPI on Render! piyushpatelcodes"}

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    db = SessionLocal()
    
    # Seed DB if empty
    if db.query(Person).count() == 0:
        db.add_all([Person(name="Alice"), Person(name="Bob"), Person(name="Charlie")])
        db.commit()

    people = db.query(Person).all()
    return templates.TemplateResponse("index.html", {"request": request, "people": people})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Render sets PORT
    uvicorn.run("main:app", host="0.0.0.0", port=port)