from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, date
from enum import Enum


# Enums
class UserRole(str, Enum):
    ADMIN = "admin"
    OPERATOR = "operator"
    ACCOUNTANT = "accountant"


class VehicleStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SOLD = "sold"


class Platform(str, Enum):
    CABIFY = "cabify"
    UBER = "uber"
    BOTH = "both"


class ExpenseType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


class ExpenseCategory(str, Enum):
    PLATFORM_INCOME = "platform_income"
    DRIVER_PAYMENT = "driver_payment"
    FUEL = "fuel"
    MAINTENANCE = "maintenance"
    INSURANCE = "insurance"
    LICENSE = "license"
    CAR_WASH = "car_wash"
    TOLLS = "tolls"
    FINES = "fines"
    OTHER = "other"
    INVESTMENT = "investment"


class DocumentType(str, Enum):
    LICENSE_PLATE = "license_plate"
    INSURANCE = "insurance"
    VTV = "vtv"
    PERMIT = "permit"
    DRIVER_LICENSE = "driver_license"


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole = UserRole.OPERATOR


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None


# Vehicle Schemas
class VehicleBase(BaseModel):
    brand: str
    model: str
    year: int
    license_plate: str
    vin: Optional[str] = None
    color: Optional[str] = None
    purchase_date: Optional[date] = None
    current_mileage: int = 0
    status: VehicleStatus = VehicleStatus.ACTIVE
    platform: Platform = Platform.CABIFY


class VehicleCreate(VehicleBase):
    pass


class VehicleUpdate(BaseModel):
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    license_plate: Optional[str] = None
    vin: Optional[str] = None
    color: Optional[str] = None
    purchase_date: Optional[date] = None
    current_mileage: Optional[int] = None
    status: Optional[VehicleStatus] = None
    platform: Optional[Platform] = None


