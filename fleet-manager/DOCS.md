# Fleet Manager - Documentación del Proyecto

## 1. Arquitectura del Sistema

### Visión General
Fleet Manager es un sistema ERP para gestión de flotas de vehículos que trabajan en plataformas de transporte (Cabify, Uber). La arquitectura sigue un diseño moderno basado en microservicios modulares.

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Frontend      │────▶│   Backend API    │────▶│   PostgreSQL    │
│   React +       │     │   FastAPI        │     │   Database      │
│   Tailwind      │◀────│   REST           │◀────│                 │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

### Stack Tecnológico
- **Backend**: Python 3.10+ con FastAPI
- **Frontend**: React 18 con Tailwind CSS
- **Base de Datos**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0
- **Autenticación**: JWT (JSON Web Tokens)
- **Despliegue**: Docker + Docker Compose

## 2. Modelo de Base de Datos

### Tablas Principales

#### users
- id, email, hashed_password, full_name, role, is_active, created_at

#### vehicles
- id, brand, model, year, license_plate, vin, color, purchase_date, 
  current_mileage, status, platform, created_at, updated_at

#### drivers
- id, name, dni, phone, email, address, hire_date, vehicle_id, 
  commission_percentage, status, notes, created_at

#### trip_income
- id, date, vehicle_id, driver_id, platform_income, tips, adjustments,
  total_income, week_number, month, year, created_at

#### expenses
- id, date, vehicle_id, expense_type, category, amount, description,
  receipt_number, user_id, created_at

#### maintenance
- id, vehicle_id, date, mileage, repair_type, mechanic_id, parts_used,
  labor_cost, parts_cost, total_cost, notes, created_at

#### mechanics
- id, name, specialty, phone, address, is_active, created_at

#### suppliers
- id, name, contact, parts_type, phone, email, is_active, created_at

#### investments
- id, vehicle_id, date, investment_type, supplier_id, amount,
  payment_method, notes, created_at

#### documents
- id, vehicle_id, driver_id, document_type, issue_date, expiry_date,
  is_renewed, notes, created_at

#### driver_payments
- id, driver_id, payment_date, amount, period_start, period_end,
  notes, created_at

## 3. API Endpoints

### Autenticación
- `POST /api/v1/auth/register` - Registrar nuevo usuario
- `POST /api/v1/auth/login` - Iniciar sesión
- `GET /api/v1/auth/me` - Obtener usuario actual

### Vehículos
- `GET /api/v1/vehicles` - Listar vehículos
- `POST /api/v1/vehicles` - Crear vehículo
- `GET /api/v1/vehicles/{id}` - Obtener vehículo
- `PUT /api/v1/vehicles/{id}` - Actualizar vehículo
- `DELETE /api/v1/vehicles/{id}` - Eliminar vehículo
- `GET /api/v1/vehicles/{id}/history` - Historial completo

### Conductores
- `GET /api/v1/drivers` - Listar conductores
- `POST /api/v1/drivers` - Crear conductor
- `GET /api/v1/drivers/{id}` - Obtener conductor
- `PUT /api/v1/drivers/{id}` - Actualizar conductor
- `DELETE /api/v1/drivers/{id}` - Eliminar conductor
- `GET /api/v1/drivers/{id}/income-history` - Historial de ingresos

### Ingresos
- `GET /api/v1/incomes` - Listar ingresos
- `POST /api/v1/incomes` - Registrar ingreso
- `GET /api/v1/incomes/{id}` - Obtener ingreso
- `PUT /api/v1/incomes/{id}` - Actualizar ingreso
- `DELETE /api/v1/incomes/{id}` - Eliminar ingreso
- `GET /api/v1/incomes/summary/monthly` - Resumen mensual

### Gastos
- `GET /api/v1/expenses` - Listar gastos
- `POST /api/v1/expenses` - Registrar gasto
- `GET /api/v1/expenses/{id}` - Obtener gasto
- `PUT /api/v1/expenses/{id}` - Actualizar gasto
- `DELETE /api/v1/expenses/{id}` - Eliminar gasto
- `GET /api/v1/expenses/summary/cashflow` - Flujo de caja

### Mantenimiento
- `GET /api/v1/maintenance/maintenance` - Listar mantenimientos
- `POST /api/v1/maintenance/maintenance` - Registrar mantenimiento
- `GET /api/v1/maintenance/mechanics` - Listar mecánicos
- `POST /api/v1/maintenance/mechanics` - Crear mecánico

