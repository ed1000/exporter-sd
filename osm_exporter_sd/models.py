from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Exporter(Base):
    __tablename__ = "exporters"

    id = Column(Integer, primary_key=True, index=True)
    osm_id = Column(String, unique=True, index=True)
    target_url = Column(String, unique=True, index=True)

    labels = relationship("Label", back_populates="exporter")


class Label(Base):
    __tablename__ = "labels"

    id = Column(Integer, primary_key=True, index=True)
    label_key = Column(String, index=True)
    label_value = Column(String, index=True)
    exporter_id = Column(Integer, ForeignKey("exporters.id"))

    exporter = relationship("Exporter", back_populates="labels")