class VehicleResponse(VehicleBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Driver Schemas
class DriverBase(BaseModel):
    name: str
    dni: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    hire_date: Optional[date] = None
    vehicle_id: Optional[int] = None
    commission_percentage: float = 30.0
    status: bool = True
    notes: Optional[str] = None


class DriverCreate(DriverBase):
    pass


class DriverUpdate(BaseModel):
    name: Optional[str] = None
    dni: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    hire_date: Optional[date] = None
    vehicle_id: Optional[int] = None
    commission_percentage: Optional[float] = None
    status: Optional[bool] = None
    notes: Optional[str] = None


class DriverResponse(DriverBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Trip Income Schemas
class TripIncomeBase(BaseModel):
    date: date
    vehicle_id: int
    driver_id: int
    platform_income: float
    tips: float = 0.0
    adjustments: float = 0.0


class TripIncomeCreate(TripIncomeBase):
    pass


class TripIncomeUpdate(BaseModel):
    date: Optional[date] = None
    vehicle_id: Optional[int] = None
    driver_id: Optional[int] = None
    platform_income: Optional[float] = None
    tips: Optional[float] = None
    adjustments: Optional[float] = None


class TripIncomeResponse(TripIncomeBase):
    id: int
    total_income: float
    week_number: int
    month: int
    year: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Expense Schemas
class ExpenseBase(BaseModel):
    date: date
    vehicle_id: Optional[int] = None
    expense_type: ExpenseType
    category: ExpenseCategory
    amount: float
    description: Optional[str] = None
    receipt_number: Optional[str] = None


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(BaseModel):
    date: Optional[date] = None
    vehicle_id: Optional[int] = None
    expense_type: Optional[ExpenseType] = None
    category: Optional[ExpenseCategory] = None
    amount: Optional[float] = None
    description: Optional[str] = None
    receipt_number: Optional[str] = None


class ExpenseResponse(ExpenseBase):
    id: int
    user_id: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True


# Maintenance Schemas
class MaintenanceBase(BaseModel):
    vehicle_id: int
    date: date
    mileage: Optional[int] = None
    repair_type: str
    mechanic_id: Optional[int] = None
    parts_used: Optional[str] = None
    labor_cost: float = 0.0
    parts_cost: float = 0.0
    notes: Optional[str] = None


class MaintenanceCreate(MaintenanceBase):
    total_cost: float


class MaintenanceUpdate(BaseModel):
    vehicle_id: Optional[int] = None
    date: Optional[date] = None
    mileage: Optional[int] = None
    repair_type: Optional[str] = None
    mechanic_id: Optional[int] = None
    parts_used: Optional[str] = None
    labor_cost: Optional[float] = None
    parts_cost: Optional[float] = None
    total_cost: Optional[float] = None
    notes: Optional[str] = None


class MaintenanceResponse(MaintenanceBase):
    id: int
    total_cost: float
    created_at: datetime
    
    class Config:
        from_attributes = True


# Mechanic Schemas
class MechanicBase(BaseModel):
    name: str
    specialty: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    is_active: bool = True


class MechanicCreate(MechanicBase):
    pass


class MechanicUpdate(BaseModel):
    name: Optional[str] = None
    specialty: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    is_active: Optional[bool] = None


class MechanicResponse(MechanicBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Supplier Schemas
class SupplierBase(BaseModel):
    name: str
    contact: Optional[str] = None
    parts_type: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: bool = True


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    contact: Optional[str] = None
    parts_type: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None


class SupplierResponse(SupplierBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Investment Schemas
class InvestmentBase(BaseModel):
    vehicle_id: int
    date: date
    investment_type: str
    supplier_id: Optional[int] = None
    amount: float
    payment_method: Optional[str] = None
    notes: Optional[str] = None


class InvestmentCreate(InvestmentBase):
    pass


class InvestmentUpdate(BaseModel):
    vehicle_id: Optional[int] = None
    date: Optional[date] = None
    investment_type: Optional[str] = None
    supplier_id: Optional[int] = None
    amount: Optional[float] = None
    payment_method: Optional[str] = None
    notes: Optional[str] = None


class InvestmentResponse(InvestmentBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Document Schemas
class DocumentBase(BaseModel):
    vehicle_id: Optional[int] = None
    driver_id: Optional[int] = None
    document_type: DocumentType
    issue_date: Optional[date] = None
    expiry_date: date
    notes: Optional[str] = None


class DocumentCreate(DocumentBase):
    pass


class DocumentUpdate(BaseModel):
    vehicle_id: Optional[int] = None
    driver_id: Optional[int] = None
    document_type: Optional[DocumentType] = None
    issue_date: Optional[date] = None
    expiry_date: Optional[date] = None
    is_renewed: Optional[bool] = None
    notes: Optional[str] = None


class DocumentResponse(DocumentBase):
    id: int
    is_renewed: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# Driver Payment Schemas
class DriverPaymentBase(BaseModel):
    driver_id: int
    payment_date: date
    amount: float
    period_start: Optional[date] = None
    period_end: Optional[date] = None
    notes: Optional[str] = None


class DriverPaymentCreate(DriverPaymentBase):
    pass


class DriverPaymentUpdate(BaseModel):
    driver_id: Optional[int] = None
    payment_date: Optional[date] = None
    amount: Optional[float] = None
    period_start: Optional[date] = None
    period_end: Optional[date] = None
    notes: Optional[str] = None


class DriverPaymentResponse(DriverPaymentBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Dashboard Schemas
class DashboardStats(BaseModel):
    total_income: float = 0.0
    total_expenses: float = 0.0
    net_profit: float = 0.0
    active_vehicles: int = 0
    total_vehicles: int = 0
    active_drivers: int = 0


class VehicleProfitability(BaseModel):
    vehicle_id: int
    license_plate: str
    total_income: float
    total_expenses: float
    net_profit: float


class DriverProductivity(BaseModel):
    driver_id: int
    driver_name: str
    total_income: float
    trips_count: int
