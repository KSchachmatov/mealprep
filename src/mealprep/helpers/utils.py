import pandas as pd
import numpy as np


def add_dietary_prefs(df: pd.DataFrame) -> pd.DataFrame:
    df["with_meat"] = df.ingredients.str.contains(
        """
    meat|chicken|turkey|duck|goose|quail|pheasant|guinea|cornish hen|
    beef|veal|steak|ground beef|minced beef|roast beef|brisket|short ribs|oxtail|beef tenderloin|sirloin|ribeye|
    pork|bacon|ham|prosciutto|pancetta|sausage|chorizo|
    lamb|mutton|goat|venison|deer|elk|rabbit|boar|bison|buffalo|
    meatballs|deli meat|hot dog|kebab|salami|pepperoni|pâté|liverwurst
    """
    )

    df["with_fish"] = df.ingredients.str.contains(
        """
        salmon|tuna|cod|haddock|tilapia|trout|mackerel|sardines|anchovies|halibut|snapper|catfish|sole|swordfish|pollock
        """
    )

    df["with_shellfish"] = df.ingredients.str.contains(
        """shrimp|prawns|crab|lobster|mussels|clams|scallops|squid|calamari|octopus|oysters
        """
    )

    df["with_dairy"] = df.ingredients.str.contains(
        """dairy|milk|cream|butter|ghee|cheese|cheddar|mozzarella|parmesan|gouda|provolone|brie|camembert|feta|gorgonzola|ricotta|mascarpone|queso fresco|halloumi|paneer|pecorino|asiago|romano|colby jack|monterey jack|havarti|yogurt|kefir|labneh|ayran|skyr|ice cream|custard|flan
        """
    )

    df["with_eggs"] = df.ingredients.str.contains(
        """
        egg|mayonnaise|aioli|hollandaise|custard|meringue|quiche|omelette|frittata|pasta dough|brioche|challah|pancakes|waffles|crepes|éclairs|choux|macarons
        """
    )
    df["with_honey"] = df.ingredients.str.contains(
        """
        honey
        """
    )
    deserts_str = """cake|cookie|brownie|muffin|cupcake|pancake|waffle|pie|tart|crumble|pudding|custard|mousse|cheesecake|ice cream|gelato|sorbet|parfait|trifle|doughnut|donut|croissant|strudel|crepe|biscuit|scone|macaron|meringue|chocolate|cocoa|caramel|vanilla|sweet|sugar|dessert|fruit salad|compote|jam|syrup|frosting|icing"""

    df["dessert"] = (
        df.title.str.contains(deserts_str) | df.ingredients.str.contains(deserts_str)
    ) & ~(df["with_fish"] | df["with_meat"])

    df["diet_pref"] = np.select(
        condlist=[
            df["with_meat"],
            ~df["with_meat"] & (df["with_fish"] | df["with_shellfish"]),
            ~df["with_meat"] & ~df["with_fish"] & ~df["with_shellfish"],
            ~df["with_meat"]
            & ~df["with_fish"]
            & ~df["with_shellfish"]
            & ~df["with_dairy"]
            & ~df["with_honey"],
        ],
        choicelist=["with_meat", "pescetarian", "vegetarian", "vegan"],
        default="omni",
    )
    return df
