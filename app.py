import pyrebase
from flask import *
from firebase import firebase

config={

 	"apiKey": "AIzaSyDC0uS-8U0HSeESHgggAlZOoU-3Y5RRp9U",
    "authDomain": "flask-forms.firebaseapp.com",
    "databaseURL": "https://flask-forms.firebaseio.com",
    "projectId": "flask-forms",
    "storageBucket": "flask-forms.appspot.com",
    "messagingSenderId": "93606330816",
    "appId": "1:93606330816:web:fea026a763f54c55938825",
    "measurementId": "G-0ZWDGM4ZC4"
	
}

FBConn = firebase.FirebaseApplication('https://flask-forms.firebaseio.com/')

firebase=pyrebase.initialize_app(config)
db=firebase.database()



app=Flask(__name__)
app.secret_key = 'hello'
@app.route('/')
def basic():
	return render_template('base.html')


@app.route('/signup', methods=['GET','POST'])
def signup_page():
	if request.method=='POST':
		if request.form['submit'] == 'add':
			fname=request.form['fname']
			lname=request.form['lname']
			phone=request.form['phone']
			address=request.form['address']
			email=request.form['email']
			username=request.form['username']
			password=request.form['password']
			conpassword=request.form['conpassword']
			if password == conpassword:					
				data_to_upload ={
					'First Name': fname,
					'Last Name': lname,
					'Phone Number': phone,
					'Address':address,
					'Email': email,
					'Username':username,
					'Password':password
				}
				result=FBConn.post('/userinfo/', data_to_upload)
				return render_template('profile.html',first_name=fname, last_name=lname,phone=phone
				,address=address,email=email,user_name=username)
			else:
				return ('password and confirm password do not match')
	return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
	result = FBConn.get('/userinfo/',None)
	if request.method =='POST':
		if request.form['submit'] == 'add':
			username1 = request.form['username']
			session["user"]= username1
			password1 = request.form['password']

			for i in result:
				a=result[i]['Username']
				b=result[i]['Password']
				if username1 == a and password1 == b:
					return redirect(url_for('profile'))
				else:
					return 'Login not successful, please try again!'
	return render_template('login.html')

@app.route('/profile',methods=['GET','POST'])
def profile():
	result  = FBConn.get('/userinfo/', None)
	first_name = ""
	last_name =""
	phone=""
	address=""
	email=""
	user_name=""
	if "user" in session:
		username = session["user"]
		for i in result:
			a = result[i]['Username']
			if a == username:
				first_name = result[i]['First Name']
				last_name=result[i]['Last Name']
				phone=result[i]['Phone Number']
				address=result[i]['Address']
				email=result[i]['Email']
				user_name=result[i]['Username']
		return render_template('profile.html',first_name=first_name,last_name=last_name,phone=phone
			,address=address,email=email,user_name=user_name)
	return render_template('profile.html')

if __name__ == '__main__':
	app.run(debug=True)

