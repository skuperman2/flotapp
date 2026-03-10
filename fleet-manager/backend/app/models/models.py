from app.core.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Float, Date, Text
from sqlalchemy.orm import relationship
import enum
from datetime import datetime


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    OPERATOR = "operator"
    ACCOUNTANT = "accountant"


class VehicleStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SOLD = "sold"


class Platform(str, enum.Enum):
    CABIFY = "cabify"
    UBER = "uber"
    BOTH = "both"


class ExpenseType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"


class ExpenseCategory(str, enum.Enum):
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


class DocumentType(str, enum.Enum):
    LICENSE_PLATE = "license_plate"
    INSURANCE = "insurance"
    VTV = "vtv"
    PERMIT = "permit"
    DRIVER_LICENSE = "driver_license"


# Tabla de Usuarios
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.OPERATOR)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    expenses = relationship("Expense", back_populates="user")


# Tabla de Vehículos
class Vehicle(Base):
    __tablename__ = "vehicles"
    
    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    license_plate = Column(String, unique=True, index=True, nullable=False)
    vin = Column(String, unique=True)
    color = Column(String)
    purchase_date = Column(Date)
    current_mileage = Column(Integer, default=0)
    status = Column(Enum(VehicleStatus), default=VehicleStatus.ACTIVE)
    platform = Column(Enum(Platform), default=Platform.CABIFY)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    driver = relationship("Driver", back_populates="vehicle", uselist=False)
    income_records = relationship("TripIncome", back_populates="vehicle")
    expenses = relationship("Expense", back_populates="vehicle")
    maintenance_records = relationship("Maintenance", back_populates="vehicle")
    investments = relationship("Investment", back_populates="vehicle")
    documents = relationship("Document", back_populates="vehicle")


# Tabla de Conductores
class Driver(Base):
    __tablename__ = "drivers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    dni = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String)
    email = Column(String)
    address = Column(String)
    hire_date = Column(Date)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=True)
    commission_percentage = Column(Float, default=30.0)
    status = Column(Boolean, default=True)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    vehicle = relationship("Vehicle", back_populates="driver")
    income_records = relationship("TripIncome", back_populates="driver")
    payments = relationship("DriverPayment", back_populates="driver")


# Tabla de Ingresos por Viajes
class TripIncome(Base):
    __tablename__ = "trip_income"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=False)
    platform_income = Column(Float, nullable=False)
    tips = Column(Float, default=0.0)
    adjustments = Column(Float, default=0.0)
    total_income = Column(Float, nullable=False)
    week_number = Column(Integer)
    month = Column(Integer)
    year = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    vehicle = relationship("Vehicle", back_populates="income_records")
    driver = relationship("Driver", back_populates="income_records")


# Tabla de Gastos e Ingresos de Caja
class Expense(Base):
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=True)
    expense_type = Column(Enum(ExpenseType), nullable=False)
    category = Column(Enum(ExpenseCategory), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(Text)
    receipt_number = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    vehicle = relationship("Vehicle", back_populates="expenses")
    user = relationship("User", back_populates="expenses")


# Tabla de Mantenimiento
class Maintenance(Base):
    __tablename__ = "maintenance"
    
    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    date = Column(Date, nullable=False)
    mileage = Column(Integer)
    repair_type = Column(String, nullable=False)
    mechanic_id = Column(Integer, ForeignKey("mechanics.id"))
    parts_used = Column(Text)
    labor_cost = Column(Float, default=0.0)
    parts_cost = Column(Float, default=0.0)
    total_cost = Column(Float, nullable=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    vehicle = relationship("Vehicle", back_populates="maintenance_records")
    mechanic = relationship("Mechanic", back_populates="maintenance_records")


# Tabla de Mecánicos
class Mechanic(Base):
    __tablename__ = "mechanics"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    specialty = Column(String)
    phone = Column(String)
    address = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    maintenance_records = relationship("Maintenance", back_populates="mechanic")


# Tabla de Proveedores de Repuestos
class Supplier(Base):
    __tablename__ = "suppliers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    contact = Column(String)
    parts_type = Column(String)
    phone = Column(String)
    email = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


# Tabla de Inversiones
class Investment(Base):
    __tablename__ = "investments"
    
    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    date = Column(Date, nullable=False)
    investment_type = Column(String, nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    amount = Column(Float, nullable=False)
    payment_method = Column(String)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    vehicle = relationship("Vehicle", back_populates="investments")
    supplier = relationship("Supplier")


# Tabla de Documentos y Vencimientos
class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=True)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=True)
    document_type = Column(Enum(DocumentType), nullable=False)
    issue_date = Column(Date)
    expiry_date = Column(Date, nullable=False)
    is_renewed = Column(Boolean, default=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    vehicle = relationship("Vehicle", back_populates="documents")
    driver = relationship("Driver")


# Tabla de Pagos a Conductores
class DriverPayment(Base):
    __tablename__ = "driver_payments"
    
    id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=False)
    payment_date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)
    period_start = Column(Date)
    period_end = Column(Date)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    driver = relationship("Driver", back_populates="payments")
