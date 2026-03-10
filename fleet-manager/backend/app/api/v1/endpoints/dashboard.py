from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.core.database import get_db
from app.models.models import DashboardStats, VehicleProfitability, DriverProductivity
from app.models.models import Vehicle, Driver, TripIncome, Expense, ExpenseType, VehicleStatus
from datetime import datetime

router = APIRouter()


@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    # Current month
    current_year = datetime.now().year
    current_month = datetime.now().month
    
    # Total vehicles
    total_vehicles = db.query(Vehicle).count()
    active_vehicles = db.query(Vehicle).filter(Vehicle.status == VehicleStatus.ACTIVE).count()
    
    # Active drivers
    active_drivers = db.query(Driver).filter(Driver.status == True).count()
    
    # Monthly income
    monthly_incomes = db.query(TripIncome).filter(
        TripIncome.year == current_year,
        TripIncome.month == current_month
    ).all()
    total_income = sum(i.total_income for i in monthly_incomes)
    
    # Monthly expenses
    monthly_expenses = db.query(Expense).filter(
        Expense.date >= date(current_year, current_month, 1),
        Expense.expense_type == ExpenseType.EXPENSE
    ).all()
    total_expenses = sum(e.amount for e in monthly_expenses)
    
    net_profit = total_income - total_expenses
    
    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_profit": net_profit,
        "active_vehicles": active_vehicles,
        "total_vehicles": total_vehicles,
        "active_drivers": active_drivers,
        "period": {"year": current_year, "month": current_month}
    }


@router.get("/vehicle-profitability")
def get_vehicle_profitability(
    year: Optional[int] = None,
    month: Optional[int] = None,
    db: Session = Depends(get_db)
):
    if not year:
        year = datetime.now().year
    if not month:
        month = datetime.now().month
    
    vehicles = db.query(Vehicle).filter(Vehicle.status == VehicleStatus.ACTIVE).all()
    profitability_list = []
    
    for vehicle in vehicles:
        # Get income for this vehicle
        incomes = db.query(TripIncome).filter(
            TripIncome.vehicle_id == vehicle.id,
            TripIncome.year == year,
            TripIncome.month == month
        ).all()
        total_income = sum(i.total_income for i in incomes)
        
        # Get expenses for this vehicle
        expenses = db.query(Expense).filter(
            Expense.vehicle_id == vehicle.id,
            Expense.date >= date(year, month, 1),
            Expense.date <= date(year, month, 31),
            Expense.expense_type == ExpenseType.EXPENSE
        ).all()
        total_expenses = sum(e.amount for e in expenses)
        
        profitability_list.append({
            "vehicle_id": vehicle.id,
            "license_plate": vehicle.license_plate,
            "total_income": total_income,
            "total_expenses": total_expenses,
            "net_profit": total_income - total_expenses
        })
    
    # Sort by net profit
    profitability_list.sort(key=lambda x: x["net_profit"], reverse=True)
    
    return profitability_list


@router.get("/driver-productivity")
def get_driver_productivity(
    year: Optional[int] = None,
    month: Optional[int] = None,
    db: Session = Depends(get_db)
):
    if not year:
        year = datetime.now().year
    if not month:
        month = datetime.now().month
    
    drivers = db.query(Driver).filter(Driver.status == True).all()
    productivity_list = []
    
    for driver in drivers:
        incomes = db.query(TripIncome).filter(
            TripIncome.driver_id == driver.id,
            TripIncome.year == year,
            TripIncome.month == month
        ).all()
        
        total_income = sum(i.total_income for i in incomes)
        
        productivity_list.append({
            "driver_id": driver.id,
            "driver_name": driver.name,
            "total_income": total_income,
            "trips_count": len(incomes)
        })
    
    # Sort by total income
    productivity_list.sort(key=lambda x: x["total_income"], reverse=True)
    
    return productivity_list


@router.get("/monthly-trend")
def get_monthly_trend(year: Optional[int] = None, db: Session = Depends(get_db)):
    if not year:
        year = datetime.now().year
    
    monthly_data = []
    
    for month in range(1, 13):
        incomes = db.query(TripIncome).filter(
            TripIncome.year == year,
            TripIncome.month == month
        ).all()
        
        expenses = db.query(Expense).filter(
            Expense.date >= date(year, month, 1),
            Expense.date <= date(year, month, 31) if month < 12 else date(year, 12, 31),
            Expense.expense_type == ExpenseType.EXPENSE
        ).all()
        
        total_income = sum(i.total_income for i in incomes)
        total_expenses = sum(e.amount for e in expenses)
        
        monthly_data.append({
            "month": month,
            "income": total_income,
            "expenses": total_expenses,
            "profit": total_income - total_expenses
        })
    
    return {"year": year, "data": monthly_data}


@router.get("/expiring-documents")
def get_expiring_documents(days_ahead: int = 30, db: Session = Depends(get_db)):
    from app.models.models import Document
    from datetime import timedelta
    
    today = date.today()
    threshold = today + timedelta(days=days_ahead)
    
    expiring = db.query(Document).filter(
        Document.expiry_date <= threshold,
        Document.expiry_date >= today,
        Document.is_renewed == False
    ).all()
    
    expired = db.query(Document).filter(
        Document.expiry_date < today,
        Document.is_renewed == False
    ).all()
    
    return {
        "expiring_soon": [
            {
                "id": d.id,
                "type": d.document_type.value,
                "expiry_date": d.expiry_date,
                "vehicle_id": d.vehicle_id,
                "driver_id": d.driver_id
            } for d in expiring
        ],
        "expired": [
            {
                "id": d.id,
                "type": d.document_type.value,
                "expiry_date": d.expiry_date,
                "vehicle_id": d.vehicle_id,
                "driver_id": d.driver_id
            } for d in expired
        ]
    }
