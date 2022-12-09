import os
from Projects.mysql_db import DBQueryEngine
from flask import Flask, flash, redirect, render_template, request, session, abort
import pymysql


class DBConnect:

    def connect(self):
        try:
            return pymysql.connect("localhost", "root", "admin", "hostel_management")
        except Exception as e:
            print("Unable to connect to database " + str(e))
            return False


app = Flask(__name__)


@app.route('/')
def dashboard():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return 'Welcome to your dashborard!'


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username is '' and password is '':
        return dashboard()
    validate = DBQueryEngine.check_password(username, password)
    if len(validate) is 0:
        session['logged_in'] = True
        return home()
    else:
        return render_template('error.html')




@app.route('/questions', methods=['GET'])
def home():
    print("Getting list of questions")
    if session.get('logged_in'):
        return render_template("home.html")
    else:
        return render_template('login.html')

@app.route('/form', methods=['GET'])
def show_form():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register():
    print("A new registration process ...")
    response = DBQueryEngine.create_user(request.form['id'], request.form['student_name'], request.form['father_name'], request.form['dob'], request.form['phno'], request.form['email'], request.form['Gender'], request.form['Roomno'], request.form['Address'], request.form['Amount'])
    return render_template('home.html')

@app.route('/delete', methods=['POST'])
def delete():
    print("Deletion")
    response = DBQueryEngine.del_user(request.form['id'])
    return render_template('home.html')


@app.route('/update', methods=['POST'])
def update():
    print("Updation")
    response = DBQueryEngine.update_user(request.form['id'])
    return render_template('home.html')



@app.route('/del', methods=['GET'])
def del_form():
    return render_template('delete.html')

@app.route('/up', methods=['GET'])
def up_form():
    return render_template('update.html')

@app.route('/log', methods=['GET'])
def log_form():
    return render_template('login.html')

@app.route('/display', methods=['GET'])
def dis_form():
    return render_template('display.html')

@app.route('/disp', methods=['GET'])
def disp():
    conn = DBConnect().connect()
    try:
        cursor = conn.cursor()
        sql="SELECT * FROM register"
        print(sql)
        cursor.execute(sql)
        data = cursor.fetchall()
        return render_template('display.html',data=data)
    except Exception as e:
        print("Caught exception while displaying users " + str(e))
        return "Unsuccessful".format(id)
    finally:
        conn.close()



@app.route("/logout")
def logout():
    session['logged_in'] = False
    return dashboard()


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='localhost', port=4000)