from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import Driver, Vehicle
from app.schemas.schemas import DriverCreate, DriverResponse, DriverUpdate
from datetime import date

router = APIRouter()


@router.post("/", response_model=DriverResponse, status_code=status.HTTP_201_CREATED)
def create_driver(driver: DriverCreate, db: Session = Depends(get_db)):
    db_driver = db.query(Driver).filter(Driver.dni == driver.dni).first()
    if db_driver:
        raise HTTPException(status_code=400, detail="DNI already registered")
    
    # Verify vehicle exists if provided
    if driver.vehicle_id:
        vehicle = db.query(Vehicle).filter(Vehicle.id == driver.vehicle_id).first()
        if not vehicle:
            raise HTTPException(status_code=400, detail="Vehicle not found")
    
    db_driver = Driver(**driver.model_dump())
    db.add(db_driver)
    db.commit()
    db.refresh(db_driver)
    return db_driver


@router.get("/", response_model=List[DriverResponse])
def read_drivers(skip: int = 0, limit: int = 50, status_filter: bool = None, db: Session = Depends(get_db)):
    query = db.query(Driver)
    if status_filter is not None:
        query = query.filter(Driver.status == status_filter)
    drivers = query.offset(skip).limit(limit).all()
    return drivers


@router.get("/{driver_id}", response_model=DriverResponse)
def read_driver(driver_id: int, db: Session = Depends(get_db)):
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if driver is None:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver


@router.put("/{driver_id}", response_model=DriverResponse)
def update_driver(driver_id: int, driver: DriverUpdate, db: Session = Depends(get_db)):
    db_driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if db_driver is None:
        raise HTTPException(status_code=404, detail="Driver not found")
    
    update_data = driver.model_dump(exclude_unset=True)
    
    # Verify vehicle exists if provided
    if "vehicle_id" in update_data and update_data["vehicle_id"]:
        vehicle = db.query(Vehicle).filter(Vehicle.id == update_data["vehicle_id"]).first()
        if not vehicle:
            raise HTTPException(status_code=400, detail="Vehicle not found")
    
    for field, value in update_data.items():
        setattr(db_driver, field, value)
    
    db.commit()
    db.refresh(db_driver)
    return db_driver


@router.delete("/{driver_id}")
def delete_driver(driver_id: int, db: Session = Depends(get_db)):
    db_driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if db_driver is None:
        raise HTTPException(status_code=404, detail="Driver not found")
    
    db.delete(db_driver)
    db.commit()
    return {"message": "Driver deleted successfully"}


@router.get("/{driver_id}/income-history")
def get_driver_income_history(driver_id: int, db: Session = Depends(get_db)):
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if driver is None:
        raise HTTPException(status_code=404, detail="Driver not found")
    
    income_records = driver.income_records
    payments = driver.payments
    
    total_income = sum(record.total_income for record in income_records)
    total_payments = sum(payment.amount for payment in payments)
    
    return {
        "driver": driver,
        "income_records": income_records,
        "payments": payments,
        "total_income": total_income,
        "total_payments": total_payments,
        "balance": total_income - total_payments
    }
