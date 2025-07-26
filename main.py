#!/usr/bin/env python
# coding: utf-8

#  HEALTHY DIET PROBLEM IN LINEAR PROGRAMING
#  1. Problem Defination:

# 2. Import library:

# In[4]:


import pandas as pd
import gurobipy as gp
from gurobipy import GRB
import numpy as np
import csv
import time
import seaborn as sns


# 3. Collect data:

# In[6]:


price_dict = {}
with open('price.csv', 'r', encoding='utf-8-sig') as price_file:
    price_reader = csv.reader(price_file)
    for row in price_reader:
        if len(row) >= 2:
            description = row[0].strip('"')
            price = float(row[2])
            price_dict[description] = price

matched_data = []
with open('food.csv', 'r', encoding='utf-8-sig') as food_file:
    food_reader = csv.DictReader(food_file)
    for row in food_reader:
        description = row['Description']
        if description in price_dict:
            row['Price'] = price_dict[description]
            matched_data.append(row)

fieldnames = food_reader.fieldnames + ['Price']
with open('matched_data.csv', 'w', newline='', encoding='utf-8') as output_file:
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(matched_data)

print("Matching and writing complete.")


# In[7]:


food_data = pd.read_csv('matched_data.csv')
print(food_data.shape)
food_data = food_data.dropna()
print(food_data.shape)


# In[8]:


food_data.head()


# Attribute: Unit
# 
# 1.Ash: g
# 2.Alpha Carotene: µg
# 3.Beta Carotene: µg
# 4.Beta Cryptoxanthin: µg
# 5.Carbohydrate: g
# 6.Cholesterol: mg
# 7.Choline: mg
# 8.Fat.Monosaturated Fat: g
# 9.Fat.Polysaturated Fat: g
# 10.Fat.Saturated Fat: g
# 11.Fat.Total Lipid: g
# 12.Fiber: g
# 13.Household Weights.1st Household Weight: g
# 14.Kilocalories: kcal
# 15.Lutein and Zeaxanthin: µg
# 16.Lycopene: µg
# 17.Major Minerals.Calcium: mg
# 18.Major Minerals.Copper: mg
# 19.Major Minerals.Iron: mg
# 20.Major Minerals.Magnesium: mg
# 21.Major Minerals.Phosphorus: mg
# 22.Major Minerals.Potassium: mg
# 23.Major Minerals.Sodium: mg
# 24.Major Minerals.Zinc: mg
# 25.Manganese: mg
# 26.Niacin: mg
# 27.Pantothenic Acid: mg
# 28.Protein: g
# 29.Refuse Percentage: % by volume
# 30.Retinol: µg
# 31.Riboflavin: mg
# 32.Selenium: µg
# 33.Sugar Total: g
# 34.Thiamin: mg
# 35.Vitamins.Vitamin A - RAE: µg
# 36.Vitamins.Vitamin B12: µg
# 37.Vitamins.Vitamin B6: µg
# 38.Vitamins.Vitamin C: µg
# 39.Vitamins.Vitamin E: mg
# 40.Vitamins.Vitamin K: µg
# 41.Water: g

# 4. Statistic:

# In[11]:


food_data.head()

print(food_data.describe())

Minerals = ['Data.Major Minerals.Calcium', 'Data.Major Minerals.Copper',
       'Data.Major Minerals.Iron', 'Data.Major Minerals.Magnesium',
       'Data.Major Minerals.Phosphorus', 'Data.Major Minerals.Potassium',
       'Data.Major Minerals.Sodium', 'Data.Major Minerals.Zinc']
Vitamins = ['Data.Vitamins.Vitamin A - IU', 'Data.Vitamins.Vitamin A - RAE',
       'Data.Vitamins.Vitamin B12', 'Data.Vitamins.Vitamin B6',
       'Data.Vitamins.Vitamin C', 'Data.Vitamins.Vitamin E',
       'Data.Vitamins.Vitamin K']

#sns.pairplot(food_data[Minerals])
#sns.pairplot(food_data[Vitamins])


