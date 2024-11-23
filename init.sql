-- Create ENUM types first
CREATE TYPE estado_enum AS ENUM ('nuevo', 'usado');
CREATE TYPE disponibilidad_enum AS ENUM ('disponible', 'no disponible');

-- Create the inventory table if it doesn't exist
CREATE TABLE IF NOT EXISTS inventory (
    id SERIAL PRIMARY KEY,
    marca VARCHAR(50) NOT NULL,
    modelo VARCHAR(50) NOT NULL,
    año INT NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    estado estado_enum NOT NULL,
    disponibilidad disponibilidad_enum NOT NULL
);

-- Insert sample data
INSERT INTO inventory (marca, modelo, año, precio, estado, disponibilidad)
VALUES 
    ('Toyota', 'Corolla', 2021, 20000, 'nuevo', 'disponible'),
    ('Ford', 'Focus', 2019, 15000, 'usado', 'disponible'),
    ('Tesla', 'Model 3', 2023, 40000, 'nuevo', 'disponible')
ON CONFLICT DO NOTHING; -- Prevent duplicate entries if re-run
