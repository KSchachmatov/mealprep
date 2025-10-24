import os
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta
from typing import Optional
from mealprep.config.settings import get_db_url


class MealDatabase:
    """Database for meals, ingredients and feedback provided by the user."""

    def __init__(self, db_url: str = None):
        """
        Initialize MealDatabase with PostgreSQL connection.

        Args:
            db_url: PostgreSQL connection string (defaults to DATABASE_URL env var)
        """
        self.db_url = db_url or get_db_url()
        if not self.db_url:
            raise ValueError("DATABASE_URL not provided and not found in environment")

        self.conn = None
        self._connect()

    def _connect(self):
        """Establish database connection."""
        try:
            self.conn = psycopg2.connect(self.db_url)
            self.conn.autocommit = False  # Use transactions
        except psycopg2.Error as e:
            raise ConnectionError(f"Failed to connect to database: {e}")

    def get_meals_from_days_back(self, days_back: int = 14) -> list[str]:
        """
        Get meal names from the last N days.

        Args:
            days_back: Number of days to look back

        Returns:
            List of meal names
        """
        date_threshold = datetime.now() - timedelta(days=days_back)

        with self.conn.cursor() as cursor:
            cursor.execute(
                "SELECT meal_name FROM meals WHERE date > %s ORDER BY date DESC",
                (date_threshold,),
            )
            return [row[0] for row in cursor.fetchall()]

    def add_meal(self, ingredients: str, meal: str, recipe: str, date: datetime) -> int:
        """
        Add a meal to the database.

        Args:
            ingredients: Comma-separated string of ingredients
            meal: Name of the meal
            recipe: Recipe steps (newline-separated string)
            date: Datetime object

        Returns:
            ID of the inserted meal
        """
        with self.conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO meals (ingredients, meal_name, recipe, date) VALUES (%s, %s, %s, %s) RETURNING id",
                (ingredients, meal, recipe, date),
            )
            meal_id = cursor.fetchone()[0]
            self.conn.commit()
            return meal_id

    def update_meal_feedback(self, meal_id: int, feedback: str) -> None:
        """
        Update feedback for a meal.

        Args:
            meal_id: ID of the meal
            feedback: Feedback text
        """
        with self.conn.cursor() as cursor:
            cursor.execute(
                "UPDATE meals SET feedback = %s WHERE id = %s", (feedback, meal_id)
            )
            self.conn.commit()

    def get_meal_by_id(self, meal_id: int) -> Optional[dict]:
        """
        Get a meal by ID.

        Args:
            meal_id: ID of the meal

        Returns:
            Meal record as dictionary or None
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM meals WHERE id = %s", (meal_id,))
            result = cursor.fetchone()
            return dict(result) if result else None

    def get_all_meals(self, limit: int = 100) -> list[dict]:
        """
        Get recent meals.

        Args:
            limit: Maximum number of meals to return

        Returns:
            List of meal records
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM meals ORDER BY date DESC LIMIT %s", (limit,))
            return [dict(row) for row in cursor.fetchall()]

    def get_meal_by_name(self, meal_name: str) -> list[dict]:
        """
        Retrieve meal records by name.

        Args:
            meal_name: Name of the meal to retrieve

        Returns:
            List of meal records as dictionaries (can be multiple with same name)
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM meals WHERE meal = %s", (meal_name,))
            return [dict(row) for row in cursor.fetchall()]

    def get_diverse_recipes(
        self, limit: int = 10, dietary_preferences: str = None
    ) -> pd.DataFrame:
        """Get diverse recipes (random sampling)."""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT contents FROM recipes WHERE contents ILIKE %s ORDER BY RANDOM() LIMIT %s",
                (
                    f"%{dietary_preferences}%",
                    limit,
                ),
            )
            rows = cursor.fetchall()
            return pd.DataFrame([dict(row) for row in rows])

    def save_meal_plan(
        self,
        num_days: int,
        num_people: int,
        dietary_preferences: str = None,
        name: str = None,
    ) -> int:
        """Save a meal plan and return its ID."""
        with self.conn.cursor() as cursor:
            cursor.execute(
                """INSERT INTO meal_plans (name, num_days, num_people, dietary_preferences) 
                VALUES (%s, %s, %s, %s) RETURNING id""",
                (name, num_days, num_people, dietary_preferences),
            )
            plan_id = cursor.fetchone()[0]
            self.conn.commit()
            return plan_id

    def add_meal_to_plan(
        self,
        meal_plan_id: int,
        day_number: int,
        ingredients: str,
        meal: str,
        recipe: str,
        accepted: bool = False,
    ) -> int:
        """Add a meal to a specific meal plan."""
        with self.conn.cursor() as cursor:
            cursor.execute(
                """INSERT INTO meals (meal_plan_id, day_number, ingredients, meal_name, recipe, date, accepted) 
                VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id""",
                (
                    meal_plan_id,
                    day_number,
                    ingredients,
                    meal,
                    recipe,
                    datetime.now(),
                    accepted,
                ),
            )
            meal_id = cursor.fetchone()[0]
            self.conn.commit()
            return meal_id

    def get_latest_meal_plan(self) -> dict:
        """Get the most recent meal plan with all its meals."""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            # Get latest plan
            cursor.execute("SELECT * FROM meal_plans ORDER BY created_at DESC LIMIT 1")
            plan = cursor.fetchone()

            if not plan:
                return None

            # Get meals for this plan
            cursor.execute(
                """SELECT * FROM meals 
                WHERE meal_plan_id = %s 
                ORDER BY day_number""",
                (plan["id"],),
            )
            meals = [dict(row) for row in cursor.fetchall()]

            return {"plan": dict(plan), "meals": meals}

    def update_meal_acceptance(self, meal_id: int, accepted: bool) -> None:
        """Update whether a meal in a plan is accepted."""
        with self.conn.cursor() as cursor:
            cursor.execute(
                "UPDATE meals SET accepted = %s WHERE id = %s", (accepted, meal_id)
            )
            self.conn.commit()

    def replace_meal_in_plan(self, old_meal_id: int, new_meal_data: dict) -> int:
        """Replace a rejected meal with a new one."""
        with self.conn.cursor() as cursor:
            # Get the old meal's plan info
            cursor.execute(
                "SELECT meal_plan_id, day_number FROM meals WHERE id = %s",
                (old_meal_id,),
            )
            plan_info = cursor.fetchone()

            if not plan_info:
                return None

            meal_plan_id, day_number = plan_info

            # Delete old meal
            cursor.execute("DELETE FROM meals WHERE id = %s", (old_meal_id,))

            # Insert new meal
            cursor.execute(
                """INSERT INTO meals (meal_plan_id, day_number, ingredients, meal_name, recipe, date, accepted) 
                VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id""",
                (
                    meal_plan_id,
                    day_number,
                    new_meal_data["ingredients"],
                    new_meal_data["name"],
                    new_meal_data["recipe"],
                    datetime.now(),
                    False,
                ),
            )
            new_meal_id = cursor.fetchone()[0]
            self.conn.commit()

            return new_meal_id

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
