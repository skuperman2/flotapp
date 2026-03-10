# Fleet Manager - Sistema de Gestión de Flotas

## Descripción
Sistema ERP para gestión de flotas de vehículos que trabajan en plataformas de transporte como Cabify/Uber.

## Arquitectura
- **Backend**: Python + FastAPI
- **Base de Datos**: PostgreSQL
- **Frontend**: React + Tailwind CSS
- **Autenticación**: JWT
- **ORM**: SQLAlchemy
- **Despliegue**: Docker

## Módulos
1. Vehículos
2. Conductores
3. Productividad
4. Caja de la Flota
5. Mecánica y Repuestos
6. Gastos de Inversión
7. Impuestos y Documentación
8. Dashboard General
9. Roles de Usuario

## Instalación

### Prerrequisitos
- Docker y Docker Compose
- Node.js 18+
- Python 3.10+

### Ejecución con Docker
```bash
docker-compose up --build
```

Acceder a:
- Frontend: http://localhost:3000
- API: http://localhost:8000
- Docs API: http://localhost:8000/docs

## Estructura del Proyecto
```
fleet-manager/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   └── services/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── context/
│   ├── package.json
│   └── Dockerfile
├── scripts/
│   └── init_db.sql
├── docker-compose.yml
└── README.md
```

## Usuarios por Defecto
- Admin: admin@fleet.com / admin123
- Operador: operator@fleet.com / operator123
- Contador: accountant@fleet.com / accountant123
