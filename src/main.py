from datetime import datetime
import streamlit as st
from mealprep.services.meal_service import MealService

service = MealService()

st.set_page_config(page_title="Meal Planner", layout="wide")
st.title("🍽️ AI Meal Planner")

# Initialize session state for Mode 1
if "ingredients" not in st.session_state:
    st.session_state.ingredients = ["", ""]
if "rejected_meals" not in st.session_state:
    st.session_state.rejected_meals = []
if "current_meal" not in st.session_state:
    st.session_state.current_meal = None
if "meal_saved" not in st.session_state:
    st.session_state.meal_saved = False

# Initialize session state for Mode 2
if "meal_plan" not in st.session_state:
    st.session_state.meal_plan = None

# =============================================================================
# MODE 1: Single Meal Suggestion
# =============================================================================

# Common inputs for both modes
st.header("Mode 1: Suggest a Single Meal")

# Common inputs for both modes
col1, col2, col3 = st.columns(3)
with col1:
    num_people = st.number_input(
        "Number of people", min_value=1, max_value=20, value=2, key="mode1_people"
    )
with col3:
    dietary_preferences = st.text_input(
        "Dietary preferences (optional)",
        placeholder="e.g., vegetarian, gluten-free",
        key="mode1_diet",
    )
with col2:
    days_back = st.number_input(
        "Number of days to avoid repetition",
        min_value=0,
        max_value=60,
        value=14,
        key="mode1_backperiod",
    )
st.write("**Available ingredients:**")

# Display ingredient inputs dynamically
for i in range(len(st.session_state.ingredients)):
    st.session_state.ingredients[i] = st.text_input(
        f"Ingredient {i+1}",
        value=st.session_state.ingredients[i],
        key=f"ingredient_{i}",
        label_visibility="collapsed",
    )

# Buttons to add/remove ingredients
col1, col2 = st.columns(2)
with col1:
    if st.button("➕ Add Ingredient"):
        st.session_state.ingredients.append("")
        st.rerun()

with col2:
    if len(st.session_state.ingredients) > 1:
        if st.button("➖ Remove Ingredient"):
            st.session_state.ingredients.pop()
            st.rerun()

# Filter out empty ingredients
active_ingredients = [
    ing.strip() for ing in st.session_state.ingredients if ing.strip()
]

# Suggest meal button
if st.button("🚀 Suggest a Meal", type="primary"):
    if active_ingredients:
        st.info(f"Looking for a meal with: {', '.join(active_ingredients)}")
        parsed_meal = service.suggest_meal(
            active_ingredients,
            rejected_meals=st.session_state.rejected_meals,
            num_people=num_people,
            dietary_preferences=dietary_preferences if dietary_preferences else None,
        )
        st.session_state.current_meal = parsed_meal
        st.session_state.meal_saved = False
        st.rerun()
    else:
        st.warning("Please add at least one ingredient")

# Show suggested meal and accept/reject buttons
if st.session_state.current_meal:
    meal = st.session_state.current_meal
    st.success(f"🍽️ **{meal['meal_name']}** (serves {num_people})")

    # Display ingredients
    if meal.get("ingredients"):
        st.subheader("🥘 Ingredients")
        for ingredient in meal["ingredients"]:
            st.write(f"- {ingredient}")

    st.subheader("👨‍🍳 Recipe Steps")
    for i, step in enumerate(meal["recipe"], 1):
        st.write(f"**{i}.** {step}")

    # Show different buttons based on whether meal is saved
    if not st.session_state.meal_saved:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ That's it, let's cook it!", type="primary"):
                st.balloons()
                st.success(
                    f"Saved! You're cooking {st.session_state.current_meal['meal_name']} today."
                )
                service.add_meal(
                    ingredients=st.session_state.current_meal["igredients"],
                    meal=st.session_state.current_meal["meal_name"],
                    recipe="\n".join(st.session_state.current_meal["recipe"]),
                    date=datetime.now(),
                )
                st.session_state.meal_saved = True
                st.rerun()

        with col2:
            if st.button("🔄 Get Another Suggestion"):
                st.session_state.rejected_meals.append(
                    st.session_state.current_meal["meal_name"]
                )
                st.session_state.current_meal = None
                st.rerun()
    else:
        # After meal is saved, show "Start Over" button
        if st.button("🎉 Enjoy your meal! Start over?", type="primary"):
            st.session_state.current_meal = None
            st.session_state.meal_saved = False
            st.session_state.rejected_meals = []
            st.rerun()

st.divider()

# =============================================================================
# MODE 2: Multi-Day Meal Plan
# =============================================================================

st.header("Mode 2: Multi-Day Meal Plan")

# Common inputs
col1, col2, col3, col4 = st.columns(4)
with col1:
    num_days = st.number_input(
        "Number of days", min_value=1, max_value=14, value=7, key="mode2_days"
    )
