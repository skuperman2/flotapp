-- Script de inicialización de la base de datos
-- Crea usuarios por defecto para el sistema

-- Usuario Administrador
INSERT INTO users (email, hashed_password, full_name, role, is_active, created_at)
VALUES (
    'admin@fleet.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzS3MebAJu', -- admin123
    'Administrador del Sistema',
    'admin',
    true,
    NOW()
) ON CONFLICT (email) DO NOTHING;

-- Usuario Operador
INSERT INTO users (email, hashed_password, full_name, role, is_active, created_at)
VALUES (
    'operator@fleet.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzS3MebAJu', -- operator123
    'Operador de Flota',
    'operator',
    true,
    NOW()
) ON CONFLICT (email) DO NOTHING;

-- Usuario Contador
INSERT INTO users (email, hashed_password, full_name, role, is_active, created_at)
VALUES (
    'accountant@fleet.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzS3MebAJu', -- accountant123
    'Contador',
    'accountant',
    true,
    NOW()
) ON CONFLICT (email) DO NOTHING;

-- Datos de ejemplo - Mecánicos
INSERT INTO mechanics (name, specialty, phone, address, is_active, created_at)
VALUES 
    ('Taller Central', 'General', '555-0100', 'Av. Principal 123', true, NOW()),
    ('Juan Pérez', 'Motor', '555-0101', 'Calle Secundaria 456', true, NOW())
ON CONFLICT DO NOTHING;

-- Datos de ejemplo - Proveedores
INSERT INTO suppliers (name, contact, parts_type, phone, email, is_active, created_at)
VALUES 
    ('Repuestos SA', 'Carlos Gómez', 'General', '555-0200', 'ventas@repuestos.sa', true, NOW()),
    ('AutoParts', 'María López', 'Especializados', '555-0201', 'info@autoparts.com', true, NOW())
ON CONFLICT DO NOTHING;
