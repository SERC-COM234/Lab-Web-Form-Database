from flask import Flask, request, redirect, send_from_directory, url_for
import pyodbc

app = Flask(__name__)

# Database connection
conn_str = (
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'Server=localhost;'
    r'PORT=1433;'
    r'Database=WebForm;'
    r'UID=sa;'
    r'PWD=P@ssw0rd;'
    # r'Trusted_Connection=yes;'
)
conn = pyodbc.connect(conn_str)

# test connection
cursor = conn.cursor()
cursor.execute("SELECT * FROM Submission")
row = cursor.fetchone()
if row:
    print(row)
cursor.close()

# form submission
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        cursor = conn.cursor()
        cursor.execute("INSERT INTO Submission (Name, Email, Message) VALUES (?, ?, ?)", (name, email, message))
        conn.commit()
        cursor.close()

        # return redirect(url_for('success'))
        return 'Submission successful!'

    return redirect(url_for('index'))

# index page - return index.html file
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
