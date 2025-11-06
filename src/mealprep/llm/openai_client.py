from openai import OpenAI
import os
import time
import logging
from mealprep.db.models import MealSuggestion, MealPlan
from mealprep.config.settings import get_api_key
from dotenv import load_dotenv
import pandas as pd

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
        similar_recipes: pd.DataFrame | None = None,
        plan: bool = False,
    ):
        context = ""
        if similar_recipes is not None and not similar_recipes.empty:
            context = "\n".join(similar_recipes["contents"].tolist())

        full_prompt = f"{context}\n\n{prompt}" if context else prompt

        if plan:
            response_format = {
                "type": "json_schema",
                "json_schema": {
                    "name": "meal_plan",
                    "schema": MealPlan.model_json_schema(),
                },
            }
        else:
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
                            "content": "You are a helpful private chef assistant.",
                        },
                        {"role": "user", "content": full_prompt},
                    ],
                    temperature=temperature,
                    response_format=response_format,
                )

                message = completion.choices[0].message.content
                if plan:
                    meal_plan = MealPlan.model_validate_json(message)
                    parsed = meal_plan.as_list()

                    return parsed

                parsed = MealSuggestion.model_validate_json(message)
                return parsed.model_dump()

            except Exception:
                log.exception(f"Attempt {attempt+1}: error parsing structured output")
                time.sleep(1)

        return None