# 5. DATA PREPROCESSING

# In[13]:


sample = food_data[~food_data['Description'].str.contains('RAW', case=False, na=False)]
sample = sample[~sample['Description'].str.contains('GROUND', case=False, na=False)]
sample = sample[~sample['Description'].str.contains('SPICES', case=False, na=False)]
sample = sample[~sample['Description'].str.contains('FRSH', case=False, na=False)]
sample = sample[~sample['Description'].str.contains('FAST FOOD')]
sample = sample[~sample['Category'].isin(['FAST FOOD', 'MCDONALD','BABYFOOD','FASTFOOD','CANDIES','SNACKS','LEAVENING AGENTS',
                                                               'ICE CREAMS','SUGARS','SYRUPS','MCDONALD\'S','BURGER KING','WENDY\'S',
                                                               'Burger king','TACO BELL','FT FDS','FST FOODS','Snacks','INF FORMULA',
                                                               'McDONALD\'S','FAST FD','FT FDS','POPEYES','KENTUCKY FRIED CHICK',
                                                               'INFANT FORMULA','INF FORM','INF FORMMEAD JOHN','CHILD FORMULA',
                                                               'INF FOR','INF FO','INF FORMU','INF FOR NUTR','Infa for','Babyfood',
                                                                'No Category',
                                                               ])]


# 6. Modeling

# In[15]:


lb_nutrition = {
    "Data.Alpha Carotene": 21.6,
    "Data.Ash": 0,
    "Data.Beta Carotene": 21.6,
    "Data.Beta Cryptoxanthin": 20,
    "Data.Carbohydrate": 500,
    "Data.Cholesterol": 0,
    "Data.Choline": 550,
    "Data.Fiber": 25,
    "Data.Kilocalories": 2500,
    "Data.Lutein and Zeaxanthin": 10,
    "Data.Lycopene": 10,
    "Data.Manganese": 2.3,
    "Data.Niacin": 16,
    "Data.Pantothenic Acid": 5,
    "Data.Protein": 60,
    "Data.Refuse Percentage": 0,
    "Data.Retinol": 0.9,
    "Data.Riboflavin": 1.3,
    "Data.Selenium": 55,
    "Data.Sugar Total": 37.5,
    "Data.Thiamin": 1.2,
    "Data.Water": 0,
    "Data.Fat.Monosaturated Fat": 44,
    "Data.Fat.Polysaturated Fat": 20,
    "Data.Fat.Saturated Fat": 24,
    "Data.Fat.Total Lipid": 70,
    "Data.Major Minerals.Copper": 0.9,
    "Data.Major Minerals.Calcium": 1300,
    "Data.Major Minerals.Iron": 8,
    "Data.Major Minerals.Magnesium": 420,
    "Data.Major Minerals.Phosphorus": 700,
    "Data.Major Minerals.Potassium": 3500,
    "Data.Major Minerals.Sodium": 1500,
    "Data.Major Minerals.Zinc": 11,
    "Data.Vitamins.Vitamin A - IU": 3000,
    "Data.Vitamins.Vitamin A - RAE": 0.9,
    "Data.Vitamins.Vitamin B12": 2.4,
    "Data.Vitamins.Vitamin B6": 1.3,
    "Data.Vitamins.Vitamin C": 90,
    "Data.Vitamins.Vitamin E": 15,
    "Data.Vitamins.Vitamin K": 120
}

