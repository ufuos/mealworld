🧠 Project Nexus Documentation

Repository:** [`alx-project-nexus`](https://github.com/ufuos/alx-project-nexus)  

---
🥘 MealWorld — Global Meal Marketplace

ALX Final Capstone Project | Project Nexus

<p align="center"> <img src="https://dummyimage.com/1200x300/000/fff&text=MealWorld+-+Global+Meal+Marketplace" /> </p> <p align="center"><b>Your global gateway to discovering delicious meals, low-calorie options, and cultural cuisines.</b></p>
🏷️ Badges
<p align="left"> <img src="https://img.shields.io/badge/Django-4.2-green?logo=django" /> <img src="https://img.shields.io/badge/Python-3.10-blue?logo=python" /> <img src="https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql" /> <img src="https://img.shields.io/badge/Docker-ready-blue?logo=docker" /> <img src="https://img.shields.io/badge/License-MIT-yellow" /> <img src="https://img.shields.io/badge/CI/CD-GitHub%20Actions-black?logo=githubactions" /> </p>
🌍 About MealWorld

MealWorld is a global meal marketplace built as part of the ALX Final Capstone Project – Project Nexus.

It enables users to:

🍽️ Browse meals across global categories
🔥 View low-calorie & healthy meals
🛍️ Add meals to cart
🔐 Authenticate securely
🧾 Manage orders
🌱 Explore curated dietary categories

The platform is powered by the E-Commerce Backend — ProDev BE, fully included in this repository.

🧠 Project Nexus

This repository includes two major deliverables:

1️⃣ MealWorld — E-Commerce Web Application

A complete global meal marketplace.

2️⃣ Project Nexus Documentation

A summary of backend engineering principles learned during ALX ProDev.

📦 Repository Structure
alx-project-nexus/
├── backend/        # Django + DRF mealworld backend (main project)
├── frontend/       # Optional frontend (React or Django templates)
├── docs/           # Project Nexus documentation
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md

🥗 Sample Meal Categories & Slugs
Category Name	Slug
African Dishes	african-dishes
Italian Cuisine	italian-cuisine
Chinese Meals	chinese-meals
Continental Breakfast	continental-breakfast
Low-Calorie Meals	low-calories
Vegan Meals	vegan-meals
Grill & BBQ	grill-bbq
Seafood Specials	seafood-specials
Soups & Stews	soups-stews
Healthy Smoothies	healthy-smoothies

These can be added via fixtures, Django Admin, or migration seeds.

🎯 Backend Overview — E-Commerce Backend (ProDev BE)

MealWorld runs on a real-world inspired backend with features such as:

🔐 Authentication

JWT-based login, registration, and token refresh

🥙 Meal Management

CRUD operations

Price, calories, availability

Category assignment

Image uploads

🔍 Search & Filter

Filter by category

Filter low-calorie meals

Sort by price

Pagination

📦 Orders

Create orders

Manage order items

Track order history

📘 Documentation

Swagger UI

DRF Schema

🧱 Project Goals
Goal	Description
CRUD APIs	Meals, categories, users, orders
Filtering	By calories, price, category
Pagination	Efficient browsing
Optimization	Indexing & performance tuning
API Docs	Swagger UI
⚙️ Technologies Used
Category	Tools
Backend	Django, Django REST Framework
Database	PostgreSQL
Authentication	JWT
Documentation	Swagger / drf-yasg
Testing	Postman, DRF Tests
CI/CD	GitHub Actions
Deployment	Docker, Render-ready
Version Control	Git & GitHub
🧩 Commit Workflow Example
feat: setup Django with PostgreSQL
feat: add JWT authentication
feat: add meal & category CRUD
feat: integrate Swagger UI
perf: add DB indexing for calories & price
docs: update API documentation

📘 Example API Endpoints
Endpoint	Method	Description
/api/auth/register/	POST	Register
/api/auth/login/	POST	Login
/api/meals/	GET/POST	List or create meals
/api/meals/<id>/	PUT/DELETE	Update/delete meal
/api/meals/?category=low-calories	GET	Filter
/api/meals/?sort=price	GET	Sort
/api/meals/?page=2	GET	Pagination
🧪 Swagger UI Setup
# settings.py
INSTALLED_APPS = [
    ...,
    'rest_framework',
    'drf_yasg',
]

# urls.py
schema_view = get_schema_view(
    openapi.Info(
        title="MealWorld E-Commerce API",
        default_version="v1",
        description="Backend powering the MealWorld global meal marketplace",
    ),
    public=True,
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
]

🚀 Getting Started
🔧 Prerequisites

Python 3.10+

PostgreSQL

Docker & Docker Compose

Git

📦 Installation
git clone https://github.com/ufuos/alx-project-nexus.git
cd alx-project-nexus

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

🧩 Environment Variables (.env)
DEBUG=True
SECRET_KEY=your_secret_key
ALLOWED_HOSTS=localhost,127.0.0.1

DATABASE_NAME=mealworld_db
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_HOST=db
DATABASE_PORT=5432

ACCESS_TOKEN_LIFETIME=60
REFRESH_TOKEN_LIFETIME=1440

🐳 Docker Deployment
Dockerfile

(clean, production-ready — unchanged)

docker-compose.yml

(unchanged but cleaned — no duplicates)

Run:

docker-compose up --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --noinput


Swagger UI:
👉 http://localhost:8000/swagger/

⚙️ CI/CD — GitHub Actions

Includes:

Django tests workflow

Docker image build workflow

(Existing configs remain valid and non-duplicated)

🖥️ Frontend Documentation
Option A — React Frontend

Pages: meals, filters, cart, orders

Uses JWT auth

Folders: pages/, components/, context/, api/

Option B — Django Templates

Simple, fast, DRF-powered HTML UI

🤝 Contributing

Contributions, feature requests, and issues are welcome.

🧾 License

MIT License.

💬 Acknowledgments

Empowering backend excellence through MealWorld — Your Global Meal Marketplace 🌍🍴