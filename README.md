# 🥗 NutriTrack

NutriTrack is a comprehensive **meal planning and nutrition tracking web application** built with **Django**. It helps users manage recipes, plan meals across different time slots (including pre- and post-workout), automatically generate shopping lists, and track daily nutritional intake against personalized goals.

---

## 🚀 Features

### 🍽 Recipe & Ingredient Management
- Maintain a detailed database of ingredients
- Nutritional values per 100g:
  - Calories
  - Protein
  - Carbohydrates
  - Fats
  - Fiber

### 💪 Protein Alternatives
- Dedicated support for protein-rich ingredients
- Protein quality scoring
- Suggested alternative protein sources for dietary flexibility

### 🗓 Flexible Meal Planning
- Plan meals by **day and time slot**
- Supported slots:
  - Breakfast
  - Lunch
  - Dinner
  - Snack
  - Pre-Workout
  - Post-Workout

### 🛒 Automated Shopping Lists
- Auto-generated shopping lists from meal plans
- Aggregates ingredient quantities across all planned meals
- Eliminates manual grocery planning

### 📊 Nutrition Dashboard
- Set personalized daily nutrition goals
- Track:
  - Calories
  - Protein
  - Carbs
  - Fats
- Automatic calculation of consumed vs remaining nutrients

---

## 🛠 Tech Stack

- **Backend**: Django (>= 5.0)
- **Language**: Python
- **Database**: SQLite

---

## 📁 Project Structure

The project is organized into multiple Django apps, each handling a specific responsibility:

```text
meal_planner/
│
├── recipes/        # Categories, ingredients, and recipes
├── meal_plans/     # Daily meal scheduling
├── shopping_list/  # Auto-generated shopping lists
├── nutrients/      # Nutrition goals and intake tracking
⚙️ Installation
1️⃣ Clone the Repository
git clone <your-repo-url>
cd meal_planner
2️⃣ Install Dependencies
pip install -r meal_planner/requirements.txt
3️⃣ Apply Migrations
python meal_planner/manage.py migrate
▶️ Usage
🌱 Seed Sample Data
To populate the app with sample categories, ingredients, recipes, and default nutrition goals, run:

python meal_planner/create_sample_data.py
This script creates:

Default nutrition goals (e.g. 2200 kcal, 150g protein)

Sample recipes like:

Grilled Chicken Breast with Quinoa

Tofu Stir-Fry

🖥 Start the Development Server
Using the helper script:

python meal_planner/start_server.py
Or using the standard Django command:

python meal_planner/manage.py runserver
🌐 Access the Application
Once the server is running, open your browser and visit:

http://127.0.0.1:8000
📌 Notes
Designed for easy extension and customization

Ideal for fitness-focused meal planning and nutrition tracking

Clean modular Django architecture

📄 License
This project is intended for educational and personal use.
