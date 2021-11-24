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
    osm_id: str
    target_url: str


class ExporterCreate(ExporterBase):
    labels: Dict[str, str] = {}


class ExporterShow(ExporterCreate):
    pass


class Exporter(ExporterBase):
    id: int
    labels: List[Label] = []

    class Config:
        orm_mode = True
