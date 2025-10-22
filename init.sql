-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS vectorscale CASCADE;

-- Create meals table
CREATE TABLE IF NOT EXISTS meals (
    id SERIAL PRIMARY KEY,
    ingredients TEXT NOT NULL,
    meal_name TEXT NOT NULL,
    recipe TEXT,
    date TIMESTAMP NOT NULL,
    feedback TEXT
);

-- Create recipes table with vector embeddings
CREATE TABLE IF NOT EXISTS recipes (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    ingredients TEXT NOT NULL,
    directions TEXT NOT NULL,
    link TEXT,
    source TEXT,
    ner TEXT,
    site TEXT,
    embedding vector(384),  -- 384 dimensions for sentence-transformers/all-MiniLM-L6-v2
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for vector similarity search
CREATE INDEX IF NOT EXISTS recipes_embedding_idx ON recipes USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Create index for faster lookups
CREATE INDEX IF NOT EXISTS recipes_title_idx ON recipes(title);
CREATE INDEX IF NOT EXISTS meals_date_idx ON meals(date);

-- Add meal_plans table
CREATE TABLE IF NOT EXISTS meal_plans (
    id SERIAL PRIMARY KEY,
    meal_name TEXT,
    num_days INTEGER NOT NULL,
    num_people INTEGER NOT NULL,
    dietary_preferences TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Link meals to meal plans
ALTER TABLE meals ADD COLUMN IF NOT EXISTS meal_plan_id INTEGER REFERENCES meal_plans(id);
ALTER TABLE meals ADD COLUMN IF NOT EXISTS day_number INTEGER;
ALTER TABLE meals ADD COLUMN IF NOT EXISTS accepted BOOLEAN DEFAULT FALSE;