### Dashboard
- `GET /api/v1/dashboard/stats` - Estadísticas generales
- `GET /api/v1/dashboard/vehicle-profitability` - Rentabilidad por vehículo
- `GET /api/v1/dashboard/driver-productivity` - Productividad por conductor
- `GET /api/v1/dashboard/monthly-trend` - Tendencia mensual
- `GET /api/v1/dashboard/expiring-documents` - Documentos por vencer

## 4. Estructura de Carpetas

```
fleet-manager/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       └── endpoints/
│   │   │           ├── auth.py
│   │   │           ├── vehicles.py
│   │   │           ├── drivers.py
│   │   │           ├── incomes.py
│   │   │           ├── expenses.py
│   │   │           ├── maintenance.py
│   │   │           └── dashboard.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   └── security.py
│   │   ├── models/
│   │   │   └── models.py
│   │   ├── schemas/
│   │   │   └── schemas.py
│   │   └── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   └── Sidebar.js
│   │   ├── pages/
│   │   │   ├── Login.js
│   │   │   ├── Dashboard.js
│   │   │   ├── Vehicles.js
│   │   │   ├── Drivers.js
│   │   │   ├── Incomes.js
│   │   │   ├── Expenses.js
│   │   │   └── Maintenance.js
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   └── Dockerfile
├── scripts/
│   ├── init_db.sql
│   └── install.sh
├── docker-compose.yml
└── README.md
```

## 5. Instalación y Despliegue

### Opción A: Docker (Recomendado)

```bash
cd fleet-manager
docker-compose up --build
```

Acceder a:
- Frontend: http://localhost:3000
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Opción B: Local

```bash
# Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (otra terminal)
cd frontend
npm install
npm start
```

## 6. Roles de Usuario

### Administrador (admin)
- Acceso completo a todos los módulos
- Gestión de usuarios
- Configuración del sistema

### Operador (operator)
- Alta, edición y baja de vehículos
- Gestión de conductores
- Registro de ingresos y gastos
- Mantenimiento

### Contador (accountant)
- Acceso a módulos financieros
- Reportes y estadísticas
- Exportación de datos

## 7. Usuarios por Defecto

| Email | Contraseña | Rol |
|-------|-----------|-----|
| admin@fleet.com | admin123 | Administrador |
| operator@fleet.com | operator123 | Operador |
| accountant@fleet.com | accountant123 | Contador |

## 8. Características Principales

### Módulo de Vehículos
- Registro completo de información vehicular
- Historial de mantenimiento
- Asignación de conductores
- Estados: activo, inactivo, vendido

### Módulo de Conductores
- Información personal y laboral
- Comisión configurable
- Historial de ingresos
- Evaluaciones y observaciones

### Módulo de Productividad
- Registro diario de ingresos
- Agrupación por semana/mes
- Rankings de conductores
- Rentabilidad por vehículo

### Módulo de Caja
- Ingresos y egresos categorizados
- Flujo de caja mensual
- Balance general
- Gastos por vehículo

### Módulo de Mecánica
- Registro de reparaciones
- Catálogo de mecánicos
- Proveedores de repuestos
- Costos detallados

### Módulo de Documentos
- Control de vencimientos
- Alertas automáticas
- Tipos: patente, seguro, VTV, licencias

### Dashboard
- KPIs en tiempo real
- Gráficos de tendencias
- Alertas de documentos
- Top vehículos/conductores

## 9. Seguridad

- Autenticación JWT
- Hash de contraseñas con bcrypt
- Roles y permisos
- CORS configurado
- Validación de datos con Pydantic

## 10. Próximas Mejoras

1. Importación desde Excel
2. Exportación a PDF/Excel
3. Integración con APIs de Cabify/Uber
4. Notificaciones email/SMS
5. Control de kilometraje automático
6. Registro de combustible
7. Control de turnos
8. Multi-tenant para múltiples flotas

## 11. Soporte

Para reportar problemas o solicitar características:
- Revisar logs en contenedores Docker
- Verificar conexión a base de datos
- Consultar documentación de API en /docs

---

**Versión**: 1.0.0 MVP  
**Licencia**: Propietaria  
**Año**: 2024
