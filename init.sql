-- Create ENUM types first
CREATE TYPE state_enum AS ENUM ('new', 'used');
CREATE TYPE availability_enum AS ENUM ('available', 'not available');

-- Create the inventory table if it doesn't exist
CREATE TABLE IF NOT EXISTS inventory (
    id SERIAL PRIMARY KEY,
    make VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    year INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    state state_enum NOT NULL,
    availability availability_enum NOT NULL
);

-- Insert sample data
INSERT INTO inventory (make, model, year, price, state, availability)
VALUES 
    ('Toyota', 'Corolla', 2021, 20000, 'new', 'available'),
    ('Ford', 'Focus', 2019, 15000, 'used', 'available'),
    ('Tesla', 'Model 3', 2023, 40000, 'new', 'available'),
    ('Honda', 'Civic', 2022, 25000, 'new', 'available'),
    ('Chevrolet', 'Malibu', 2020, 22000, 'used', 'available'),
    ('BMW', '3 Series', 2021, 35000, 'new', 'available'),
    ('Audi', 'A4', 2022, 38000, 'new', 'available'),
    ('Mercedes-Benz', 'C-Class', 2020, 42000, 'used', 'available'),
    ('Nissan', 'Altima', 2018, 14000, 'used', 'available'),
    ('Hyundai', 'Elantra', 2023, 28000, 'new', 'available')
ON CONFLICT DO NOTHING; -- Prevent duplicate entries if re-run
