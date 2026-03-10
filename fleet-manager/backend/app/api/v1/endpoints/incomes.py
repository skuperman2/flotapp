from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime
from app.core.database import get_db
from app.models.models import TripIncome, Vehicle, Driver
from app.schemas.schemas import TripIncomeCreate, TripIncomeResponse, TripIncomeUpdate

router = APIRouter()


def calculate_week_number(d: date) -> int:
    return d.isocalendar()[1]


@router.post("/", response_model=TripIncomeResponse, status_code=status.HTTP_201_CREATED)
def create_trip_income(income: TripIncomeCreate, db: Session = Depends(get_db)):
    # Verify vehicle and driver exist
    vehicle = db.query(Vehicle).filter(Vehicle.id == income.vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=400, detail="Vehicle not found")
    
    driver = db.query(Driver).filter(Driver.id == income.driver_id).first()
    if not driver:
        raise HTTPException(status_code=400, detail="Driver not found")
    
    total_income = income.platform_income + income.tips + income.adjustments
    
    db_income = TripIncome(
        **income.model_dump(),
        total_income=total_income,
        week_number=calculate_week_number(income.date),
        month=income.date.month,
        year=income.date.year
    )
    
    db.add(db_income)
    db.commit()
    db.refresh(db_income)
    return db_income


@router.get("/", response_model=List[TripIncomeResponse])
def read_trip_incomes(
    skip: int = 0,
    limit: int = 50,
    vehicle_id: Optional[int] = None,
    driver_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    query = db.query(TripIncome)
    
    if vehicle_id:
        query = query.filter(TripIncome.vehicle_id == vehicle_id)
    if driver_id:
        query = query.filter(TripIncome.driver_id == driver_id)
    if start_date:
        query = query.filter(TripIncome.date >= start_date)
    if end_date:
        query = query.filter(TripIncome.date <= end_date)
    
    incomes = query.order_by(TripIncome.date.desc()).offset(skip).limit(limit).all()
    return incomes


@router.get("/{income_id}", response_model=TripIncomeResponse)
def read_trip_income(income_id: int, db: Session = Depends(get_db)):
    income = db.query(TripIncome).filter(TripIncome.id == income_id).first()
    if income is None:
        raise HTTPException(status_code=404, detail="Income record not found")
    return income


@router.put("/{income_id}", response_model=TripIncomeResponse)
def update_trip_income(income_id: int, income: TripIncomeUpdate, db: Session = Depends(get_db)):
    db_income = db.query(TripIncome).filter(TripIncome.id == income_id).first()
    if db_income is None:
        raise HTTPException(status_code=404, detail="Income record not found")
    
    update_data = income.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_income, field, value)
    
    # Recalculate total_income if any component changed
    db_income.total_income = db_income.platform_income + db_income.tips + db_income.adjustments
    
    db.commit()
    db.refresh(db_income)
    return db_income


@router.delete("/{income_id}")
def delete_trip_income(income_id: int, db: Session = Depends(get_db)):
    db_income = db.query(TripIncome).filter(TripIncome.id == income_id).first()
    if db_income is None:
        raise HTTPException(status_code=404, detail="Income record not found")
    
    db.delete(db_income)
    db.commit()
    return {"message": "Income record deleted successfully"}


@router.get("/summary/monthly")
def get_monthly_summary(
    year: Optional[int] = None,
    month: Optional[int] = None,
    db: Session = Depends(get_db)
):
    if not year:
        year = datetime.now().year
    if not month:
        month = datetime.now().month
    
    incomes = db.query(TripIncome).filter(
        TripIncome.year == year,
        TripIncome.month == month
    ).all()
    
    total_income = sum(i.total_income for i in incomes)
    total_platform = sum(i.platform_income for i in incomes)
    total_tips = sum(i.tips for i in incomes)
    
    # Group by vehicle
    by_vehicle = {}
    for income in incomes:
        if income.vehicle_id not in by_vehicle:
            by_vehicle[income.vehicle_id] = {"total": 0, "count": 0}
        by_vehicle[income.vehicle_id]["total"] += income.total_income
        by_vehicle[income.vehicle_id]["count"] += 1
    
    # Group by driver
    by_driver = {}
    for income in incomes:
        if income.driver_id not in by_driver:
            by_driver[income.driver_id] = {"total": 0, "count": 0}
        by_driver[income.driver_id]["total"] += income.total_income
        by_driver[income.driver_id]["count"] += 1
    
    return {
        "year": year,
        "month": month,
        "total_income": total_income,
        "total_platform_income": total_platform,
        "total_tips": total_tips,
        "records_count": len(incomes),
        "by_vehicle": by_vehicle,
        "by_driver": by_driver
    }