ub_nutrition = {
    "Data.Alpha Carotene": 64.8,
    "Data.Ash": 100,
    "Data.Beta Carotene": 64.8,
    "Data.Beta Cryptoxanthin": 60,
    "Data.Carbohydrate": 1500,
    "Data.Cholesterol": 300,
    "Data.Choline": 1650,
    "Data.Fiber": 75,
    "Data.Kilocalories": 7500,
    "Data.Lutein and Zeaxanthin": 30,
    "Data.Lycopene": 30,
    "Data.Manganese": 6.9,
    "Data.Niacin": 48,
    "Data.Pantothenic Acid": 15,
    "Data.Protein": 180,
    "Data.Refuse Percentage": 100,
    "Data.Retinol": 2.7,
    "Data.Riboflavin": 3.9,
    "Data.Selenium": 165,
    "Data.Sugar Total": 112.5,
    "Data.Thiamin": 3.6,
    "Data.Water": 3700,
    "Data.Fat.Monosaturated Fat": 132,
    "Data.Fat.Polysaturated Fat": 60,
    "Data.Fat.Saturated Fat": 72,
    "Data.Fat.Total Lipid": 210,
    "Data.Major Minerals.Copper": 2.7,
    "Data.Major Minerals.Calcium": 3900,
    "Data.Major Minerals.Iron": 24,
    "Data.Major Minerals.Magnesium": 1260,
    "Data.Major Minerals.Phosphorus": 2100,
    "Data.Major Minerals.Potassium": 10500,
    "Data.Major Minerals.Sodium": 4500,
    "Data.Major Minerals.Zinc": 33,
    "Data.Vitamins.Vitamin A - IU": 9000,
    "Data.Vitamins.Vitamin A - RAE": 2.7,
    "Data.Vitamins.Vitamin B12": 7.2,
    "Data.Vitamins.Vitamin B6": 3.9,
    "Data.Vitamins.Vitamin C": 270,
    "Data.Vitamins.Vitamin E": 45,
    "Data.Vitamins.Vitamin K": 360
}


columns_to_exclude = ['Description', 'Category', 'Data.Household Weights.1st Household Weight Description', 
                      'Data.Household Weights.1st Household Weight', 'Data.Household Weights.2nd Household Weight Description', 
                      'Data.Household Weights.2nd Household Weight','Nutrient Data Bank Number','Price']

nutrition_columns = [col for col in sample.columns if col not in columns_to_exclude]
nutrition = sample[nutrition_columns].values.tolist()
p = sample["Price"].values.tolist()
w = sample['Data.Household Weights.1st Household Weight'].values.tolist()
num_foods = len(p)
num_nutrients = len(nutrition[0])


# initializing the model

# In[ ]:





# In[17]:


model = gp.Model("Food_Selection")
x = model.addVars(num_foods, vtype=GRB.BINARY, name="x")
q = model.addVars(num_foods, vtype=GRB.INTEGER, lb=1,ub=2, name="q")


# 

# Objective function:

# In[20]:


model.setObjective(sum(p[i] * x[i] * q[i] for i in range(num_foods)), GRB.MINIMIZE)


# Constraint:

# In[22]:


for j in range(num_nutrients):
    col_name = nutrition_columns[j]
    if col_name in lb_nutrition:
        print(col_name,lb_nutrition[col_name],ub_nutrition[col_name])
        model.addConstr(sum(nutrition[i][j] * x[i] * q[i] for i in range(num_foods)) >= lb_nutrition[col_name],name = "lb_"+col_name)
        model.addConstr(sum(nutrition[i][j] * x[i] * q[i] for i in range(num_foods)) <= ub_nutrition[col_name]*10,name = "ub_"+col_name)
model.addConstr(sum((x[i]*q[i]*w[i]) for i in range(num_foods)) <= 2000)


# In[23]:


model.addConstr(sum(x[i] for i in range(num_foods)) == 12)


# Solving model

# In[25]:


def result():
    model.optimize()
    if model.status == GRB.OPTIMAL:
        selected_foods = [i for i in range(num_foods) if x[i].x > 0.5]
        selected_food_data = []
        for food in selected_foods:
            selected_food_data.append({
                'Description': sample.iloc[food]['Description'],
                'Weight': sample.iloc[food]['Data.Household Weights.1st Household Weight'],
                'Price': sample.iloc[food]['Price'],
                'Quantity': q[food].x
            })

        selected_food_df = pd.DataFrame(selected_food_data)
        display(selected_food_df)
    else:
        print("No optimal solution found.")

result()   

