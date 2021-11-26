from typing import List
import secrets

from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .settings import settings
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

security = HTTPBasic()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_lcm_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "lcm")
    correct_password = secrets.compare_digest(
        credentials.password, settings.lcm_password
    )
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


def check_prometheus_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "prometheus")
    correct_password = secrets.compare_digest(
        credentials.password, settings.prometheus_password
    )
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.post("/exporters", response_model=schemas.ExporterShow)
async def register_exporter(
    exporter: schemas.ExporterCreate,
    db: Session = Depends(get_db),
    username: str = Depends(check_lcm_credentials),
):
    db_exporter = crud.get_exporter(db=db, exporter_osm_id=exporter.osm_id)
    if db_exporter:
        raise HTTPException(status_code=400, detail="Exporter already exists")
    return crud.create_exporter(db=db, exporter=exporter)


@app.get("/exporters", response_model=List[schemas.ExporterShow])
async def list_exporters(
    db: Session = Depends(get_db), username: str = Depends(check_lcm_credentials)
):
    db_exporters = crud.get_exporters(db=db)
    return db_exporters


@app.get("/exporters/{exporter_osm_id}", response_model=schemas.ExporterShow)
async def get_exporter(
    exporter_osm_id: str,
    db: Session = Depends(get_db),
    username: str = Depends(check_lcm_credentials),
):
    db_exporter = crud.get_exporter(db=db, exporter_osm_id=exporter_osm_id)
    if not db_exporter:
        raise HTTPException(status_code=404, detail="Exporter not found")
    return db_exporter


@app.delete("/exporters/{exporter_osm_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_exporter(
    exporter_osm_id: str,
    db: Session = Depends(get_db),
    username: str = Depends(check_lcm_credentials),
):
    db_exporter = crud.get_exporter(db=db, exporter_osm_id=exporter_osm_id)
    if not db_exporter:
        raise HTTPException(status_code=404, detail="Exporter not found")
    crud.delete_exporter(db=db, exporter_osm_id=exporter_osm_id)


@app.get("/prometheus", response_model=List[schemas.ExporterShow])
async def list_exporters_for_prometheus(
    response: Response,
    db: Session = Depends(get_db),
    username: str = Depends(check_prometheus_credentials),
):
    response.headers["X-Prometheus-Refresh-Interval-Seconds"] = "60"
    db_exporters = crud.get_exporters(db=db)
    return db_exporters
