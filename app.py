from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    date_baked = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50))
    added_by = db.Column(db.String(50))

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add_item():
    product = request.form.get('product')
    category = request.form.get('category')
    quantity = request.form.get('quantity', type=int)
    price = request.form.get('price', type=float)
    date_str = request.form.get('date')
    status = request.form.get('status')
    added_by = "User"

    if product and category and quantity is not None and price is not None and date_str and status:
        try:
            date_baked = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            new_item = Item(
                product=product,
                category=category,
                quantity=quantity,
                price=price,
                date_baked=date_baked,
                status=status,
                added_by=added_by
            )
            db.session.add(new_item)
            db.session.commit()
        except ValueError:
            print("Invalid date format submitted.")

    return redirect('/')

@app.route('/update/<int:item_id>', methods=['GET', 'POST'])
def update_item(item_id):
    item = Item.query.get_or_404(item_id)
    if request.method == 'POST':
        item.product = request.form.get('product')
        item.category = request.form.get('category')
        item.quantity = request.form.get('quantity', type=int)
        item.price = request.form.get('price', type=float)
        date_str = request.form.get('date')
        item.status = request.form.get('status')
        try:
            item.date_baked = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            db.session.commit()
            return redirect('/')
        except ValueError:
            print("Invalid date format submitted for update.")
            
    return render_template('update_item.html', item=item)

@app.route('/delete/<int:item_id>')
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
