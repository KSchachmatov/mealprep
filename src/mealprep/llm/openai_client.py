from openai import OpenAI
import os
import time
import logging
from mealprep.db.models import MealSuggestion
from mealprep.config.settings import get_api_key
from dotenv import load_dotenv

load_dotenv()
log = logging.getLogger(__name__)


class OpenAIClient:
    """Client for interacting with the OpenAI API with structured outputs."""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or get_api_key("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key must be provided or set in OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)

    def get_meal_suggestion(
        self,
        prompt: str,
        temperature: float = 0.7,
        similar_recipes: list[dict] | None = None,
    ) -> dict | None:
        # Build context from similar recipes
        context = ""
        if not similar_recipes.empty:
            context = "Here are some recipe ideas from our database:\n\n"
            for i, recipe in similar_recipes.iterrows():
                context += recipe["contents"]

        full_prompt = f"{context}\n{prompt}" if context else prompt

        response_format = {
            "type": "json_schema",
            "json_schema": {
                "name": "meal_suggestion",
                "schema": MealSuggestion.model_json_schema(),
            },
        }

        for attempt in range(2):
            try:
                completion = self.client.chat.completions.create(
                    model="gpt-5-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful private chef assistant who suggests meals.",
                        },
                        {"role": "user", "content": full_prompt},
                    ],
                    temperature=temperature,
                    response_format=response_format,
                )

                meal_suggestion = MealSuggestion.model_validate_json(
                    completion.choices[0].message.content
                )

                if not meal_suggestion.meal_name:
                    log.warning("Meal suggestion missing name: %s", meal_suggestion)

                return meal_suggestion.model_dump()

            except Exception as e:
                log.exception(f"Attempt {attempt+1}: error parsing structured output")
                time.sleep(1)

        return None
