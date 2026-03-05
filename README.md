# student-task-manager
A full-stack task management web application built with Flask, MySQL, and Bootstrap that allows users to manage tasks with authentication, priorities, and status tracking.

# Student Task Manager Web Application

A full-stack task management web application built with Python (Flask) and MySQL, following the MVC design pattern and complete SDLC — from requirements gathering and system design to coding, testing, and deployment.

---

## 📌 Project Overview

This application allows students to register, login, and manage their daily tasks efficiently. It supports full CRUD operations, user authentication, session management, and task prioritization — all built with a clean and responsive UI using Bootstrap.

---

## ⚙️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| Flask | Web framework and REST API |
| MySQL | Database — users and tasks |
| Bootstrap | Frontend UI |
| Werkzeug | Secure password hashing |
| PythonAnywhere | Cloud deployment |

---

## 🔁 Application Workflow

```
User Opens App
      ↓
Register / Login
      ↓
Session Created (Authentication)
      ↓
Dashboard — View All Tasks
      ↓
  ┌───────────────────────────┐
  │  Add Task                 │
  │  Edit Task                │
  │  Delete Task              │
  │  Update Status            │
  └───────────────────────────┘
      ↓
MySQL Database (CRUD Operations)
      ↓
Response Rendered to User
```

---

## 🗂️ Project Structure

```
task_manager/
│
├── app.py              → Main Flask application — all REST API routes
├── schema.sql          → Database schema — run this first
├── requirements.txt    → Project dependencies
│
└── templates/
    ├── base.html       → Base layout template
    ├── login.html      → Login page
    ├── register.html   → Registration page
    ├── dashboard.html  → Main task dashboard
    ├── add_task.html   → Add new task form
    └── edit_task.html  → Edit existing task form
```

---

## 🌐 REST API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home — redirect to login or dashboard |
| GET/POST | `/register` | User registration |
| GET/POST | `/login` | User login with session management |
| GET | `/logout` | Clear session and logout |
| GET | `/dashboard` | View all tasks with stats |
| GET/POST | `/add` | Add new task |
| GET/POST | `/edit/<id>` | Edit existing task |
| GET | `/delete/<id>` | Delete task |
| GET | `/status/<id>/<status>` | Quick status update |

---

## 🗄️ Database Schema

**Users Table** — stores registered users with hashed passwords

**Tasks Table** — stores tasks with title, description, priority, status, due date linked to user

---

## 🚀 How to Run

**Step 1** — Install dependencies
```
pip install -r requirements.txt
```

**Step 2** — Set up the database
```
mysql -u root -p < schema.sql
```

**Step 3** — Update MySQL credentials in `app.py`
```python
app.config['MYSQL_PASSWORD'] = 'your_password'
```

**Step 4** — Run the application
```
python app.py
```

Application available at `http://localhost:5000`

---

## ✨ Features

- User registration and login with **secure password hashing**
- **Session management** — protected routes require login
- Full **CRUD operations** — create, read, update, delete tasks
- Task **priority levels** — High, Medium, Low
- Task **status tracking** — Pending, In Progress, Completed
- **Dashboard statistics** — total, pending, in progress, completed counts
- Tasks sorted by priority and status automatically
- Deployed on **PythonAnywhere** cloud platform

---

## 👨‍💻 Author

**Bestha Bhuvan**
B.Tech CSE (AI & ML) — SVCE Tirupati, 2026
[LinkedIn](https://linkedin.com/in/bhuvan098) | [GitHub](https://github.com/bhuvan098)
