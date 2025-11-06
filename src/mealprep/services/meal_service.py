from datetime import datetime, timedelta
from mealprep.llm.claude_client import ClaudeClient
from mealprep.llm.openai_client import OpenAIClient
from mealprep.db.database import MealDatabase
from mealprep.db.vector_store import VectorStore
import re
import json

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
            similar_recipes_df = vec.search(
                ingredients,
                limit=10,
                metadata_filter={"dietary_preferences": dietary_preferences},
            )
            context_type = "ingredient-based"
        else:
            # NO INGREDIENTS -> Either:
            # Option A: Get popular/diverse recipes
            similar_recipes_df = self.db.get_diverse_recipes(
                limit=10, dietary_preferences=dietary_preferences
            )
            context_type = "diverse-selection"

            # Option B: Don't use RAG at all
            # similar_recipes = []
            # context_type = "creative"

        # Build prompt for LLM
        prompt = self._build_suggestion_prompt(
            ingredients=ingredients or [],
            all_excluded=all_excluded,
            num_people=num_people,
            dietary_preferences=dietary_preferences,
            context_type=context_type,
        )

        # Get suggestion from LLM
        suggestion = self.llm.get_meal_suggestion(
            prompt, temperature=1.0, similar_recipes=similar_recipes_df
        )
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

    def parse_meal_plan(self, raw_response: list) -> list:
        """
        Parse meal plan suggestion - now just passes through since LLM returns structured data.
        """
        content_bool = []
        if raw_response:
            for meal in raw_response:
                if meal and all(
                    k in meal for k in ["day", "meal_name", "ingredients", "recipe"]
                ):
                    content_bool.append(True)
        if all(content_bool):
            return raw_response
        else:
            # Fallback: use regex parser if structured output failed
            return self._fallback_parse_meal_plan(raw_response)

    def generate_meal_plan(
        self,
        num_days: int,
        num_people: int = 2,
        days_back: int = 14,
        dietary_preferences: str = None,
    ) -> dict:
        """Generate entire meal plan in ONE LLM call."""

        # Get recent meals to avoid repetition
        recent_meals = self.db.get_meals_from_days_back(days_back)

        # Get diverse recipes for inspiration
        similar_recipes_df = self.db.get_diverse_recipes(
            limit=num_days * 3, dietary_preferences=dietary_preferences
        )

        # Single prompt for entire plan
        prompt = self._build_mealplan_prompt(
            num_days=num_days,
            num_people=num_people,
            dietary_preferences=dietary_preferences,
            all_excluded=recent_meals,
        )

        suggestion = self.llm.get_meal_suggestion(
            prompt, temperature=1.0, similar_recipes=similar_recipes_df, plan=True
        )
        meals = self.parse_meal_plan(suggestion)
        # Collect all ingredients
        ingredients = []
        for meal in meals:
            ingredients.extend(meal.get("ingredients", []))
        # Generate shopping list
        shopping_list = self._create_shopping_list(ingredients)

        return {"meals": meals, "shopping_list": shopping_list}

    def _generate_meal_plan(
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
                recipe="|".join(meal["recipe"]),
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

    def _build_suggestion_prompt(
        self,
        ingredients: list[str],
        dietary_preferences: str,
        all_excluded: list[str],
        num_people: int,
        context_type: str,
    ) -> str:
        """
        Build a prompt for OpenAI to suggest a meal.

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
            You are a creative private chef planning daily meals. 
            Suggest ONE meal that is easy to prepare (ready in under 1 hour) and uses as many of the available ingredients as possible 
            without being repetitive or too similar to recent meals.

            ✦ The meal must be suitable for {num_people} people.
            ✦ Dietary preferences: {diet_str}. Suggest healthy and balanced meals.
            ✦ Basic stock of groceries (salt, pepper, oil, vinegar, noodles, rice) is always available.
            ✦ Available ingredients: {", ".join(ingredients)}.
            ✦ Show how much of the ingredients will be needed for {num_people} people.
            ✦ Recent or excluded meals (avoid these and anything very similar in flavor, cuisine, main ingredient, or cooking style): 
            {all_excluded_str}.

            To ensure variety:
            - Try to vary the **main protein**, **cuisine style**, or **preparation method** from excluded meals.
            - Prefer a different dominant flavor profile (e.g., spicy vs mild, Asian vs Mediterranean, etc.).
            - Avoid repeating similar sauces, spice mixes, or cooking bases.

            Respond strictly in this structured format:
            meal_name: [Meal Name]
            ingredients: [Ingredient1, Ingredient2, ...]
            recipe: [Step-by-step recipe, no numbering]
            """
        else:
            prompt = f"""
            You are a creative private chef planning daily meals. 
            Suggest ONE easy meal (ready in under 1 hour) that is **distinct** from recently served meals.

            ✦ Suitable for {num_people} people.
            ✦ Dietary preferences: {diet_str}.
            ✦ Basic stock of groceries (salt, pepper, oil, vinegar, noodles, rice) is always available.
            ✦ Show how much of the ingredients will be needed for {num_people} people.
            ✦ Recent or excluded meals (avoid these and anything very similar in flavor, cuisine, main ingredient, or cooking style): 
            {all_excluded_str}.

            To ensure variety:
            - Choose a different **cuisine**, **main ingredient**, or **cooking method** from excluded meals.
            - Try to diversify in **flavors**, **textures**, and **meal types** (e.g., salad vs stew vs stir-fry).

            Return one suggested meal.
            """
        return prompt

    def _build_mealplan_prompt(
        self,
        num_days: int,
        dietary_preferences: str,
        all_excluded: list[str],
        num_people: int,
    ) -> str:
        """
        Build a prompt for OpenAI to suggest a meal plan.

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
        prompt = f"""
            You are a creative private chef creating a {num_days}-day meal plan.
            Suggest ONE easy meal (ready in under 1 hour) that is **distinct** from recently served meals.

            ✦ Suitable for {num_people} people.
            ✦ Dietary preferences: {diet_str}. Suggest healthy and balanced meals.
            ✦ Basic stock of groceries (salt, pepper, oil, vinegar, noodles, rice) is always available.
            ✦ Show how much of the ingredients will be needed for {num_people} people.
            ✦ Recent or excluded meals (avoid these and anything very similar in flavor, cuisine, main ingredient, or cooking style): 
            {all_excluded_str}.
            ✦ Ensure maximum variety across all {num_days} days.
            

            To ensure variety:
            - Choose a different **cuisine**, **main ingredient**, or **cooking method** from excluded meals.
            - Try to diversify in **flavors**, **textures**, and **meal types** (e.g., salad vs stew vs stir-fry).

            Return one suggested meal per day.

            Return only valid JSON.
            Do not add explanations or formatting outside JSON.
            Fill the structure:
            {{
            "days": {{
                "1": {{ "meal_name": "", "ingredients": [], "recipe": [] }},
                "2": {{ "meal_name": "", "ingredients": [], "recipe": [] }}
            }}
            }}
            """
        return prompt

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

    def _fallback_parse(self, raw_response: str) -> dict:
        """
        Fallback: Parse meal response in format: 'meal_name: XY, ingredients: [...], recipe: 1. step, 2. step, etc'

        Args:
            raw_response: Raw response string from OpenAI

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

    def _fallback_parse_meal_plan(self, raw_response: str) -> list[dict]:
        """
        Fallback: Parse meal plan response with multiple days.

        Expected format for each meal:
        day_number: [Day Number]
        meal_name: [Meal Name]
        ingredients: [Ingredient1, Ingredient2, ...]
        recipe: [Step-by-step recipe, no numbering]

        Args:
            raw_response: Raw response string from OpenAI

        Returns:
            List of meal dictionaries, one per day
        """
        meals = []

        # Try to parse as JSON first
        try:
            # Remove markdown code blocks if present
            json_match = re.search(
                r"```(?:json)?\s*(\[.*?\])\s*```", raw_response, re.DOTALL
            )
            if json_match:
                raw_response = json_match.group(1)

            meals_data = json.loads(raw_response)
            return meals_data
        except json.JSONDecodeError:
            pass

        # Fallback: Split by day markers
        day_pattern = r"day:\s*(\d+)"
        day_splits = re.split(day_pattern, raw_response, flags=re.IGNORECASE)

        # day_splits will be: ['', '1', 'content for day 1', '2', 'content for day 2', ...]
        for i in range(1, len(day_splits), 2):
            if i + 1 >= len(day_splits):
                break

            day_number = int(day_splits[i])
            day_content = day_splits[i + 1]

            meal = {
                "day_number": day_number,
                "meal_name": "",
                "ingredients": [],
                "recipe": [],
            }

            # Extract meal name
            meal_match = re.search(
                r"meal_name:\s*([^\n]+?)(?=\n|ingredients:|$)",
                day_content,
                re.IGNORECASE,
            )
            if meal_match:
                meal["meal_name"] = meal_match.group(1).strip()

            # Extract ingredients
            ingredients_match = re.search(
                r"ingredients:\s*(.+?)(?=recipe:|$)",
                day_content,
                re.IGNORECASE | re.DOTALL,
            )
            if ingredients_match:
                ingredients_text = ingredients_match.group(1).strip()
                # Handle both list format and comma-separated
                ingredients_text = re.sub(r"[\[\]]", "", ingredients_text)
                ingredients_list = re.split(r"[,\n]", ingredients_text)
                meal["ingredients"] = [
                    ing.strip() for ing in ingredients_list if ing.strip()
                ]

            # Extract recipe steps
            recipe_match = re.search(
                r"recipe:\s*(.+?)(?=day:\s*\d+|$)",
                day_content,
                re.IGNORECASE | re.DOTALL,
            )
            if recipe_match:
                recipe_text = recipe_match.group(1).strip()

                # Split by newlines (since no numbering)
                steps = [
                    line.strip() for line in recipe_text.split("\n") if line.strip()
                ]

                # Remove any bullet points or dashes at the start
                meal["recipe"] = [
                    re.sub(r"^[-•*]\s*", "", step).strip()
                    for step in steps
                    if step.strip()
                ]

            meals.append(meal)

        return meals
