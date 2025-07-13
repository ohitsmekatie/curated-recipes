import os
import json
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheet setup
SHEET_ID = "1eEixN5MuUJs1O2XYK1jQNaVcyQ30lw8AXMlwoFTqtgM"

TAB_MAPPING = {
    "breakfast": "Breakfast",
    "lunch": "Lunch",
    "dinner": "Dinner",
    "snacks": "Snacks"
}

# Create gspread client using env var
def get_gspread_client():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds_dict = json.loads(os.environ["GOOGLE_CREDS"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    return gspread.authorize(creds)

# Fetch a random recipe from the sheet based on tab
def get_random_recipe(tab_name):
    try:
        client = get_gspread_client()
        sheet = client.open_by_key(SHEET_ID)
        worksheet = sheet.worksheet(TAB_MAPPING[tab_name.lower()])
        data = worksheet.get_all_records()

        if not data:
            return {"name": "No recipes found", "link": "#"}

        recipe = random.choice(data)
        return {
            "name": recipe.get("Name", "Unnamed"),
            "link": recipe.get("Recipe Link", "#")
        }

    except Exception as e:
        print(f"Error fetching recipe: {e}")
        return {"name": "Error fetching recipe", "link": "#"}

# Add a new recipe to the appropriate tab
def add_recipe_to_sheet(meal_type, name, link):
    try:
        client = get_gspread_client()
        sheet = client.open_by_key(SHEET_ID)
        tab_name = TAB_MAPPING.get(meal_type.lower())

        if not tab_name:
            return False

        worksheet = sheet.worksheet(tab_name)
        worksheet.append_row([name, link])
        return True

    except Exception as e:
        print(f"Error appending to sheet: {e}")
        return False
