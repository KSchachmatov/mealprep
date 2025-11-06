from pydantic import BaseModel, Field
from typing import Dict, List


class MealSuggestion(BaseModel):
    meal_name: str = Field(description="Name of the meal")
    ingredients: List[str] = Field(description="List of ingredients needed")
    recipe: List[str] = Field(description="Step-by-step instructions")


# class MealPlan(BaseModel):
#     days: Dict[str, MealSuggestion] = Field(
#         description="Mapping of day numbers to meal suggestions",
#         example={
#             "1": {"meal_name": "...", "ingredients": ["..."], "recipe": ["..."]},
#             "2": {"meal_name": "...", "ingredients": ["..."], "recipe": ["..."]},
#         },
#     )
class MealPlan(BaseModel):
    days: Dict[str, MealSuggestion]

    def as_list(self) -> List[dict]:
        return [
            {"day_number": day, **meal.model_dump()} for day, meal in self.days.items()
        ]
