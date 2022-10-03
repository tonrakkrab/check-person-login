# Store this code in 'app.py' file
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import json
import datetime as datetime

 
app = Flask(__name__)
 
app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'migae5o25m2psr4q.cbetxkdyhwsb.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'vhqskbgmu3qpnyqa'
app.config['MYSQL_PASSWORD'] = 'peh1p64ucikdulzs'
app.config['MYSQL_DB'] = 'tevm7fxnw6cl3fyr'
 
mysql = MySQL(app)


@app.route('/')
def hello_world():
    #return 'Hello, world!'
    return render_template("index.html")


@app.route("/index")
def index():
    if 'loggedin' in session:
        return render_template("index.html")
    return redirect(url_for('login'))


@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password, ))
        users = cursor.fetchone()
        if users:
            session['loggedin'] = True
            session['user_id'] = users['user_id']
            session['username'] = users['username']
            msg = 'Logged in successfully !'
            return render_template('main.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)
 
@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('user_id', None)
   session.pop('username', None)
   return redirect(url_for('login'))


@app.route('/user')
#@login_required
def user():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        return render_template("user.html", users = users)        
    return redirect(url_for('login'))

@app.route("/user_view", methods =['GET', 'POST'])
def user_view():
    if 'loggedin' in session:
        viewUserId = request.args.get('userid')   
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE user_id = %s', (viewUserId, ))
        user = cursor.fetchone()   
        return render_template("user_view.html", user = user)
    return redirect(url_for('login'))

@app.route("/user_edit", methods =['GET', 'POST'])
def user_edit():
    msg = ''    
    if 'loggedin' in session:
        editUserId = request.args.get('userid')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE user_id = %s', (editUserId, ))
        editUser = cursor.fetchone()
        # if request.method == 'POST' and 'username' in request.form and 'user_id' in request.form and 'role' in request.form and 'country' in request.form :
        if request.method == 'POST' and 'username' in request.form and 'user_id' in request.form :
            userName = request.form['username']   
            # role = request.form['role']
            # country = request.form['country']            
            userId = request.form['user_id']
            if not re.match(r'[A-Za-z0-9]+', userName):
                msg = 'name must contain only characters and numbers !'
            else:
                cursor.execute('UPDATE users SET username =%s WHERE user_id =%s', (userName, userId) )
                mysql.connection.commit()
                msg = 'User updated !'
                return redirect(url_for('user'))
        elif request.method == 'POST':
            msg = 'Please fill out the form !'        
        return render_template("user_edit.html", msg = msg, editUser = editUser)

    return redirect(url_for('login'))

@app.route("/user_delete")
def user_delete():
    if 'loggedin' in session:
        return render_template("user.html")
    return redirect(url_for('login'))


@app.route('/person')
#@login_required
def person():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute('SELECT * FROM persons')
        sql = 'SELECT persons.*, trip_types.trip_type_name as trip_type_name FROM persons INNER JOIN trip_types ON trip_types.trip_type_id = persons.trip_type_id'
        cursor.execute(sql)        
        persons = cursor.fetchall()
        return render_template("person.html", persons = persons)        
    return redirect(url_for('login'))

@app.route("/person_view", methods =['GET', 'POST'])
def person_view():
    if 'loggedin' in session:
        viewPersonId = request.args.get('personid')   
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #cursor.execute('SELECT * FROM persons WHERE person_id = %s', (viewPersonId, ))
        cursor.execute('SELECT persons.*, trip_types.trip_type_name as trip_type_name FROM persons INNER JOIN trip_types ON trip_types.trip_type_id = persons.trip_type_id WHERE person_id = %s', (viewPersonId, ))
        person = cursor.fetchone()   
        return render_template("person_view.html", person = person)
    return redirect(url_for('login'))


@app.route("/person_edit", methods =['GET', 'POST'])
def person_edit():
    msg = ''    
    if 'loggedin' in session:
        editPersonId = request.args.get('personid')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute("SELECT * FROM trip_types order by trip_type_id asc")
        tripTypesList = cursor.fetchall()

        #cursor.execute('SELECT * FROM persons WHERE person_id = %s', (editPersonId, ))
        cursor.execute('SELECT persons.*, trip_types.trip_type_name as trip_type_name FROM persons INNER JOIN trip_types ON trip_types.trip_type_id = persons.trip_type_id WHERE person_id = %s', (editPersonId, ))
        editPerson = cursor.fetchone()
        # if request.method == 'POST' and 'username' in request.form and 'user_id' in request.form and 'role' in request.form and 'country' in request.form :
        if request.method == 'POST' and 'person_id' in request.form and 'identify' in request.form and 'firstname_th' in request.form and 'telephone_number' in request.form and 'trip_type' in request.form  and 'origin_date' in request.form :

            personId = request.form['person_id']
            #ID_card_photo_path
            identify = request.form['identify']            
            firstname_th = request.form['firstname_th']
            lastname_th = request.form['lastname_th']
            telephone_number = request.form['telephone_number']
            trip_type_id = request.form['trip_type']

            origin_date = request.form['origin_date']
            origin_country_id = request.form['origin_country']
            origin_province_id = request.form['origin_province']
            origin_amphur_id = request.form['origin_amphur']
            origin_tambon_id = request.form['origin_tambon']

            destination_date = request.form['destination_date']
            destination_country_id = request.form['destination_country']
            destination_province_id = request.form['destination_province']
            destination_amphur_id = request.form['destination_amphur']
            destination_tambon_id = request.form['destination_tambon']
            
            # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # cursor.execute('SELECT * FROM persons WHERE person_id !=%s and identify = %s', (personId,identify))
            # person = cursor.fetchone()
            # if person:
            #     #msg = 'User already exists !'
            #     msg = 'ข้อมูลที่ปรับปรุงไปซ้ำกับข้อมูลบุคคลอื่น'
            #     return render_template("person_edit.html", msg = msg, editPerson = editPerson, tripTypesList = tripTypesList)
            # # elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            # #     mesage = 'Invalid email address !'
            # # elif not identify or not firstNameTH or not lastNameTH:
            # #     msg = 'Please fill out the form !'
            # else:
            #     # if not re.match(r'[A-Za-z0-9]+', firstNameTH):
            #     #     msg = 'name must contain only characters and numbers !'
            #     # else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('UPDATE persons SET identify =%s , firstname_th =%s , lastname_th =%s , telephone_number =%s , trip_type_id =%s , origin_country_id =%s , origin_province_id =%s , origin_amphur_id =%s , origin_tambon_id =%s , destination_country_id =%s , destination_province_id =%s , destination_amphur_id =%s , destination_tambon_id =%s  WHERE person_id =%s', (identify, firstname_th, lastname_th, telephone_number, trip_type_id,  origin_country_id, origin_province_id, origin_amphur_id, origin_tambon_id,  destination_country_id, destination_province_id, destination_amphur_id, destination_tambon_id, personId) )

            # origin_date =%s , 
            # destination_date =%s , 
            # datetime.strptime(origin_date, '%m/%d/%Y'),
            # datetime.strptime(destination_date, '%m/%d/%Y'),

            # dt.datetime.strptime(origin_date, '%m/%d/%Y') # string to date
            # dt.datetime.strptime(destination_date, '%m/%d/%Y')
            # now = dt.datetime.now()
            # formatted_date = now.strftime('%Y-%m-%d %H:%M:%S') # date to string

            mysql.connection.commit()
            #msg = 'User updated !'
            msg = 'ปรับปรุงข้อมูลบุคคลสำเร็จ !'
            return redirect(url_for('person'))

        elif request.method == 'POST':
            #msg = 'Please fill out the form !'
            msg = 'กรุณาระบุข้อมูล !'
                    

        cursor.execute("SELECT * FROM countries order by id asc")
        countriesList = cursor.fetchall()

        cursor.execute("SELECT * FROM provinces order by id asc")
        provincesList = cursor.fetchall()

        cursor.execute("SELECT * FROM amphures order by id asc")
        amphuresList = cursor.fetchall()

        cursor.execute("SELECT * FROM districts order by id asc")
        districtsList = cursor.fetchall() 

        return render_template("person_edit.html", msg = msg, editPerson = editPerson, tripTypesList = tripTypesList, countriesList = countriesList, provincesList = provincesList, amphuresList = amphuresList, districtsList = districtsList)
        
    return redirect(url_for('login'))


@app.route('/person_add', methods =['GET', 'POST'])
def person_add():
    msg = ''

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("SELECT * FROM trip_types order by trip_type_id asc")
    tripTypesList = cursor.fetchall()

    cursor.execute("SELECT * FROM countries order by id asc")
    countriesList = cursor.fetchall()

    cursor.execute("SELECT * FROM provinces order by id asc")
    provincesList = cursor.fetchall()

    cursor.execute("SELECT * FROM amphures order by id asc")
    amphuresList = cursor.fetchall()

    cursor.execute("SELECT * FROM districts order by id asc")
    districtsList = cursor.fetchall() 

    if request.method == 'POST' and 'identify' in request.form and 'firstname_th' in request.form and 'telephone_number' in request.form and 'trip_type' in request.form  and 'origin_date' in request.form :

        identify = request.form['identify']
        ID_card_photo_path = request.form['ID_card_photo_path']
        firstname_th = request.form['firstname_th']
        lastname_th = request.form['lastname_th']
        telephone_number = request.form['telephone_number']

        trip_type_id = request.form['trip_type']

        origin_date = request.form['origin_date']
        origin_country_id = request.form['origin_country']
        origin_province_id = request.form['origin_province']
        origin_amphur_id = request.form['origin_amphur']
        origin_tambon_id = request.form['origin_tambon']

        destination_date = request.form['destination_date']
        destination_country_id = request.form['destination_country']
        destination_province_id = request.form['destination_province']
        destination_amphur_id = request.form['destination_amphur']
        destination_tambon_id = request.form['destination_tambon']

        #cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute('SELECT * FROM persons WHERE email = % s', (email, ))
        # account = cursor.fetchone()
        # if account:
        #     mesage = 'User already exists !'
        # elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        #     mesage = 'Invalid email address !'
        # elif not firstname or not lastname or not email:
        #     mesage = 'Please fill out the form !'
        # else:

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # sql = 'INSERT INTO persons (identify, ID_card_photo_path, firstname_th, lastname_th, telephone_number, trip_type_id) VALUES (NULL, %s, %s, %s, %s, %s, %s)'
        # value = (identify, ID_card_photo_path, firstname_th, lastname_th, telephone_number, trip_type_id)        
        # cursor.execute(sql, value)

        # cursor.execute('SELECT * FROM persons WHERE identify = %s', (identify))
        # person = cursor.fetchone()
        # if person:
        #     #msg = 'User already exists !'
        #     msg = 'ข้อมูลที่ต้องการเพิ่มไปซ้ำกับข้อมูลบุคคลอื่น'
        #     return render_template("person_add.html", msg = msg, tripTypesList = tripTypesList, countriesList = countriesList, provincesList = provincesList, amphuresList = amphuresList, districtsList = districtsList)
        # # elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        # #     mesage = 'Invalid email address !'
        # # elif not identify or not firstNameTH or not lastNameTH:
        # #     msg = 'Please fill out the form !'
        # else:
        # if not re.match(r'[A-Za-z0-9]+', firstNameTH):
        #     msg = 'name must contain only characters and numbers !'
        # else:
        cursor.execute('INSERT INTO persons (identify, ID_card_photo_path, firstname_th, lastname_th, telephone_number, trip_type_id, origin_country_id, origin_province_id, origin_amphur_id, origin_tambon_id, destination_country_id, destination_province_id, destination_amphur_id, destination_tambon_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (identify, ID_card_photo_path, firstname_th, lastname_th, telephone_number, trip_type_id, origin_country_id, origin_province_id, origin_amphur_id, origin_tambon_id, destination_country_id, destination_province_id, destination_amphur_id, destination_tambon_id)) 
        
        # origin_date, 
        # destination_date, 
        # origin_date, 
        # destination_date, 
        # , %s, %s

        mysql.connection.commit()
        # msg = 'New person created!'
        msg = 'เพิ่มข้อมูลบุคคลสำเร็จ !'

    elif request.method == 'POST':
        #msg = 'Please fill out the form !'
        msg = 'กรุณาระบุข้อมูล !'
    else:        
        return render_template('person_add.html', msg = msg, tripTypesList = tripTypesList, countriesList = countriesList, provincesList = provincesList, amphuresList = amphuresList, districtsList = districtsList)

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT persons.*, trip_types.trip_type_name as trip_type_name FROM persons INNER JOIN trip_types ON trip_types.trip_type_id = persons.trip_type_id')
    persons = cursor.fetchall()

    return render_template('person.html', msg = msg, persons = persons)


@app.route("/person_delete")
def person_delete():
    if 'loggedin' in session:
        return render_template("person.html")
    return redirect(url_for('login'))


# (C)
@app.route("/person_search", methods=["GET", "POST"])
def person_search():
  # (C1) SEARCH FOR PERSONS
  if request.method == "POST":
    data = dict(request.form)
    persons = getperson(data["search1"],data["search2"])
  else:
    persons = []
 
  # (C2) RENDER HTML PAGE
  return render_template("person.html", persons=persons)

# (B) HELPER FUNCTION - SEARCH PERSONS
def getperson(search1,search2):
  cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
  cursor.execute('SELECT persons.*, trip_types.trip_type_name as trip_type_name FROM persons INNER JOIN trip_types ON trip_types.trip_type_id = persons.trip_type_id WHERE firstname_th LIKE %s AND lastname_th LIKE %s', ('%'+search1+'%', '%'+search2+'%'))
  results = cursor.fetchall()  
  return results


# def get_dropdown_values():

#     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     cursor.execute("SELECT * FROM countries order by id asc")
#     countriesList = cursor.fetchall()

#     cursor.execute("SELECT * FROM provinces order by id asc")
#     provincesList = cursor.fetchall()

#     #carbrands = Carbrands.query.all()
#     carbrands = countriesList
#     # Create an empty dictionary
#     myDict = {}
#     for p in carbrands:
    
#         # key = p.name_th
#         # country_id = p.id

#         # Select all car models that belong to a car brand
#         #q = Carmodels.query.filter_by(brand_id=brand_id).all()
#         q = provincesList.query.filter_by(country_id=p.id).all()
    
#         # build the structure (lst_c) that includes the names of the car models that belong to the car brand
#         lst_c = []
#         for c in q:
#             lst_c.append( c.name_th )
#         carbrands[p.name_th] = lst_c
    
#     class_entry_relations = carbrands
                        
#     return class_entry_relations


# @app.route('/_update_dropdown')
# def update_dropdown():

#     # the value of the first dropdown (selected by the user)
#     selected_class = request.args.get('selected_class', type=str)

#     # get values for the second dropdown
#     updated_values = get_dropdown_values()[selected_class]

#     # create the value sin the dropdown as a html string
#     html_string_selected = ''
#     for entry in updated_values:
#         html_string_selected += '<option value="{}">{}</option>'.format(entry, entry)

#     return jsonify(html_string_selected=html_string_selected)


# @app.route('/_process_data')
# def process_data():
#     selected_class = request.args.get('selected_class', type=str)
#     selected_entry = request.args.get('selected_entry', type=str)

#     # process the two selected values here and return the response; here we just create a dummy string

#     return jsonify(random_text="You selected the car brand: {} and the model: {}.".format(selected_class, selected_entry))


# @app.route('/index_brand')
# def index_brand():

#     """
#     initialize drop down menus
#     """

#     class_entry_relations = get_dropdown_values()

#     default_classes = sorted(class_entry_relations.keys())
#     default_values = class_entry_relations[default_classes[0]]

#     return render_template('index.html',
#                        all_classes=default_classes,
#                        all_entries=default_values)

 
# def get_dropdown_values():

#     """
#     dummy function, replace with e.g. database call. If data not change, this function is not needed but dictionary
# could be defined globally
#     """

#     # Create a dictionary (myDict) where the key is 
#     # the name of the brand, and the list includes the names of the car models
#     # 
#     # Read from the database the list of cars and the list of models. 
#     # With this information, build a dictionary that includes the list of models by brand. 
#     # This dictionary is used to feed the drop down boxes of car brands and car models that belong to a car brand.
#     # 
#     # Example:
#     #
#     # {'Toyota': ['Tercel', 'Prius'], 
#     #  'Honda': ['Accord', 'Brio']}

#     carbrands = Carbrands.query.all()
#     # Create an empty dictionary
#     myDict = {}
#     for p in carbrands:
    
#         key = p.brand_name
#         brand_id = p.brand_id

#         # Select all car models that belong to a car brand
#         q = Carmodels.query.filter_by(brand_id=brand_id).all()
    
#         # build the structure (lst_c) that includes the names of the car models that belong to the car brand
#         lst_c = []
#         for c in q:
#             lst_c.append( c.car_model )
#         myDict[key] = lst_c
    
    
#     class_entry_relations = myDict
                        
#     return class_entry_relations


# @app.route('/_update_dropdown')
# def update_dropdown():

#     # the value of the first dropdown (selected by the user)
#     selected_class = request.args.get('selected_class', type=str)

#     # get values for the second dropdown
#     updated_values = get_dropdown_values()[selected_class]

#     # create the value sin the dropdown as a html string
#     html_string_selected = ''
#     for entry in updated_values:
#         html_string_selected += '<option value="{}">{}</option>'.format(entry, entry)

#     return jsonify(html_string_selected=html_string_selected)


# @app.route('/_process_data')
# def process_data():
#     selected_class = request.args.get('selected_class', type=str)
#     selected_entry = request.args.get('selected_entry', type=str)

#     # process the two selected values here and return the response; here we just create a dummy string

#     return jsonify(random_text="You selected the car brand: {} and the model: {}.".format(selected_class, selected_entry))




# @app.route('/')
# def index():

#     """
#     initialize drop down menus
#     """

#     class_entry_relations = get_dropdown_values()

#     default_classes = sorted(class_entry_relations.keys())
#     default_values = class_entry_relations[default_classes[0]]

#     return render_template('index.html',
#                        all_classes=default_classes,
#                        all_entries=default_values)


if __name__ == "__main__":
    app.run(host ="localhost", port = int("5000"))