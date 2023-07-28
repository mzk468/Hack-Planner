from flask import Flask, render_template, request, redirect

import sqlite3

app = Flask(__name__)

items = [] # No DB for now, simply using list

db_path = 'checklist.db'

def create_table():
  connection = sqlite3.connect(db_path)
  cursor = connection.cursor()
  cursor.execute('''CREATE TABLE IF NOT EXISTS checklist (id INTEGER PRIMARY KEY AUTOINCREMENT, item TEXT)''')
  connection.commit()
  connection.close()

def add_item(item):
  connection = sqlite3.connect(db_path)
  cursor = connection.cursor()
  cursor.execute("INSERT INTO checklist (item) VALUES (?)", (item,))
  connection.commit()
  connection.close()

def get_items():
  connection = sqlite3.connect(db_path)
  cursor = connection.cursor()
  cursor.execute("SELECT * FROM checklist")
  items = cursor.fetchall()
  connection.close()
  return items

def update_item(item_id, new_item):
  connection = sqlite3.connect(db_path)
  cursor = connection.cursor()
  cursor.execute("UPDATE checklist SET item = ? WHERE id = ?", (new_item, item_id))
  connection.commit()
  connection.close()

def delete_item(item_id):
  connection = sqlite3.connect(db_path)
  cursor = connection.cursor()
  cursor.execute("DELETE FROM checklist WHERE id = ?", (item_id,))
  connection.commit()
  connection.close()

# Create functionality
@app.route('/add', methods=['POST'])
def add_item():
  item = request.form['item']
  items.append(item)
  return redirect('/') # Go back to old page

# Read functionality
@app.route('/') # GET method implied, as default option
def checklist():
  return render_template('checklist.html', items=items)

# Update functionality
@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
  item = items[item_id - 1]

  if request.method == 'POST':
    new_item = request.form['item']
    items[item_id - 1] = new_item
    return redirect('/')
  
  return render_template('edit.html', item=item, item_id=item_id)

# Delete functionality
@app.route('/delete/<int:item_id>')
def delete_item(item_id):
  del items[item_id - 1]
  return redirect('/')
