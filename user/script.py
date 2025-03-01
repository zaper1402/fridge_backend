#Collumn : Name	Image URL	Time to Cook	Difficulty	Servings	Description	Cuisine Tags	Ingredients	Instructions																	
#Sample Row : Kids Can Make: Strawberry French Toast Roll-Ups	https://d2vsf1hynzxim7.cloudfront.net/production/media/22479/responsive-images/foodnetwork-image-e69cd580-23f3-4388-aa08-539a0ffd3a43___default_283_212.jpeg	1 HRS 5 MINS	EASY	4	These fun, crunchy and sweet roll-ups are the kind of breakfast food that both kids and adults will like. Get kids involved in the cooking. For little and big kids: Let them help with rolling the bread out and filling and coating the roll-ups. For an easy variation, swap out the cream cheese and sugar in the filling for 1/4 cup chocolate-hazelnut spread.	EGG RECIPES, BREAKFAST RECIPES, BRUNCH RECIPES, SCHOOL HOLIDAY RECIPES TO KEEP THE KIDS OCCUPIED, TOAST WITH THE MOST: DELIGHTFUL FRENCH TOAST RECIPES	[Cooking spray], [45g cream cheese, at room temperature], [2 tablespoons plus 100g sugar], [6 slices stale white sandwich bread, crusts removed], [5 or 6 strawberries, diced], [60ml heavy cream], [2 large eggs, beaten], [1 tablespoon ground cinnamon], [Maple syrup, optional]	[  Preheat the oven to 190 degrees C. Line a baking sheet with parchment, and spray the parchment with cooking spray.  ], [Mix together the cream cheese and 2 tablespoons sugar in a small bowl. Roll each slice of bread flat with a rolling pin, and spread with 1 heaping teaspoon of the cream cheese mixture. Place 2 heaping teaspoons of the diced strawberries at one end of each slice. Starting at that end, roll up each slice. Pinch and press the seam and ends so each roll-up is sealed, and push back in any ingredients that may have snuck out of the ends.  ], [Whisk the cream and eggs together in a small bowl. Combine the remaining 100g sugar and the cinnamon in a shallow dish. Dip each roll-up in the egg mixture until completely submerged, shake off excess egg, then cover completely in the cinnamon sugar. Arrange the roll-ups, seam-side down and evenly spaced, on the prepared baking sheet.  ], []																	
#Make a Django model for the data in the excel file and write a script to populate the database with the data from the excel file.
#The script should be able to handle the ingredients and instructions array columns in the excel file.
#The script should be able to handle the image URL column in the excel file.
#The script should be able to handle the cuisine tags column in the excel file.
#The script should be able to handle the difficulty column in the excel file.
#The script should be able to handle the time to cook column in the excel file and covert it into integer minutes.
#The script should be able to handle the servings column in the excel file and save null if unable to parse into integer.
import pandas as pd
import os
from user.models import Meals, Cuisine
from product.models import Product
import re
import random
from django.conf import settings
from django.db.models import Q



def populate_recipes_db(sheet_count):    
    excel_path = '/home/auriga/Downloads/recipes_with_ingredients1.xlsx'
    cuisine = Cuisine.objects.all().values('id', 'name')
    cuisine_dict = {item['name']:item['id'] for item in cuisine}
    create_list = []
    error_list = []
    df = pd.read_excel(excel_path, sheet_name=sheet_count)
    total_rows = df.shape[0]
    # print(df)

    for index, row in df.iterrows():
        try:
            diff = 1
            if row['Difficulty'] == 'VERY EASY':
                diff = 1
            if row['Difficulty'] == 'EASY':
                diff = 2
            if row['Difficulty'] == 'MEDIUM':
                diff = 3
            if row['Cuisine'] and row['Cuisine'] != 'All':
                category_id = parse_category(row['Cuisine'], cuisine_dict)

                obj = {
                    'image_url': row['Image URL'],
                    'name':row['Name'],
                    'category_id':category_id or None,
                    'recipe_time': convert_time_to_minutes(row['Time to Cook']),
                    'recipe_type': diff,
                    'steps': parse_instructions(row['Instructions']),
                    'details': row['Description'],
                    'servings': convert_to_int(row['Servings']),
                    'ingredients': parse_ingredients(row['Ingredient only']),
                    'meal_type':sheet_count+1
                }
                print(obj)
                create_list.append(Meals(**obj))

            total_rows = total_rows-1
            print(total_rows)
        except Exception as e:
            print(f"Error creating recipe: {row['Name']} => {e}")
            error_list.append({"row":row['Name'], "error":e})
            continue
        # recipe.save()
    print(create_list)
    if create_list:
        Meals.objects.bulk_create(create_list, ignore_conflicts=True)
    print(error_list)


def parse_category(data, cuisine_dict):
    item = data.split(",")
    return cuisine_dict.get(item[0], '')    

def convert_time_to_minutes(time):
    try:
        time = time.split(' ')
        minutes = 0
        for i in range(0, len(time), 2):
            if time[i+1] == 'HRS':
                minutes += int(time[i]) * 60
            else:
                minutes += int(time[i])
        
        if minutes == 0:
            return None
        return minutes
    except:
        return None

def convert_to_int(value):
    try:
        return int(value)
    except:
        return None
    
def parse_ingredients(ingredients):
    processed_ingredients = ingredients.replace('[', '').replace(']', '')
    parent_list = {}
    for item in processed_ingredients.split(','):
        words = item.strip()
        item1 = Product.objects.filter(name=words).first()
        if item1:
            parent_list[item1.id] = {'id':item1.id, "name":item}
    return list(parent_list.values())


def parse_instructions(instructions : str):
    #Sample data
    # [1. Bring 3 1/2 cups water and 1/2 teaspoon salt to a boil in a medium saucepan. Reduce the heat to medium-low and stir in the oats. Cook, stirring frequently, until the oats are creamy and tender, 5 to 6 minutes. Remove the saucepan from the heat, cover and rest until the oatmeal thickens slightly, for about 2 minutes.]
    # Expected Output : 
    # [ '1. Bring 3 1/2 cups water and 1/2 teaspoon salt to a boil in a medium saucepan', 'Reduce the heat to medium-low and stir in the oats', 'Cook, stirring frequently, until the oats are creamy and tender, 5 to 6 minutes', 'Remove the saucepan from the heat, cover and rest until the oatmeal thickens slightly, for about 2 minutes'] 
    #Remove all number followed by a dot
    instructions = re.sub(r'\d+\.', '', instructions)
    #Remove all square brackets
    instructions = instructions.replace('[', '').replace(']', '')
    #return JSONArray split by dot and strip whitespace
    return [step.strip(',').strip() for step in instructions.split('.') if step and len(step.strip()) > 3]