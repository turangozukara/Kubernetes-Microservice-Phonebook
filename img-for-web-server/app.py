from flask import Flask, request, render_template
from flaskext.mysql import MySQL
import os

app = Flask(__name__)

app.config['MYSQL_DATABASE_HOST'] = os.getenv('MYSQL_DATABASE_HOST')
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DATABASE_DB'] = os.getenv('MYSQL_DATABASE')
app.config['MYSQL_DATABASE_USER'] = os.getenv('MYSQL_USER')
project_db = os.getenv('MYSQL_DATABASE')
#app.config['MYSQL_DATABASE_PORT'] = 3306
mysql = MySQL()
mysql.init_app(app) 
connection = mysql.connect()
connection.autocommit(True)
cursor = connection.cursor()

def init_phonebook_db():
    phonebook_table = """
    CREATE TABLE IF NOT EXISTS """+ project_db +""".phonebook(
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    number VARCHAR(100) NOT NULL,
    PRIMARY KEY (id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """
    cursor.execute(phonebook_table)

def insert_person(name, number):
    query = f"""
    SELECT * FROM phonebook WHERE name like '{name.strip().lower()}';
    """
    cursor.execute(query)
    row = cursor.fetchone()
    if row is not None:
        return f'Person with name {row[1].title()} already exits.'

    insert = f"""
    INSERT INTO phonebook (name, number)
    VALUES ('{name.strip().lower()}', '{number}');
    """
    cursor.execute(insert)
    result = cursor.fetchall()
    return f'Person {name.strip().title()} added to Phonebook successfully'

def update_person(name, number):
    query = f"""
    SELECT * FROM phonebook WHERE name like '{name.strip().lower()}';
    """
    cursor.execute(query)
    row = cursor.fetchone()
    if row is None:
        return f'Person with name {name.strip().title()} does not exist.'
        
    update = f"""
    UPDATE phonebook
    SET name='{row[1]}', number = '{number}'
    WHERE id= {row[0]};
    """
    cursor.execute(update)

    return f'Phone record of {name.strip().title()} is updated successfully'

def delete_person(name):
    query = f"""
    SELECT * FROM phonebook WHERE name like '{name.strip().lower()}';
    """
    cursor.execute(query)
    row = cursor.fetchone()
    if row is None:
        return f'Person with name {name.strip().title()} does not exist, no need to delete.'

    delete = f"""
    DELETE FROM phonebook
    WHERE id= {row[0]};
    """
    cursor.execute(delete)
    return f'Phone record of {name.strip().title()} is deleted from the phonebook successfully'

@app.route('/add', methods=['GET', 'POST'])
def add_record():
    if request.method == 'POST':
        name = request.form['username']
        if name is None or name.strip() == "":
            return render_template('add-update.html', not_valid=True, message='Invalid input: Name can not be empty', show_result=False, action_name='save', developer_name='Turan')
        elif name.isdecimal():
            return render_template('add-update.html', not_valid=True, message='Invalid input: Name of person should be text', show_result=False, action_name='save', developer_name='Turan')

        phone_number = request.form['phonenumber']
        if phone_number is None or phone_number.strip() == "":
            return render_template('add-update.html', not_valid=True, message='Invalid input: Phone number can not be empty', show_result=False, action_name='save', developer_name='Turan')
        elif not phone_number.isdecimal():
            return render_template('add-update.html', not_valid=True, message='Invalid input: Phone number should be in numeric format', show_result=False, action_name='save', developer_name='Turan')

        result = insert_person(name, phone_number)
        return render_template('add-update.html', show_result=True, result=result, not_valid=False, action_name='save', developer_name='Turan')
    else:
        return render_template('add-update.html', show_result=False, not_valid=False, action_name='save', developer_name='Turan')

@app.route('/update', methods=['GET', 'POST'])
def update_record():
    if request.method == 'POST':
        name = request.form['username']
        if name is None or name.strip() == "":
            return render_template('add-update.html', not_valid=True, message='Invalid input: Name can not be empty', show_result=False, action_name='update', developer_name='Turan')
        phone_number = request.form['phonenumber']
        if phone_number is None or phone_number.strip() == "":
            return render_template('add-update.html', not_valid=True, message='Invalid input: Phone number can not be empty', show_result=False, action_name='update', developer_name='Turan')
        elif not phone_number.isdecimal():
            return render_template('add-update.html', not_valid=True, message='Invalid input: Phone number should be in numeric format', show_result=False, action_name='update', developer_name='Turan')

        result = update_person(name, phone_number)
        return render_template('add-update.html', show_result=True, result=result, not_valid=False, action_name='update', developer_name='Turan')
    else:
        return render_template('add-update.html', show_result=False, not_valid=False, action_name='update', developer_name='Turan')


# using template files named `delete.html` given under `templates` folder
# and assign to the static route of ('delete')
@app.route('/delete', methods=['GET', 'POST'])
def delete_record():
    if request.method == 'POST':
        name = request.form['username']
        if name is None or name.strip() == "":
            return render_template('delete.html', not_valid=True, message='Invalid input: Name can not be empty', show_result=False, developer_name='Turan')
        result = delete_person(name)
        return render_template('delete.html', show_result=True, result=result, not_valid=False, developer_name='Turan')
    else:
        return render_template('delete.html', show_result=False, not_valid=False, developer_name='Turan')

@app.route('/', methods=['GET', 'POST'])
def find_records():
    return render_template('index.html', show_result=False, developer_name='Turan')


if __name__== '__main__':
    init_phonebook_db()
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=80) 
