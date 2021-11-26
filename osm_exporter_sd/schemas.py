from typing import Dict, List
from pydantic import BaseModel


class LabelBase(BaseModel):
    label_key: str
    label_value: str


class Label(LabelBase):
    id: int
    exporter_id: int

    class Config:
        orm_mode = True


class ExporterBase(BaseModel):
    target_url: str


class ExporterCreate(ExporterBase):
    osm_id: str
    labels: Dict[str, str] = {}


class ExporterShow(ExporterCreate):
    pass


class ExporterPrometheusShow(BaseModel):
    targets: List[str]
    labels: Dict[str, str] = {}


class Exporter(ExporterBase):
    id: int
    labels: List[Label] = []

    class Config:
        orm_mode = True
