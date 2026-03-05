from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)

# ── Secret key for session management ──
app.secret_key = 'your_secret_key_change_in_production'

# ── MySQL Configuration ──
DB_CONFIG = {
    'host'    : 'localhost',
    'user'    : 'root',
    'password': 'Bhuvan11042004',
    'database': 'task_manager_db'
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)


# ─────────────────────────────────────────
#  LOGIN REQUIRED DECORATOR
# ─────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


# ─────────────────────────────────────────
#  HOME
# ─────────────────────────────────────────
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


# ─────────────────────────────────────────
#  REGISTER
# ─────────────────────────────────────────
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        email    = request.form['email'].strip()
        password = request.form['password']

        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return render_template('register.html')

        hashed_pw = generate_password_hash(password)

        conn = get_db()
        cur  = conn.cursor()
        try:
            cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                        (username, email, hashed_pw))
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception:
            flash('Username or email already exists.', 'danger')
        finally:
            cur.close()
            conn.close()

    return render_template('register.html')


# ─────────────────────────────────────────
#  LOGIN
# ─────────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form['email'].strip()
        password = request.form['password']

        conn = get_db()
        cur  = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id']  = user['id']
            session['username'] = user['username']
            flash(f"Welcome back, {user['username']}!", 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html')


# ─────────────────────────────────────────
#  LOGOUT
# ─────────────────────────────────────────
@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


# ─────────────────────────────────────────
#  DASHBOARD
# ─────────────────────────────────────────
@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db()
    cur  = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT * FROM tasks
        WHERE user_id = %s
        ORDER BY
            FIELD(priority, 'High', 'Medium', 'Low'),
            FIELD(status, 'Pending', 'In Progress', 'Completed'),
            created_at DESC
    """, (session['user_id'],))
    tasks = cur.fetchall()
    cur.close()
    conn.close()

    total     = len(tasks)
    pending   = sum(1 for t in tasks if t['status'] == 'Pending')
    progress  = sum(1 for t in tasks if t['status'] == 'In Progress')
    completed = sum(1 for t in tasks if t['status'] == 'Completed')

    return render_template('dashboard.html',
                           tasks=tasks,
                           total=total,
                           pending=pending,
                           progress=progress,
                           completed=completed)


# ─────────────────────────────────────────
#  ADD TASK
# ─────────────────────────────────────────
@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_task():
    if request.method == 'POST':
        title       = request.form['title'].strip()
        description = request.form['description'].strip()
        priority    = request.form['priority']
        due_date    = request.form['due_date'] or None

        if not title:
            flash('Task title is required.', 'danger')
            return render_template('add_task.html')

        conn = get_db()
        cur  = conn.cursor()
        cur.execute("""
            INSERT INTO tasks (user_id, title, description, priority, due_date, status)
            VALUES (%s, %s, %s, %s, %s, 'Pending')
        """, (session['user_id'], title, description, priority, due_date))
        conn.commit()
        cur.close()
        conn.close()

        flash('Task added successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('add_task.html')


# ─────────────────────────────────────────
#  EDIT TASK
# ─────────────────────────────────────────
@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    conn = get_db()
    cur  = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM tasks WHERE id = %s AND user_id = %s",
                (task_id, session['user_id']))
    task = cur.fetchone()

    if not task:
        flash('Task not found.', 'danger')
        cur.close()
        conn.close()
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        title       = request.form['title'].strip()
        description = request.form['description'].strip()
        priority    = request.form['priority']
        status      = request.form['status']
        due_date    = request.form['due_date'] or None

        cur.execute("""
            UPDATE tasks
            SET title=%s, description=%s, priority=%s, status=%s, due_date=%s
            WHERE id=%s AND user_id=%s
        """, (title, description, priority, status, due_date, task_id, session['user_id']))
        conn.commit()
        cur.close()
        conn.close()

        flash('Task updated successfully!', 'success')
        return redirect(url_for('dashboard'))

    cur.close()
    conn.close()
    return render_template('edit_task.html', task=task)


# ─────────────────────────────────────────
#  DELETE TASK
# ─────────────────────────────────────────
@app.route('/delete/<int:task_id>')
@login_required
def delete_task(task_id):
    conn = get_db()
    cur  = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s AND user_id = %s",
                (task_id, session['user_id']))
    conn.commit()
    cur.close()
    conn.close()
    flash('Task deleted.', 'info')
    return redirect(url_for('dashboard'))


# ─────────────────────────────────────────
#  UPDATE STATUS
# ─────────────────────────────────────────
@app.route('/status/<int:task_id>/<new_status>')
@login_required
def update_status(task_id, new_status):
    allowed = ['Pending', 'In Progress', 'Completed']
    if new_status not in allowed:
        flash('Invalid status.', 'danger')
        return redirect(url_for('dashboard'))

    conn = get_db()
    cur  = conn.cursor()
    cur.execute("UPDATE tasks SET status=%s WHERE id=%s AND user_id=%s",
                (new_status, task_id, session['user_id']))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True)
