from sqlalchemy.orm import Session

from . import models, schemas


def _transform_exporter(exporter: models.Exporter):
    labels = {label.label_key: label.label_value for label in exporter.labels}
    return schemas.ExporterShow(
        osm_id=exporter.osm_id, target_url=exporter.target_url, labels=labels
    )


def get_exporter(db: Session, exporter_osm_id: str):
    db_exporter = (
        db.query(models.Exporter)
        .filter(models.Exporter.osm_id == exporter_osm_id)
        .first()
    )
    return _transform_exporter(db_exporter) if db_exporter else db_exporter


def get_exporters(db: Session):
    db_exporters = db.query(models.Exporter).all()
    return [_transform_exporter(exporter) for exporter in db_exporters]


def create_exporter(db: Session, exporter: schemas.ExporterCreate):
    # add exporter to db
    db_exporter = models.Exporter(
        osm_id=exporter.osm_id, target_url=exporter.target_url
    )
    db.add(db_exporter)
    db.commit()
    db.refresh(db_exporter)

    # add labels to db
    for label_key, label_value in exporter.labels.items():
        db_label = models.Label(
            label_key=label_key, label_value=label_value, exporter_id=db_exporter.id
        )
        db.add(db_label)
        db.commit()

    # refresh exporter and return
    db.refresh(db_exporter)
    return _transform_exporter(db_exporter)


def delete_exporter(db: Session, exporter_osm_id: str):
    return (
        db.query(models.Exporter)
        .filter(models.Exporter.osm_id == exporter_osm_id)
        .delete()
    )
