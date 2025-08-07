from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Trajectory
from fastapi import Depends
from typing import List
from pydantic import BaseModel
import time
import os
import uvicorn

# --- Initialize database ---
Base.metadata.create_all(bind=engine)
class TrajectorySchema(BaseModel):
    id: int
    x: int
    y: int
    step: int

    class Config:
        orm_mode = True

# --- Setup FastAPI ---
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- Routes ---

@app.get("/test")
def test():
    return {"message": "Hello from FastAPI WallPilot"}

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/plan")
def plan_coverage(
    request: Request,
    wall_width: int = Form(...),
    wall_height: int = Form(...),
    obs_x: int = Form(...),
    obs_y: int = Form(...),
    obs_w: int = Form(...),
    obs_h: int = Form(...)
):
    start = time.time()
    path = []

    for y in range(wall_height):
        for x in range(wall_width):
            if obs_x <= x < obs_x + obs_w and obs_y <= y < obs_y + obs_h:
                continue
            path.append((x, y))

    db: Session = SessionLocal()
    for idx, (x, y) in enumerate(path):
        db.add(Trajectory(x=x, y=y, step=idx))
    db.commit()
    db.close()

    elapsed = round(time.time() - start, 3)
    return {"steps": len(path), "time": elapsed}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/trajectory", response_model=List[TrajectorySchema])
def get_trajectories(db: Session = Depends(get_db)):
    trajectories = db.query(Trajectory).order_by(Trajectory.step).all()
    return trajectories


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Render sets PORT
    uvicorn.run("main:app", host="0.0.0.0", port=port)