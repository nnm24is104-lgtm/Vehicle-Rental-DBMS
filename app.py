from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cars.db'
db = SQLAlchemy(app)

# The Database Table
class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(50))
    status = db.Column(db.String(20), default='Available')
    renter = db.Column(db.String(50), default='-')

@app.route('/')
def index():
    data = Car.query.all()
    return render_template('index.html', cars=data)

@app.route('/book/<int:id>', methods=['POST'])
def book(id):
    car_record = Car.query.get(id)
    car_record.renter = request.form['user_name']
    car_record.status = 'Rented'
    db.session.commit()
    return redirect('/')

@app.route('/reset')
def reset():
    Car.query.update({Car.status: 'Available', Car.renter: '-'})
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not Car.query.first():
            db.session.add(Car(model="Toyota"))
            db.session.add(Car(model="Swift"))
            db.session.commit()
    app.run(debug=True)
