import sqlite3
import os
from datetime import datetime, timedelta


class MealDatabase:
    """Database for meals, ingredients and feedback provided by the user."""

    def __init__(self, db_path: str = "data/meals.db"):
        """Initialize MealDatabase."""
        self.db_path = db_path
        self.conn = None
        self._connect()
        self._ensure_table_exists()

    def _connect(self):
        """Establish database connection."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # Return rows as dicts

    def _ensure_table_exists(self):
        """Create meals table if it doesn't exist."""
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS meals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ingredients TEXT NOT NULL,
                meal TEXT NOT NULL,
                recipe TEXT NOT NULL,
                date TIMESTAMP NOT NULL,
                feedback TEXT
            )
        """
        )
        self.conn.commit()

    def get_meals_from_days_back(self, days_back: int = 14) -> list[str]:
        """
        Get meal names from the last N days.

        Args:
            days_back: Number of days to look back

        Returns:
            List of meal names
        """
        date_threshold = datetime.now() - timedelta(days=days_back)

        cursor = self.conn.execute(
            "SELECT meal_name FROM meals WHERE date > ?", (date_threshold.isoformat(),)
        )

        # Return just the meal names
        return [row[0] for row in cursor.fetchall()]

    def add_meal(self, ingredients: str, meal: str, recipe: str, date: datetime) -> int:
        """
        Add a meal to the database.

        Args:
            ingredients: Comma-separated string of ingredients
            meal: Name or description of the meal
            recipe: Recipe or instructions for the meal
            date: Datetime object

        Returns:
            ID of the inserted meal
        """
        cursor = self.conn.execute(
            "INSERT INTO meals (ingredients, meal, recipe, date) VALUES (?, ?, ?, ?)",
            (ingredients, meal, recipe, date.isoformat()),
        )
        self.conn.commit()

        return cursor.lastrowid

    def update_meal_feedback(self, meal_id: int, feedback: str) -> None:
        """
        Update feedback for a meal.

        Args:
            meal_id: ID of the meal
            feedback: Feedback text
        """
        self.conn.execute(
            "UPDATE meals SET feedback = ? WHERE id = ?", (feedback, meal_id)
        )
        self.conn.commit()

    def get_meal_by_name(self, meal_name: str) -> dict:
        """
        Retrieve a meal record by its name.

        Args:
            meal_name: Name of the meal to retrieve

        Returns:
            Meal record as a dictionary
        """
        cursor = self.conn.execute("SELECT * FROM meals WHERE meal = ?", (meal_name,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
