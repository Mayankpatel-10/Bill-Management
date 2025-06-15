from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secretkey"

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    bills = conn.execute('SELECT * FROM bills WHERE user_id = ? ORDER BY date DESC', (session['user_id'],)).fetchall()
    conn.close()

    return render_template('dashboard.html', username=session['username'], bills=bills)

@app.route('/add-bill', methods=['GET', 'POST'])
def add_bill():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        date = request.form['date']
        category = request.form['category']
        amount = request.form['amount']
        description = request.form['description']

        conn = get_db_connection()
        conn.execute('INSERT INTO bills (date, category, amount, description, user_id) VALUES (?, ?, ?, ?, ?)',
                     (date, category, amount, description, session['user_id']))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))

    return render_template('add_bill.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
