from typing import List

from fastapi import Depends, FastAPI, HTTPException, Response
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/exporters/", response_model=schemas.ExporterShow)
async def register_exporter(
    exporter: schemas.ExporterCreate, db: Session = Depends(get_db)
):
    db_exporter = crud.get_exporter(db=db, exporter_osm_id=exporter.osm_id)
    if db_exporter:
        raise HTTPException(status_code=400, detail="Exporter already exists")
    return crud.create_exporter(db=db, exporter=exporter)


@app.get("/exporters/", response_model=List[schemas.ExporterShow])
async def list_exporters(db: Session = Depends(get_db)):
    db_exporters = crud.get_exporters(db=db)
    return db_exporters


@app.get("/exporters/{exporter_osm_id}", response_model=schemas.ExporterShow)
async def get_exporter(exporter_osm_id: str, db: Session = Depends(get_db)):
    db_exporter = crud.get_exporter(db=db, exporter_osm_id=exporter_osm_id)
    if not db_exporter:
        raise HTTPException(status_code=404, detail="Exporter not found")
    return db_exporter


@app.patch("/exporters/{exporter_osm_id}")
async def update_exporter(exporter_osm_id: str, db: Session = Depends(get_db)):
    return {}


@app.delete("/exporters/{exporter_osm_id}")
async def delete_exporter(exporter_osm_id: str, db: Session = Depends(get_db)):
    return {}


@app.get("/prometheus/", response_model=List[schemas.ExporterShow])
async def list_exporters_for_prometheus(
    response: Response, db: Session = Depends(get_db)
):
    response.headers["X-Prometheus-Refresh-Interval-Seconds"] = "60"
    db_exporters = crud.get_exporters(db=db)
    return db_exporters
