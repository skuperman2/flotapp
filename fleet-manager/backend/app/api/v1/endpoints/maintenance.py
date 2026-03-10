from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.core.database import get_db
from app.models.models import Maintenance, Mechanic, Vehicle
from app.schemas.schemas import MaintenanceCreate, MaintenanceResponse, MaintenanceUpdate, MechanicCreate, MechanicResponse, MechanicUpdate

router = APIRouter()


# Maintenance endpoints
@router.post("/maintenance", response_model=MaintenanceResponse, status_code=status.HTTP_201_CREATED)
def create_maintenance(maintenance: MaintenanceCreate, db: Session = Depends(get_db)):
    vehicle = db.query(Vehicle).filter(Vehicle.id == maintenance.vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=400, detail="Vehicle not found")
    
    db_maintenance = Maintenance(**maintenance.model_dump())
    db.add(db_maintenance)
    db.commit()
    db.refresh(db_maintenance)
    return db_maintenance


@router.get("/maintenance", response_model=List[MaintenanceResponse])
def read_maintenance_records(
    skip: int = 0,
    limit: int = 50,
    vehicle_id: Optional[int] = None,
    mechanic_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Maintenance)
    
    if vehicle_id:
        query = query.filter(Maintenance.vehicle_id == vehicle_id)
    if mechanic_id:
        query = query.filter(Maintenance.mechanic_id == mechanic_id)
    if start_date:
        query = query.filter(Maintenance.date >= start_date)
    if end_date:
        query = query.filter(Maintenance.date <= end_date)
    
    records = query.order_by(Maintenance.date.desc()).offset(skip).limit(limit).all()
    return records


@router.get("/maintenance/{record_id}", response_model=MaintenanceResponse)
def read_maintenance(record_id: int, db: Session = Depends(get_db)):
    record = db.query(Maintenance).filter(Maintenance.id == record_id).first()
    if record is None:
        raise HTTPException(status_code=404, detail="Maintenance record not found")
    return record


@router.put("/maintenance/{record_id}", response_model=MaintenanceResponse)
def update_maintenance(record_id: int, maintenance: MaintenanceUpdate, db: Session = Depends(get_db)):
    db_record = db.query(Maintenance).filter(Maintenance.id == record_id).first()
    if db_record is None:
        raise HTTPException(status_code=404, detail="Maintenance record not found")
    
    update_data = maintenance.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_record, field, value)
    
    db.commit()
    db.refresh(db_record)
    return db_record


@router.delete("/maintenance/{record_id}")
def delete_maintenance(record_id: int, db: Session = Depends(get_db)):
    db_record = db.query(Maintenance).filter(Maintenance.id == record_id).first()
    if db_record is None:
        raise HTTPException(status_code=404, detail="Maintenance record not found")
    
    db.delete(db_record)
    db.commit()
    return {"message": "Maintenance record deleted successfully"}


# Mechanic endpoints
@router.post("/mechanics", response_model=MechanicResponse, status_code=status.HTTP_201_CREATED)
def create_mechanic(mechanic: MechanicCreate, db: Session = Depends(get_db)):
    db_mechanic = Mechanic(**mechanic.model_dump())
    db.add(db_mechanic)
    db.commit()
    db.refresh(db_mechanic)
    return db_mechanic


@router.get("/mechanics", response_model=List[MechanicResponse])
def read_mechanics(skip: int = 0, limit: int = 50, active_only: bool = True, db: Session = Depends(get_db)):
    query = db.query(Mechanic)
    if active_only:
        query = query.filter(Mechanic.is_active == True)
    mechanics = query.offset(skip).limit(limit).all()
    return mechanics


@router.get("/mechanics/{mechanic_id}", response_model=MechanicResponse)
def read_mechanic(mechanic_id: int, db: Session = Depends(get_db)):
    mechanic = db.query(Mechanic).filter(Mechanic.id == mechanic_id).first()
    if mechanic is None:
        raise HTTPException(status_code=404, detail="Mechanic not found")
    return mechanic


@router.put("/mechanics/{mechanic_id}", response_model=MechanicResponse)
def update_mechanic(mechanic_id: int, mechanic: MechanicUpdate, db: Session = Depends(get_db)):
    db_mechanic = db.query(Mechanic).filter(Mechanic.id == mechanic_id).first()
    if db_mechanic is None:
        raise HTTPException(status_code=404, detail="Mechanic not found")
    
    update_data = mechanic.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_mechanic, field, value)
    
    db.commit()
    db.refresh(db_mechanic)
    return db_mechanic


@router.delete("/mechanics/{mechanic_id}")
def delete_mechanic(mechanic_id: int, db: Session = Depends(get_db)):
    db_mechanic = db.query(Mechanic).filter(Mechanic.id == mechanic_id).first()
    if db_mechanic is None:
        raise HTTPException(status_code=404, detail="Mechanic not found")
    
    db.delete(db_mechanic)
    db.commit()
    return {"message": "Mechanic deleted successfully"}
