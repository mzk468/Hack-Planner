from flask import Flask, render_template, request, redirect

app = Flask(__name__)

items = [] # No DB for now, simply using list

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

app.run(port=8000)
