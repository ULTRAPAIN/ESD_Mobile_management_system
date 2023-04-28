from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:dasu@localhost/mobiledb'
db = SQLAlchemy(app)

class Mobile(db.Model):
    id = db.Column(db.Integer, primary_key=True,unique=False)
    customer_name = db.Column(db.String(50), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    purchase_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Mobile {self.brand} {self.model}>'

@app.route('/')
def index():
    mobiles = Mobile.query.all()
    return render_template('index.html', mobiles=mobiles)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        brand = request.form['brand']
        model = request.form['model']
        price = request.form['price']
        customer_name = request.form['customer_name']
        purchase_date = datetime.now()
        mobile = Mobile(brand=brand, model=model, price=price, customer_name=customer_name, purchase_date=purchase_date)
        db.session.add(mobile)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    mobile = Mobile.query.get(id)
    if request.method == 'POST':
        mobile.brand = request.form['brand']
        mobile.model = request.form['model']
        mobile.price = request.form['price']
        mobile.customer_name = request.form['customer_name']
        mobile.purchase_date = datetime.now()
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', mobile=mobile)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    mobile = Mobile.query.get(id)
    db.session.delete(mobile)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
