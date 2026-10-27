# FoodExpress

Online food ordering and delivery system (Flask + MySQL + vanilla JS).

## Setup (Windows, VS Code)

1. `python -m venv venv`
2. `venv\Scripts\activate`
3. `pip install -r requirements.txt`
4. In MySQL: `CREATE DATABASE foodexpress_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`
5. `copy .env.example .env` and put your MySQL password in `.env`
6. `python app.py` then open http://localhost:5000
7. Check the database connection at http://localhost:5000/health/db

## Status

Phase 1 complete: project structure, Flask config, MySQL connection, homepage.
Phase 2 complete: database tables, register, login, logout, admin account.
Phase 3 complete: admin panel (add, edit, delete restaurants and menu items) and public restaurant pages.

## Phase 2 commands

```
flask db init
flask db migrate -m "create tables"
flask db upgrade
python create_admin.py
python app.py
```
