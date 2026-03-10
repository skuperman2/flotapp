#!/bin/bash

# Script de instalación y despliegue local sin Docker

echo "=== Fleet Manager - Instalación Local ==="

# Crear entorno virtual para Python
echo "Creando entorno virtual para backend..."
cd backend
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias de Python
echo "Instalando dependencias de Python..."
pip install -r requirements.txt

# Volver al directorio raíz
cd ..

# Instalar dependencias de Node.js para frontend
echo "Instalando dependencias de Node.js para frontend..."
cd frontend
npm install
cd ..

# Crear archivo .env si no existe
if [ ! -f backend/.env ]; then
    echo "Creando archivo .env para backend..."
    cat > backend/.env << EOF
POSTGRES_USER=fleetuser
POSTGRES_PASSWORD=fleetpass123
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=fleetdb
SECRET_KEY=your-secret-key-change-in-production-2024
EOF
fi

echo ""
echo "=== Instrucciones de Uso ==="
echo ""
echo "1. Asegúrate de tener PostgreSQL instalado y corriendo"
echo "2. Crea la base de datos: createdb fleetdb"
echo "3. Ejecuta el script de inicialización: psql fleetdb < scripts/init_db.sql"
echo "4. Inicia el backend: cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
echo "5. En otra terminal, inicia el frontend: cd frontend && npm start"
echo ""
echo "Accede a:"
echo "  - Frontend: http://localhost:3000"
echo "  - API Docs: http://localhost:8000/docs"
echo ""
echo "Usuarios por defecto:"
echo "  - Admin: admin@fleet.com / admin123"
echo "  - Operador: operator@fleet.com / operator123"
echo ""
