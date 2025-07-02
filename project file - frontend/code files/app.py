from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for session management

# In-memory user storage (email: password)
users = {}

@app.route('/')
def index():
    return render_template('index.html')  # Login page

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    if email in users and users[email] == password:
        session['email'] = email
        return redirect(url_for('movies'))
    else:
        return "Invalid email or password. <a href='/'>Try again</a>"

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email in users:
            return "Email already exists. <a href='/'>Login here</a>"
        users[email] = password
        return redirect(url_for('index'))  # Go to login after signup
    return render_template('signup.html')

@app.route('/movies', methods=['GET', 'POST'])
def movies():
    if 'email' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        movie = request.form['movie']
        time = request.form['time']
        tickets = request.form['tickets']
        rows = [chr(i) for i in range(65, 91)]  # A to Z
        return render_template('seats.html', movie=movie, time=time, tickets=tickets, rows=rows)
    return render_template('movies.html')

@app.route('/payment', methods=['POST'])
def payment():
    movie = request.form['movie']
    time = request.form['time']
    tickets = request.form['tickets']
    seats = request.form.getlist('seats')
    return render_template('payment.html', movie=movie, time=time, tickets=tickets, seats=seats)

@app.route('/confirm', methods=['POST'])
def confirm():
    movie = request.form['movie']
    time = request.form['time']
    tickets = request.form['tickets']
    seats = request.form.getlist('seats')
    name = request.form['name']
    return render_template('success.html', movie=movie, time=time, tickets=tickets, seats=seats, name=name)

if __name__ == '__main__':
    app.run(debug=True)