with col2:
    num_people_plan = st.number_input(
        "Number of people", min_value=1, max_value=20, value=2, key="mode2_people"
    )
with col3:
    days_back_plan = st.number_input(
        "Number of days to avoid repetition",
        min_value=0,
        max_value=60,
        value=14,
        key="mode2_backperiod",
    )
with col4:
    dietary_preferences_plan = st.text_input(
        "Dietary preferences (optional)",
        placeholder="e.g., vegan, nut-free",
        key="mode2_diet",
    )

col1, col2 = st.columns(2)
with col1:
    if st.button("📅 Generate Meal Plan", type="primary"):
        with st.spinner(f"Generating {num_days}-day meal plan..."):
            meal_plan = service.generate_meal_plan(
                num_days=num_days,
                num_people=num_people_plan,
                days_back=days_back_plan,
                dietary_preferences=(
                    dietary_preferences_plan if dietary_preferences_plan else None
                ),
            )
            st.session_state.meal_plan = meal_plan
            st.rerun()
with col2:
    if st.button("📋 Load Last Plan", key="planloader_first_run"):
        loaded_plan = service.get_latest_plan()
        print(loaded_plan)
        if loaded_plan:
            st.session_state.meal_plan = {
                "meals": loaded_plan["meals"],
                "shopping_list": [],  # Regenerate if needed
            }
            st.rerun()
        else:
            st.warning("No saved meal plans found")

# Display meal plan with accept/reject per meal
if st.session_state.meal_plan:
    plan = st.session_state.meal_plan

    st.success(f"✨ Your {len(plan['meals'])}-day meal plan is ready!")

    # Initialize acceptance state if not exists
    if "meal_acceptances" not in st.session_state:
        st.session_state.meal_acceptances = {
            i: False for i in range(len(plan["meals"]))
        }

    # Display meals with individual accept/reject
    st.subheader("📆 Your Meal Plan")
    for idx, meal in enumerate(plan["meals"]):
        col1, col2 = st.columns([4, 1])

        with col1:
            with st.expander(
                f"Day {meal['day_number']}: {meal['meal_name']}",
                expanded=not st.session_state.meal_acceptances.get(idx, False),
            ):
                if meal.get("ingredients"):
                    st.write("**Ingredients:**")
                    print(meal["ingredients"])
                    for ingredient in meal["ingredients"]:
                        print(ingredient)
                        st.write(f"- {ingredient}")
                    st.write("")

                st.write("**Recipe:**")
                for i, step in enumerate(meal["recipe"], 1):
                    st.write(f"{i}. {step}")

        with col2:
            if st.session_state.meal_acceptances.get(idx, False):
                st.success("✅ Accepted")
                if st.button("↩️ Undo", key=f"undo_{idx}"):
                    st.session_state.meal_acceptances[idx] = False
                    st.rerun()
            else:
                col_accept, col_reject = st.columns(2)
                with col_accept:
                    if st.button("✅", key=f"accept_{idx}"):
                        st.session_state.meal_acceptances[idx] = True
                        st.rerun()
                with col_reject:
                    if st.button("🔄", key=f"regenerate_{idx}"):
                        # Regenerate this meal
                        with st.spinner("Generating new meal..."):
                            new_meal = service.regenerate_meal_for_day(
                                day=meal["day_number"],
                                meal_plan_context=plan,
                                num_people=num_people_plan,
                                dietary_preferences=dietary_preferences_plan,
                            )
                            new_meal["day_number"] = meal["day_number"]
                            st.session_state.meal_plan["meals"][idx] = new_meal
                            st.rerun()

    # Shopping list
    st.subheader("🛒 Shopping List")
    if plan["shopping_list"]:
        for item in plan["shopping_list"]:
            st.write(f"- {item}")
    else:
        st.info("No shopping list generated")

    # Action buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💾 Save Meal Plan", type="primary"):
            service.save_meal_plan_to_db(
                meal_plan=plan,
                num_people=num_people_plan,
                dietary_preferences=dietary_preferences_plan,
                name=f"Meal Plan {datetime.now().strftime('%Y-%m-%d')}",
            )
            st.success("Meal plan saved!")

    with col2:
        if st.button("📋 Load Last Plan", key="planloader_after_new_gen"):
            loaded_plan = service.get_latest_plan()
            if loaded_plan:
                st.session_state.meal_plan = {
                    "meals": loaded_plan["meals"],
                    "shopping_list": [],  # Regenerate if needed
                }
                st.rerun()
            else:
                st.warning("No saved meal plans found")

    with col3:
        if st.button("🔄 Generate New Plan"):
            st.session_state.meal_plan = None
            st.session_state.meal_acceptances = {}
            st.rerun()
