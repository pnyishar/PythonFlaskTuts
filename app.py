from flask import Flask, render_template, request, redirect, url_for, flash
import MySQLdb

app = Flask(__name__)
app.secret_key = 'flash message'

mysql = MySQLdb.connect(host='localhost', user='root', password='Peace@1507', database='flaskcrud')


@app.route('/')
def index():  # put application's code here
    cur = mysql.cursor()
    cur.execute("SELECT * FROM student")
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', students=data)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully!!!")
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        cur = mysql.cursor()
        cur.execute("INSERT INTO student (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
        mysql.commit()
        return redirect(url_for('index'))


@app.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == "POST":
        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        cur = mysql.cursor()
        cur.execute("""
        UPDATE student
        SET name = %s, email = %s, phone = %s
        WHERE id = %s
        """, (name, email, phone, id_data))
        flash("Data Updated Successfully!!!")
        mysql.commit()
        return redirect(url_for('index'))


@app.route('/delete/<string:id_data>', methods=['POST', 'GET'])
def delete(id_data):
    flash("Deleted Successfully!!!")
    cur = mysql.cursor()
    cur.execute("DELETE FROM student WHERE id=%s", id_data)
    mysql.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
