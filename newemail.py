from flask import Flask,request,redirect,render_template,flash,session

from datetime import datetime
# from datetime import datetime
import re

from mysqlconnection import MySQLConnector
app = Flask(__name__)

app.secret_key = "vsdkjnfskj/nsknjscdckj"

mysql = MySQLConnector(app, 'email')

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9+-._]+@[a-zA-Z0-9+-._]+\.[a-zA-Z]+$')

@app.route('/')
def user():

	return render_template('again.html',email=mysql.query_db("SELECT * FROM email"))

@app.route('/process', methods=['POST'])
def create():

	valid=True

	if request.form["email"]=='':
		flash("Email is required!")
		valid = False

		return redirect('/')
	elif not EMAIL_REGEX.match(request.form["email"]):
		flash("Invalid Email")
		valid = False

		return redirect('/')
	else:
		flash("The email address you entered "+request.form['email']+" is a VALID email address! Thank you!")

		query="INSERT INTO email (email, created_at) VALUES (:email, NOW())"


	data={'email':request.form['email']}

	mysql.query_db(query,data)	

	return redirect('/success')


#need to get parameters email and new_email
@app.route('/success')
def display():
	return render_template('success.html', email=mysql.query_db("SELECT * FROM email"))

@app.route('/remove/<email_id>', methods=['POST'])
def delete(email_id):
    query = "DELETE FROM email WHERE id=:id"
    data = {'id': email_id}
    mysql.query_db(query, data)
    return redirect('/success')


app.run(debug=True)