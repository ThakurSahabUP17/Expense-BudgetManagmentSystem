# Expense & Budget Manager

A small Django project for keeping track of personal income, expenses and monthly budgets.

I made this project for a college micro-project, so the code is kept fairly simple and easy to follow.

## What it can do

- Create a user account and login with a password
- Show a personal dashboard after login
- Add, edit and delete expenses
- Add, edit and delete income
- Set and track monthly budgets
- Filter expenses and income by month/category
- Show simple charts for income and spending
- Keep each user's records separate

## Tech used

- Python
- Django
- SQLite
- HTML and CSS
- JavaScript
- Chart.js

## Run it on your computer

1. Clone the repository.

```bash
git clone https://github.com/your-username/ExpenseBudgetSystem.git
cd ExpenseBudgetSystem/expense_manager
```

2. Create and activate a virtual environment.

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Mac/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install the packages.

```bash
pip install -r requirements.txt
```

4. Create the database.

```bash
python manage.py migrate
```

5. Start the server.

```bash
python manage.py runserver
```

6. Open this in your browser:

`http://127.0.0.1:8000/`

## First use

Open the Register page and create your own account. After login, the dashboard is ready to use.

## GitHub note

The local database, virtual environment and Python cache files are not included in GitHub. They are listed in `.gitignore`.

For a real production website, `DEBUG` should be turned off and the Django secret key should be kept in environment variables.
