import requests
def get_nutrient_info(food_name):
    # API endpoint for the USDA Food Composition Databases
    url = 'https://api.nal.usda.gov/fdc/v1/foods/search'
    # API key (replace with your own if you have one)
    api_key = 'IphEUj1GUJWBEjPhPJRENqRokVbVTtAIoaMcXqdK'
    # Set the serving size to 100 grams
    serving_size = 100
    # Make the API request
    params = {
        'api_key': api_key,
        'query': food_name,
        'pageSize': 1,
    }
    response = requests.get(url, params=params)
    # Parse the API response to get the nutrient information
    if response.status_code == 200:
        data = response.json()
        if 'foods' in data and len(data['foods']) > 0:
            food = data['foods'][0]
            nutrients = food['foodNutrients']
            calories = next((n['value'] for n in nutrients if n['nutrientName'] == 'Energy' and n['unitName'] == 'KCAL'), None)
            fat = next((n['value'] for n in nutrients if n['nutrientName'] == 'Total lipid (fat)' and n['unitName'] == 'G'), None)
            carbs = next((n['value'] for n in nutrients if n['nutrientName'] == 'Carbohydrate, by difference' and n['unitName'] == 'G'), None)
            protein = next((n['value'] for n in nutrients if n['nutrientName'] == 'Protein' and n['unitName'] == 'G'), None)
            vitamins = [n for n in nutrients if 'Vitamin' in n['nutrientName']]
            minerals = [n for n in nutrients if 'Mineral' in n['nutrientName']]
            if calories is not None:
                nutrient_info = f'{food_name.capitalize()} ({serving_size}g):\n' \
                                f'{calories} calories\n' \
                                f'{fat}g fat\n' \
                                f'{carbs}g carbs\n' \
                                f'{protein}g protein\n' \
                                f'Vitamins:\n'
                for v in vitamins:
                    nutrient_info += f'{v["nutrientName"]}: {v["value"]}{v["unitName"]}\n'
                nutrient_info += 'Minerals:\n'
                for m in minerals:
                    nutrient_info += f'{m["nutrientName"]}: {m["value"]}{m["unitName"]}\n'
                return nutrient_info
            else:
                return f'Could not find nutrient information for {food_name.capitalize()}'
        else:
            return f'Could not find {food_name.capitalize()} in the database'
    else:
        return f'Error {response.status_code}: {response.reason}'

food_name="porota"
print(get_nutrient_info(food_name))