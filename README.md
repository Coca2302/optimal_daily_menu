# 🥗 Optimal Daily Menu

## 📌 Project Overview

The **Optimal Daily Menu** project aims to create a balanced and cost-effective daily meal plan that meets nutritional requirements while minimizing expenses.  
It uses **linear programming** with the **Gurobi optimization library** to select a set of foods that satisfy:

- Predefined **nutritional constraints**
- A maximum **daily food weight**
- A fixed **number of dishes**

---

## 🎯 Problem Definition

Design a daily menu for a **student** seeking a healthy diet under financial constraints. The menu must:

- ✅ Meet **minimum and maximum nutritional requirements** (e.g., vitamins, minerals, macronutrients)
- ⚖️ Limit the **total food weight** to **2000 grams/day**
- 🍽️ Include **exactly 12 distinct dishes**
- 💸 **Minimize total cost**

---

## 🧾 Dependencies

- Python 3.x
- [Gurobi Optimizer](https://www.gurobi.com/) (`gurobipy`)
- `pandas`
- `numpy`
- `seaborn` (for visualization)
- `csv` (standard library)

Install all Python packages using:

```bash
pip install gurobipy pandas numpy seaborn
```

> 📌 Make sure you have a valid **Gurobi license** and installation.

---

## 📁 Project Structure

```
optimal-daily-menu/
│
├── main.py                  # Main script: model, preprocessing, optimization
├── price.csv                # Price data for food items
├── food.csv                 # Nutritional data for food items
├── matched_data.csv         # Output: merged food + price data
└── README.md
```

---

## 🚀 How to Run

1. Make sure `price.csv` and `food.csv` are in the same directory as `main.py`.

2. Run the optimization script:

```bash
python main.py
```

The script will:

- ✅ Load and merge nutrition + price data
- 🧹 Filter out unwanted food items
- 🧠 Formulate the linear programming model
- 🔧 Solve using **Gurobi**
- 📤 Output selected food items to the console and optionally a file

---

## 📐 Model Details

### 🔢 Variables

- `x[i]`: Binary — whether food item *i* is selected (1) or not (0)
- `q[i]`: Integer — quantity of food item *i* (either 1 or 2 portions)

### 🎯 Objective Function

Minimize total cost:

\[
\min \sum_{i=1}^n p_i \cdot x_i \cdot q_i
\]

Where:

- \( p_i \): price of food item \( i \)

### 🔒 Constraints

- **Nutritional constraints** (for each nutrient \( j \)):

\[
\text{lb}_j \leq \sum_{i=1}^n \text{nutrition}[i][j] \cdot x_i \cdot q_i \leq \text{ub}_j
\]

- **Total weight constraint**:

\[
\sum_{i=1}^n x_i \cdot q_i \cdot w_i \leq 2000
\]

- **Dish count constraint**:

\[
\sum_{i=1}^n x_i = 12
\]

---

## 🧹 Data Preprocessing

- Filters out food items with names containing:
  - `"RAW"`, `"GROUND"`, `"SPICES"`, `"FRSH"`, `"FAST FOOD"`
- Excludes categories such as:
  - Fast food, candies, snacks, infant formulas
- Matches and merges data from `price.csv` and `food.csv`
- Saves merged dataset to `matched_data.csv`

---

## 📊 Results

If an optimal solution is found, the script outputs a table of **selected foods** with:

- 📝 **Description**: Name of food
- ⚖️ **Weight**: Per portion (grams)
- 💰 **Price**: Cost per portion
- 🔢 **Quantity**: Number of portions (1 or 2)

If no feasible solution is found, an error message will be shown.

