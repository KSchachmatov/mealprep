from datetime import datetime, timedelta
from mealprep.llm.claude_client import ClaudeClient
from mealprep.llm.openai_client import OpenAIClient
from mealprep.db.database import MealDatabase
from mealprep.db.vector_store import VectorStore
import re

# Initialize VectorStore
vec = VectorStore()


class MealService:
    """Service for meal planning operations."""

    def __init__(self, api_key: str = None):
        """
        Initialize MealService.

        Args:
            db_path: Path to SQLite database
            api_key: Anthropic API key (from env if not provided)
        """
        self.db = MealDatabase()
        self.llm = OpenAIClient(api_key)

    def suggest_meal(
        self,
        ingredients: list[str],
        days_back: int = 14,
        num_people: int = 3,
        dietary_preferences: str = None,
        rejected_meals: list[str] = None,
    ) -> str:
        """
        Suggest a meal based on available ingredients.

        Args:
            ingredients: List of available ingredients
            days_back: Number of days to look back for recent meals (default 14)

        Returns:
            Suggested meal as string
        """
        # Get recent meals to avoid repetition
        recent_meals = self.db.get_meals_from_days_back(days_back)
        all_excluded = recent_meals + (rejected_meals or [])

        if ingredients and len(ingredients) > 0:
            # USER HAS INGREDIENTS -> Use RAG to find similar recipes
            similar_recipes_df = vec.search(ingredients, limit=5)
            context_type = "ingredient-based"
        else:
            # NO INGREDIENTS -> Either:
            # Option A: Get popular/diverse recipes
            similar_recipes_df = self.db.get_diverse_recipes(limit=10)
            context_type = "diverse-selection"

            # Option B: Don't use RAG at all, let Claude be creative
            # similar_recipes = []
            # context_type = "creative"

        # Build prompt for Claude
        prompt = self._build_suggestion_prompt(
            ingredients=ingredients or [],
            all_excluded=all_excluded,
            num_people=num_people,
            dietary_preferences=dietary_preferences,
            context_type=context_type,
        )

        # Get suggestion from Claude
        suggestion = self.llm.get_meal_suggestion(
            prompt, temperature=1.0, similar_recipes=similar_recipes_df
        )
        print(suggestion)
        return self.parse_meal_suggestion(suggestion)

    def add_meal(
        self, ingredients: str, meal: str, recipe: str, date: datetime = None
    ) -> int:
        """
        Add a meal to the database.

        Args:
            ingredients: Comma-separated string of ingredients
            meal: Name of the meal
            recipe: Recipe steps
            date: Date when the meal was cooked (default now)

        Returns:
            ID of the added meal
        """
        if date is None:
            date = datetime.now()

        # Store in database
        return self.db.add_meal(", ".join(ingredients), meal, "\n".join(recipe), date)

    def get_recent_meals(self, days_back: int = 14) -> list[dict]:
        """
        Get meals from the last N days.

        Args:
            days_back: Number of days to retrieve

        Returns:
            List of meal records with date and meal name
        """
        return self.db.get_meals_from_days_back(days_back)

    def add_feedback(self, meal_id: int, feedback: str) -> None:
        """
        Add feedback for a meal (for future learning).

        Args:
            meal_id: ID of the meal in database
            feedback: Feedback text (e.g., "loved it", "too spicy", etc.)
        """
        self.db.update_meal_feedback(meal_id, feedback)

    def get_meal_by_name(self, meal_name: int) -> dict:
        """
        Retrieve a meal record by its name.

        Args:
            meal_name: Name of the meal to retrieve

        Returns:
            Meal record as a dictionary
        """
        return self.db.get_meal_by_name(meal_name)

    def parse_meal_suggestion(self, raw_response: dict) -> dict:
        """
        Parse meal suggestion - now just passes through since LLM returns structured data.
        """
        if raw_response and all(
            k in raw_response for k in ["meal_name", "ingredients", "recipe"]
        ):
            return raw_response
        else:
            # Fallback: use regex parser if structured output failed
            return self._fallback_parse(raw_response)

    def _fallback_parse(self, raw_response: str) -> dict:
        """
        Fallback: Parse meal response in format: 'meal_name: XY, ingredients: [...], recipe: 1. step, 2. step, etc'

        Args:
            raw_response: Raw response string from Claude

        Returns:
            Dictionary with 'meal_name', 'recipe', and 'ingredients' keys
            Example: {
                'meal_name': 'Pasta Carbonara',
                'ingredients': ['pasta', 'eggs', 'parmesan'],
                'recipe': ['Cook pasta', 'Mix eggs with cheese', 'Combine']
            }
        """
        result = {"meal_name": "", "recipe": [], "ingredients": []}

        # Extract meal name (between 'meal_name:' and next comma or 'ingredients:')
        meal_match = re.search(
            r"meal_name:\s*([^,]+?)(?=,\s*ingredients:|$)", raw_response, re.IGNORECASE
        )
        if meal_match:
            result["meal_name"] = meal_match.group(1).strip()

        # Extract ingredients (between 'ingredients:' and 'recipe:')
        ingredients_match = re.search(
            r"ingredients:\s*(.+?)(?=recipe:)", raw_response, re.IGNORECASE | re.DOTALL
        )
        if ingredients_match:
            ingredients_text = ingredients_match.group(1).strip()
            # Split by commas or newlines, clean up
            ingredients_list = re.split(r"[,\n]", ingredients_text)
            result["ingredients"] = [
                ing.strip() for ing in ingredients_list if ing.strip()
            ]

        # Extract recipe steps (everything after 'recipe:')
        recipe_match = re.search(
            r"recipe:\s*(.+)$", raw_response, re.IGNORECASE | re.DOTALL
        )
        if recipe_match:
            recipe_text = recipe_match.group(1).strip()

            # Split by numbered steps (1., 2., 3., etc.)
            steps = re.split(r"\d+\.\s*", recipe_text)

            # Filter out empty strings and strip whitespace
            result["recipe"] = [step.strip() for step in steps if step.strip()]

        return result

    def close(self):
        """Close the database connection."""
        self.db.close()

    def _build_suggestion_prompt(
        self,
        ingredients: list[str],
        dietary_preferences: str,
        all_excluded: list[str],
        num_people: int,
        context_type: str,
    ) -> str:
        """
        Build a prompt for Claude to suggest a meal.

        Args:
            ingredients: List of available ingredients
            recent_meals: List of recently suggested meals

        Returns:
            Formatted prompt string
        """

        all_excluded_str = ", ".join(all_excluded) if all_excluded else "None"
        diet_str = (
            f"\nDietary restrictions: {dietary_preferences}"
            if dietary_preferences
            else ""
        )
        if context_type == "ingredient-based":
            prompt = f"""
            Image you are a private chef and you need to come up with meal suggestions every day. 
            The recipes have to be easy to prepare and be ready under an hour. 
            Suggest ONE meal using the available ingredients. You don't need to use all ingredients, but try to use as many as possible. 
            If no ingredients are provided, suggest a random meal.
            The meal should be suitable to serve {num_people} people. There are the following dietary preferences to consider: {diet_str}.
            Assume that basic seasonings (salt, pepper, oil, vinegar, noodles, rice) are always available.

            Available ingredients: {", ".join(ingredients)}

            Recent meals, do NOT suggest these or some that are very similar: {all_excluded_str}

            Respond with the meal name and the recipe in form of steps to be executed. 
            Return the response strictly in the following format: "meal_name: [Meal Name], ingredients: [Ingredient1, Ingredient2, ...], recipe: [Recipe Steps]"
            """
        else:
            prompt = f"""
            Image you are a private chef and you need to come up with meal suggestions every day. 
            The recipes have to be easy to prepare and be ready under an hour. 
            Suggest ONE meal that is different from recent meals.
            The meal should be suitable to serve {num_people} people. There are the following dietary preferences to consider: {diet_str}.
            Assume that basic seasonings (salt, pepper, oil, vinegar, noodles, rice) are always available.

            Recent meals, do NOT suggest these or some that are very similar: {all_excluded_str}

            Respond with the meal name and the recipe in form of steps to be executed. 
            Return the response strictly in the following format: "meal_name: [Meal Name], ingredients: [Ingredient1, Ingredient2, ...], recipe: [Recipe Steps]"
            """

        return prompt

    def generate_meal_plan(
        self,
        num_days: int,
        num_people: int,
        days_back: int,
        dietary_preferences: str = None,
    ) -> dict:
        """Generate a meal plan for X days with shopping list."""
        meals = []
        all_ingredients = []

        for day in range(1, num_days + 1):
            # Get diverse meals - use rejected_meals to avoid repeats
            rejected = [m["meal_name"] for m in meals]

            # Generate meal for this day
            meal = self.suggest_meal(
                ingredients=[],  # Let RAG suggest based on variety
                days_back=days_back,
                num_people=num_people,
                dietary_preferences=dietary_preferences,
                rejected_meals=rejected,
            )

            meal["day_number"] = day
            meals.append(meal)
            all_ingredients.extend(meal["ingredients"])

        # Deduplicate and organize shopping list
        shopping_list = self._create_shopping_list(all_ingredients)

        return {"meals": meals, "shopping_list": shopping_list}

    def _create_shopping_list(self, ingredients: list[str]) -> list[str]:
        """Create a deduplicated shopping list from ingredients."""
        ingredient_count = {}
        for ing in ingredients:
            ing_lower = ing.lower()
            if ing_lower in ingredient_count:
                ingredient_count[ing_lower] += 1
            else:
                ingredient_count[ing_lower] = 1

        shopping_list = [
            f"{ing} (x{count})" if count > 1 else ing
            for ing, count in ingredient_count.items()
        ]
        return shopping_list

    def save_meal_plan_to_db(
        self,
        meal_plan: dict,
        num_people: int,
        dietary_preferences: str = None,
        name: str = None,
    ):
        """Save a meal plan to database."""
        # Create meal plan record
        plan_id = self.db.save_meal_plan(
            num_days=len(meal_plan["meals"]),
            num_people=num_people,
            dietary_preferences=dietary_preferences,
            name=name,
        )

        # Save each meal
        for meal in meal_plan["meals"]:
            self.db.add_meal_to_plan(
                meal_plan_id=plan_id,
                day_number=meal["day_number"],
                ingredients=", ".join(meal.get("ingredients", [])),
                meal=meal["meal_name"],
                recipe="\n".join(meal["recipe"]),
                accepted=False,
            )

        return plan_id

    def get_latest_plan(self):
        """Retrieve the latest meal plan."""
        return self.db.get_latest_meal_plan()

    def regenerate_meal_for_day(
        self,
        day: int,
        meal_plan_context: dict,
        num_people: int,
        dietary_preferences: str = None,
    ):
        """Generate a new meal for a specific day in the plan."""
        # Get all meal names from the plan to avoid duplicates
        existing_meals = [
            m["meal_name"] for m in meal_plan_context["meals"] if m["day_number"] != day
        ]

        # Generate new meal
        new_meal = self.suggest_meal(
            ingredients=[],
            rejected_meals=existing_meals,
            num_people=num_people,
            dietary_preferences=dietary_preferences,
        )

        return new_meal
