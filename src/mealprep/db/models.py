from pydantic import BaseModel, Field


class MealSuggestion(BaseModel):
    meal_name: str = Field(description="Name of the meal")
    ingredients: list[str] = Field(description="List of ingredients needed")
    recipe: list[str] = Field(description="List of recipe steps")
