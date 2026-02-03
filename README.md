# 🥗 NutriTrack

NutriTrack is a comprehensive **meal planning and nutrition tracking web application** built with **Django**. It helps users manage recipes, plan meals across different slots (including pre- and post-workout), automatically generate shopping lists, and track daily nutritional intake against personalized goals.

---

## 🚀 Features

### 🍽 Recipe & Ingredient Management
- Detailed ingredient database
- Nutritional values per 100g:
  - Calories
  - Protein
  - Carbohydrates
  - Fats
  - Fiber

### 💪 Protein Alternatives
- Support for protein-rich ingredients
- Protein quality scoring
- Suggested alternative protein sources

### 🗓 Flexible Meal Planning
- Plan meals by **day and slot**
- Supported slots:
  - Breakfast
  - Lunch
  - Dinner
  - Snack
  - Pre-Workout
  - Post-Workout

### 🛒 Automated Shopping Lists
- Auto-generated shopping lists from meal plans
- Aggregated ingredient quantities
- Eliminates manual grocery planning

### 📊 Nutrition Dashboard
- Set daily nutrition goals
- Track calories & macronutrients
- Automatic remaining balance calculation

---

## 🛠 Tech Stack

- **Backend**: Django (>= 5.0)
- **Language**: Python
- **Database**: SQLite

---

## 📁 Project Structure

```text
NUTRITRACK/
│
├── .venv/                     # Virtual environment
│
├── meal_planner/
│   │
│   ├── meal_planner/          # Core Django project settings
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   │
│   ├── meal_plans/            # Meal scheduling logic
│   │   ├── migrations/
│   │   ├── templatetags/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── nutrients/             # Nutrition goals & intake tracking
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── recipes/               # Ingredients & recipes management
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── shopping_list/         # Automated shopping list generation
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── static/
│   │   └── css/
│   │       └── styles.css     # Global styles
│   │
│   ├── templates/             # HTML templates
│   │   ├── meal_plans/
│   │   ├── nutrients/
│   │   ├── recipes/
│   │   ├── shopping_list/
│   │   ├── base.html
│   │   └── index.html
│   │
│   ├── create_sample_data.py  # Script to seed sample data
│   └── db.sqlite3             # SQLite database
⚙️ Installation
1️⃣ Clone the Repository
git clone <your-repo-url>
cd NUTRITRACK
2️⃣ Install Dependencies
pip install -r meal_planner/requirements.txt
3️⃣ Apply Migrations
python meal_planner/manage.py migrate
▶️ Usage
🌱 Seed Sample Data
Populate the database with sample ingredients, recipes, and default nutrition goals:

python meal_planner/create_sample_data.py
Creates:

Default nutrition goals (e.g. 2200 kcal, 150g protein)

Sample recipes like:

Grilled Chicken Breast with Quinoa

Tofu Stir-Fry

🖥 Start the Development Server
python meal_planner/manage.py runserver
🌐 Access the App
Open your browser and go to:

http://127.0.0.1:8000
📌 Notes
Modular Django architecture

Easy to extend with authentication, charts, or APIs

Ideal for fitness-focused nutrition tracking

📄 License
This project is intended for educational and personal use.
