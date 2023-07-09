from flask import Flask, render_template, request, redirect

app = Flask(__name__)

items = [] # No DB for now, simply using list

@app.route('/add', method=['POST'])
def add_item():
  item = request.form['item']
  items.append(item)
  return redirect('/') # Go back to old page