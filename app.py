from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

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
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    db = SessionLocal()
    
    # Seed DB if empty
    if db.query(Person).count() == 0:
        db.add_all([Person(name="Alice"), Person(name="Bob"), Person(name="Charlie")])
        db.commit()

    people = db.query(Person).all()
    return templates.TemplateResponse("index.html", {"request": request, "people": people})
