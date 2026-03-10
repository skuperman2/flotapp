from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime
from app.core.database import get_db
from app.models.models import Expense, ExpenseType, ExpenseCategory, Vehicle
from app.schemas.schemas import ExpenseCreate, ExpenseResponse, ExpenseUpdate

router = APIRouter()


@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    # Verify vehicle exists if provided
    if expense.vehicle_id:
        vehicle = db.query(Vehicle).filter(Vehicle.id == expense.vehicle_id).first()
        if not vehicle:
            raise HTTPException(status_code=400, detail="Vehicle not found")
    
    db_expense = Expense(**expense.model_dump())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


@router.get("/", response_model=List[ExpenseResponse])
def read_expenses(
    skip: int = 0,
    limit: int = 50,
    expense_type: Optional[ExpenseType] = None,
    category: Optional[ExpenseCategory] = None,
    vehicle_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Expense)
    
    if expense_type:
        query = query.filter(Expense.expense_type == expense_type)
    if category:
        query = query.filter(Expense.category == category)
    if vehicle_id:
        query = query.filter(Expense.vehicle_id == vehicle_id)
    if start_date:
        query = query.filter(Expense.date >= start_date)
    if end_date:
        query = query.filter(Expense.date <= end_date)
    
    expenses = query.order_by(Expense.date.desc()).offset(skip).limit(limit).all()
    return expenses


@router.get("/{expense_id}", response_model=ExpenseResponse)
def read_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(expense_id: int, expense: ExpenseUpdate, db: Session = Depends(get_db)):
    db_expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    update_data = expense.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_expense, field, value)
    
    db.commit()
    db.refresh(db_expense)
    return db_expense


@router.delete("/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    db_expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    db.delete(db_expense)
    db.commit()
    return {"message": "Expense deleted successfully"}


@router.get("/summary/cashflow")
def get_cashflow_summary(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    if not start_date:
        start_date = date(datetime.now().year, datetime.now().month, 1)
    if not end_date:
        end_date = date.today()
    
    incomes = db.query(Expense).filter(
        Expense.expense_type == ExpenseType.INCOME,
        Expense.date >= start_date,
        Expense.date <= end_date
    ).all()
    
    expenses_list = db.query(Expense).filter(
        Expense.expense_type == ExpenseType.EXPENSE,
        Expense.date >= start_date,
        Expense.date <= end_date
    ).all()
    
    total_income = sum(e.amount for e in incomes)
    total_expenses = sum(e.amount for e in expenses_list)
    
    # Group expenses by category
    by_category = {}
    for expense in expenses_list:
        cat = expense.category.value
        if cat not in by_category:
            by_category[cat] = 0
        by_category[cat] += expense.amount
    
    # Group expenses by vehicle
    by_vehicle = {}
    for expense in expenses_list:
        if expense.vehicle_id:
            if expense.vehicle_id not in by_vehicle:
                by_vehicle[expense.vehicle_id] = 0
            by_vehicle[expense.vehicle_id] += expense.amount
    
    return {
        "period": {"start": start_date, "end": end_date},
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_balance": total_income - total_expenses,
        "by_category": by_category,
        "by_vehicle": by_vehicle
    }
