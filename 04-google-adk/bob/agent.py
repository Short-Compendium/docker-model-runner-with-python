import os
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm


os.environ["OPENAI_API_KEY"] = "tada"
os.environ["OPENAI_API_BASE"] = f"{os.environ.get('DMR_BASE_URL')}/engines/llama.cpp/v1"

pizza_ingredients = {
    # Base ingredients
    "pizza_dough": 2.50,
    "pizza_sauce": 1.80,
    "tomato_sauce": 1.50,
    "white_sauce": 2.20,
    "pesto_sauce": 3.50,
    "bbq_sauce": 2.00,
    
    # Cheeses
    "mozzarella_cheese": 4.50,
    "parmesan_cheese": 6.80,
    "cheddar_cheese": 4.20,
    "goat_cheese": 7.50,
    "ricotta_cheese": 3.80,
    "feta_cheese": 5.20,
    "gorgonzola_cheese": 6.50,
    "provolone_cheese": 5.80,
    
    # Meats
    "pepperoni": 5.50,
    "italian_sausage": 6.20,
    "ground_beef": 7.80,
    "ham": 6.50,
    "bacon": 7.20,
    "chicken_breast": 8.50,
    "prosciutto": 12.00,
    "salami": 6.80,
    "chorizo": 7.50,
    "turkey": 7.00,
    
    # Vegetables
    "mushrooms": 3.20,
    "bell_peppers": 2.80,
    "red_onions": 1.50,
    "black_olives": 3.50,
    "green_olives": 3.80,
    "tomatoes": 2.50,
    "cherry_tomatoes": 3.80,
    "spinach": 2.20,
    "arugula": 4.50,
    "basil": 3.50,
    "oregano": 2.80,
    "garlic": 1.20,
    "red_pepper_flakes": 2.50,
    "jalapenos": 2.80,
    "pineapple": 3.20,
    "artichokes": 4.80,
    "sun_dried_tomatoes": 5.50,
    "roasted_peppers": 4.20,
    "capers": 6.20,
    "corn": 2.50,
    "broccoli": 3.00,
    "zucchini": 2.80,
    "eggplant": 3.50,
    
    # Specialty items
    "anchovies": 5.80,
    "pine_nuts": 8.50,
    "fresh_mozzarella": 6.80,
    "buffalo_mozzarella": 9.50,
    "truffle_oil": 15.00,
    "balsamic_glaze": 4.50,
    "olive_oil": 3.80,
    "eggs": 2.50,
    "avocado": 4.20,
    "cilantro": 2.80,
    "lime": 1.50,
    "lemon": 1.80,
    "thyme": 3.20,
    "rosemary": 3.50,
    "sage": 4.00
}

# Create a pizza as a dictionary
my_pizza = {}

# Pizza management with dictionary (no class)
def add_ingredient(ingredient_name, quantity=1.0):
    """
    Add an ingredient to the pizza dictionary
    Args:
        pizza (dict): The pizza dictionary to modify
        ingredient_name (str): Name of the ingredient
        quantity (float): Quantity to add (default: 1.0)
    Returns:
        bool: True if successful, False if ingredient not found
    """
    ingredient_name = ingredient_name.lower().strip()
    
    # Check if ingredient exists in our dictionary
    if ingredient_name not in pizza_ingredients:
        print(f"Error: '{ingredient_name}' not found in ingredients list")
        return False
    
    unit_price = pizza_ingredients[ingredient_name]
    total_price = unit_price * quantity
    
    # If ingredient already exists, add to existing quantity
    if ingredient_name in my_pizza:
        old_quantity = my_pizza[ingredient_name]['quantity']
        new_quantity = old_quantity + quantity
        my_pizza[ingredient_name] = {
            'quantity': new_quantity,
            'unit_price': unit_price,
            'total_price': unit_price * new_quantity
        }
        print(f"Added {quantity} more {ingredient_name} (total: {new_quantity})")
    else:
        my_pizza[ingredient_name] = {
            'quantity': quantity,
            'unit_price': unit_price,
            'total_price': total_price
        }
        print(f"Added {quantity} {ingredient_name}")
    




# Function to search ingredients by name
def search_ingredient_by_name(name: str):
    """
    Search for an ingredient by exact name match
    Returns the price if found, None if not found
    """
    name = name.lower().strip()
    return pizza_ingredients.get(name)


root_agent = Agent(
    model=LiteLlm(model="openai/ai/qwen2.5:latest"),
    name="bob_agent",
    description=(
        """
        Bob agent is a pizza expert.
        """
    ),
    instruction="""
    You are Bob, a a pizza expert. 
    Use the tools provided to interact with users.
    You can search for ingredients by name.
    """,
    tools=[
        search_ingredient_by_name,
    ],

)


