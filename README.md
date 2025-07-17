
# 🏋️‍♂️ Fitness Tracker

A Django-based web application that tracks user fitness profiles and segregates data across **multiple databases** based on **BMI categories** — `Thin`, `Medium`, and `Fat`.

---

## 🔥 Key Features

- 🧑‍⚕️ User profile creation with automatic BMI calculation
- 🧠 Intelligent **Database Routing** using a custom `db_router.py`
- 💾 Multi-Database setup:
  - `fitness_db_thin`
  - `fitness_db_medium`
  - `fitness_db_fat`
- 📃 Django Forms for input validation
- 📊 Admin dashboard for managing user data
- 🌐 Template-based rendering using Django views

---

## 🗂️ Project Structure

```

fitness\_project/
├── tracker/
│   ├── templates/tracker/       # HTML templates
│   ├── **init**.py
│   ├── admin.py                 # Registering models for admin
│   ├── apps.py
│   ├── db\_router.py             # Custom DB router for BMI logic
│   ├── forms.py                 # Forms for profile input
│   ├── models.py                # Profile model with BMI logic
│   ├── tests.py
│   ├── urls.py                  # URL routing
│   └── views.py                 # Handles logic and templates
├── manage.py
├── requirements.txt             # Python dependencies
└── .gitignore

````

---

## ⚙️ Setup Instructions

### 🔧 Prerequisites

- Python 3.8+
- MySQL server
- Virtualenv (recommended)

### 🛠️ Installation

```bash
# Clone the project
git clone https://github.com/your-username/fitness_project.git
cd fitness_project

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
````

### 💾 MySQL Setup

Create **4 databases** in your MySQL server:

* `fitness_db_main`
* `fitness_db_thin`
* `fitness_db_medium`
* `fitness_db_fat`

Then configure your `settings.py` like so:

```python
DATABASES = {
    'default': {},
    'main': { ... },
    'thin': { ... },
    'medium': { ... },
    'fat': { ... }
}
```

### 🧠 Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate --database=main
python manage.py migrate --database=thin
python manage.py migrate --database=medium
python manage.py migrate --database=fat
```

### 🚀 Run the Server

```bash
python manage.py runserver
```

---

## 🧠 How the DB Router Works

The file `db_router.py` contains logic to route each `Profile` object based on its BMI:

```python
if profile.bmi < 18.5:
    return 'thin'
elif 18.5 <= profile.bmi < 25:
    return 'medium'
else:
    return 'fat'
```

This allows better scalability, segmentation, and performance.

---

## ✅ TODO / Future Plans

* Add user authentication (login/signup)
* REST API for mobile integration
* Charts & analytics for fitness trends
* BMI recommendation tips

---

## 🙋‍♂️ Author

**Md Faiyazur Rahman**
🎓 Django Developer | Full Stack Enthusiast
🔗 [GitHub](https://github.com/faiyazzrahman)

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

> *Track smart. Stay fit. Built with Django.*

