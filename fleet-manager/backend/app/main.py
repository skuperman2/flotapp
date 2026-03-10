from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.api.v1.endpoints import auth, vehicles, drivers, incomes, expenses, maintenance, dashboard

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Fleet Manager API",
    description="API para gestión de flotas de vehículos",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(vehicles.router, prefix="/api/v1/vehicles", tags=["Vehicles"])
app.include_router(drivers.router, prefix="/api/v1/drivers", tags=["Drivers"])
app.include_router(incomes.router, prefix="/api/v1/incomes", tags=["Incomes"])
app.include_router(expenses.router, prefix="/api/v1/expenses", tags=["Expenses"])
app.include_router(maintenance.router, prefix="/api/v1/maintenance", tags=["Maintenance"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["Dashboard"])


@app.get("/")
def read_root():
    return {"message": "Fleet Manager API - Bienvenido", "docs": "/docs"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
