-- Enable extensions
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;
CREATE EXTENSION IF NOT EXISTS vector;
-- CREATE EXTENSION IF NOT EXISTS vectorscale CASCADE;

-- Create meals table
CREATE TABLE IF NOT EXISTS meals (
    id SERIAL PRIMARY KEY,
    ingredients TEXT NOT NULL,
    meal_name TEXT NOT NULL,  -- Your preferred naming
    recipe TEXT,
    date TIMESTAMP NOT NULL,
    feedback TEXT,
    meal_plan_id INTEGER,
    day_number INTEGER,
    accepted BOOLEAN DEFAULT FALSE
);

-- Create recipes table with vector embeddings
CREATE TABLE IF NOT EXISTS recipes (
    id UUID PRIMARY KEY,
    metadata JSONB,  -- Changed from TEXT to JSONB for timescale compatibility
    contents TEXT NOT NULL,
    embedding vector(1536),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for vector similarity search
CREATE INDEX IF NOT EXISTS recipes_embedding_idx ON recipes USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);


-- Create meal_plans table
CREATE TABLE IF NOT EXISTS meal_plans (
    id SERIAL PRIMARY KEY,
    name TEXT,
    num_days INTEGER NOT NULL,
    num_people INTEGER NOT NULL,
    dietary_preferences TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add foreign key constraint
ALTER TABLE meals ADD CONSTRAINT fk_meal_plan 
    FOREIGN KEY (meal_plan_id) REFERENCES meal_plans(id) ON DELETE CASCADE;