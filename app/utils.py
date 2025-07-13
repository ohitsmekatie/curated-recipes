import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials

SHEET_ID = "1eEixN5MuUJs1O2XYK1jQNaVcyQ30lw8AXMlwoFTqtgM"
TAB_MAPPING = {
    "breakfast": "Breakfast",
    "lunch": "Lunch",
    "dinner": "Dinner",
    "snacks": "Snacks"
}

def get_random_recipe(tab_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SHEET_ID)
    worksheet = sheet.worksheet(TAB_MAPPING[tab_name.lower()])
    data = worksheet.get_all_records()
    if not data:
        return {"name": "No recipes found", "link": "#"}
    recipe = random.choice(data)
    return {"name": recipe["Name"], "link": recipe["Recipe Link"]}


def add_recipe_to_sheet(meal_type, name, link):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
        client = gspread.authorize(creds)

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

