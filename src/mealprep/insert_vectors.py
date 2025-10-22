from datetime import datetime

import pandas as pd
from db.vector_store import VectorStore
from timescale_vector.client import uuid_from_time
from pathlib import Path

# Initialize VectorStore
vec = VectorStore()

# Read the CSV file

# Get the project root (two levels up from this file)
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "recipes_data.csv"
df = pd.read_csv(DATA_PATH)


# Prepare data for insertion
def prepare_record(row):
    """
    Prepare a single record for insertion into the vector store.
    Args:
        row: A row from the DataFrame
    Returns:
        A dictionary with id, metadata, contents, and embedding
    """
    content = f"Title: {row["title"]}\nIngredients: {row['ingredients']}\nRecipe: {row['directions']}"
    embedding = vec.get_embedding(content)
    return pd.Series(
        {
            "id": str(uuid_from_time(datetime.now())),
            "metadata": {
                "created_at": datetime.now().isoformat(),
            },
            "contents": content,
            "embedding": embedding,
        }
    )


records_df = df.sample(n=100).apply(prepare_record, axis=1)


# Create tables and insert data
vec.create_tables()
vec.create_index()  # DiskAnnIndex
vec.upsert(records_df)
