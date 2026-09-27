# Expense Tracker 💰

A full-stack expense tracking app that lets you log, view, and analyze your spending — with proper login/signup so your data stays yours.

I built this to actually understand where my money goes each month instead of guessing at it. It's got a Flask + MySQL backend handling the data and auth, and a Streamlit frontend for the actual dashboard/UI.

## What it does

- Register and log in securely (JWT-based auth, passwords are hashed, not stored in plain text)
- Add expenses with a title, category, and amount
- View all your expenses with filters — search by title, filter by category, filter by amount range or date
- Update or delete any expense
- Dashboard with a quick summary: total spent, expense count, category-wise pie/bar charts, and a monthly spending trend chart

## Tech stack

- **Backend:** Python, Flask, MySQL, Flask-SQLAlchemy, Flask-JWT-Extended
- **Frontend:** Streamlit, Plotly (for charts), Pandas
- **Auth:** JWT access + refresh tokens, passwords hashed with Werkzeug

## Project structure

```
expense_tracker/
├── backend/
│   ├── app/
│   │   ├── __init__.py       # app factory, config, blueprint registration
│   │   ├── extensions.py     # db, jwt instances
│   │   ├── models.py         # User and Expense models
│   │   ├── auth/routes.py    # register, login, refresh, me
│   │   └── expenses/routes.py # CRUD routes for expenses
│   ├── run.py
│   ├── requirements.txt
│   └── .env                  # not committed — see setup below
└── frontend/
    ├── app.py                # the Streamlit app
    └── requirements.txt
```

## Running it locally

You'll need Python installed, and a MySQL server running locally (or update the connection string to point wherever your DB lives).

### 1. Clone the repo
```bash
git clone https://github.com/KPAVAN602/expense-tracker.git
cd expense-tracker
```

### 2. Set up the backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # on Windows
pip install -r requirements.txt
```

Create a `.env` file inside `backend/` with:
```
DATABASE_URL=mysql+pymysql://root:yourpassword@localhost/expense_tracker
JWT_SECRET_KEY=some-random-secret-string
```

Then run it:
```bash
python run.py
```
This starts the Flask API on `http://127.0.0.1:5000`.

### 3. Set up the frontend
Open a second terminal:
```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```
This opens the app in your browser, usually at `http://localhost:8501`.

## A few notes if you're poking around the code

- Expense ownership is enforced on the backend — one user can't view/edit/delete another user's expenses, even if they guess an ID.
- Amounts, categories, and titles are all validated before hitting the database (no negative amounts, no empty fields).
- The frontend keeps the JWT in Streamlit's session state, so refreshing the page mid-session won't log you out, but closing the tab will.

# Expense Tracker 💰

A full-stack expense tracking app that lets you log, view, and analyze your spending — with proper login/signup so your data stays yours.

I built this to actually understand where my money goes each month instead of guessing at it. It's got a Flask + MySQL backend handling the data and auth, and a Streamlit frontend for the actual dashboard/UI.

## What it does

- Register and log in securely (JWT-based auth, passwords are hashed, not stored in plain text)
- Add expenses with a title, category, and amount
- View all your expenses with filters — search by title, filter by category, filter by amount range or date
- Update or delete any expense
- Dashboard with a quick summary: total spent, expense count, category-wise pie/bar charts, and a monthly spending trend chart

## Tech stack

- **Backend:** Python, Flask, MySQL, Flask-SQLAlchemy, Flask-JWT-Extended
- **Frontend:** Streamlit, Plotly (for charts), Pandas
- **Auth:** JWT access + refresh tokens, passwords hashed with Werkzeug

## Project structure

```
expense_tracker/
├── backend/
│   ├── app/
│   │   ├── __init__.py       # app factory, config, blueprint registration
│   │   ├── extensions.py     # db, jwt instances
│   │   ├── models.py         # User and Expense models
│   │   ├── auth/routes.py    # register, login, refresh, me
│   │   └── expenses/routes.py # CRUD routes for expenses
│   ├── run.py
│   ├── requirements.txt
│   └── .env                  # not committed — see setup below
└── frontend/
    ├── app.py                # the Streamlit app
    └── requirements.txt
```

## Running it locally

You'll need Python installed, and a MySQL server running locally (or update the connection string to point wherever your DB lives).

### 1. Clone the repo
```bash
git clone https://github.com/KPAVAN602/expense-tracker.git
cd expense-tracker
```

### 2. Set up the backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # on Windows
pip install -r requirements.txt
```

Create a `.env` file inside `backend/` with:
```
DATABASE_URL=mysql+pymysql://root:yourpassword@localhost/expense_tracker
JWT_SECRET_KEY=some-random-secret-string
```

Then run it:
```bash
python run.py
```
This starts the Flask API on `http://127.0.0.1:5000`.

### 3. Set up the frontend
Open a second terminal:
```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```
This opens the app in your browser, usually at `http://localhost:8501`.

## A few notes if you're poking around the code

- Expense ownership is enforced on the backend — one user can't view/edit/delete another user's expenses, even if they guess an ID.
- Amounts, categories, and titles are all validated before hitting the database (no negative amounts, no empty fields).
- The frontend keeps the JWT in Streamlit's session state, so refreshing the page mid-session won't log you out, but closing the tab will.

## About me

I'm Pavan Kalyan K, and I built this to get real practice with backend fundamentals — not just following a tutorial, but actually designing the pieces myself: a Flask API with proper blueprint structure, JWT-based auth with access and refresh tokens, a MySQL schema linking users to their own data, and input validation on every route before it touches the database.

Skills this project put to work: Python, Flask, SQLAlchemy, MySQL, REST APIs, JWT authentication, and connecting it all to a Streamlit frontend.

📧 [kpavankalyan648@gmail.com](mailto:kpavankalyan648@gmail.com)
🔗 [GitHub](https://github.com/KPAVAN602) · [LinkedIn](https://linkedin.com/in/komkonipavan)
