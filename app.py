from flask import Flask, render_template, request, redirect

import sqlite3

app = Flask(__name__)

db_path = 'checklist.db'

def create_table():
  connection = sqlite3.connect(db_path)
  cursor = connection.cursor()
  cursor.execute('''CREATE TABLE IF NOT EXISTS checklist (id INTEGER PRIMARY KEY AUTOINCREMENT, item TEXT)''')
  connection.commit()
  connection.close()

def db_add_item(item):
  connection = sqlite3.connect(db_path)
  cursor = connection.cursor()
  cursor.execute("INSERT INTO checklist (item) VALUES (?)", (item,))
  connection.commit()
  connection.close()

def db_get_items():
  connection = sqlite3.connect(db_path)
  cursor = connection.cursor()
  cursor.execute("SELECT * FROM checklist")
  items = cursor.fetchall()
  connection.close()
  return items

def db_update_item(item_id, new_item):
  connection = sqlite3.connect(db_path)
  cursor = connection.cursor()
  cursor.execute("UPDATE checklist SET item = ? WHERE id = ?", (new_item, item_id))
  connection.commit()
  connection.close()

def db_delete_item(item_id):
  connection = sqlite3.connect(db_path)
  cursor = connection.cursor()
  cursor.execute("DELETE FROM checklist WHERE id = ?", (item_id,))
  connection.commit()
  connection.close()

# Create functionality
@app.route('/add', methods=['POST'])
def add_item():
  item = request.form['item']
  db_add_item(item)
  return redirect('/') # Go back to old page

# Read functionality
@app.route('/') # GET method implied, as default option
def checklist():
  create_table()
  items = db_get_items()
  return render_template('checklist.html', items=items)

# Update functionality
@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):

  if request.method == 'POST':
    new_item = request.form['item']
    db_update_item(item_id, new_item)
    return redirect('/')
  else:
    items = db_get_items()
    item = next((x[1] for x in items if x[0] == item_id), None)
  
  return render_template('edit.html', item=item, item_id=item_id)

# Delete functionality
@app.route('/delete/<int:item_id>')
def delete_item(item_id):
  db_delete_item(item_id)
  return redirect('/')
