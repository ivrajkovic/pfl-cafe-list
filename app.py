from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, FloatField, SubmitField
from wtforms.validators import DataRequired, URL, Length, NumberRange


app = Flask(__name__)
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '2!j@56czUkTQ53'
db = SQLAlchemy(app)


# ------------------ SQL Tables
# Cafe TABLE Configuration
class Cafe(db.Model):
    __tablename__ = 'cafe'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=True)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


# ------------------ Forms
# Create Cafe Form
class AddCafeForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired(), Length(max=200)], render_kw={'class': 'form-control'})
    map_url = StringField(label='Maps link', validators=[DataRequired(), Length(max=450), URL()], render_kw={'class': 'form-control'})
    img_url = StringField(label='Image link', validators=[DataRequired(), Length(max=450), URL()], render_kw={'class': 'form-control'})
    location = StringField(label='Location', validators=[DataRequired(), Length(max=200)], render_kw={'class': 'form-control'})
    seats = StringField(label='Seats (range)', validators=[DataRequired(), Length(max=200)], render_kw={'class': 'form-control'})
    has_toilet = BooleanField(label='Has Toilet', render_kw={'class': 'form-check-input'})
    has_wifi = BooleanField(label='Has Wifi', render_kw={'class': 'form-check-input'})
    has_sockets = BooleanField(label='Has Power sockets', render_kw={'class': 'form-check-input'})
    can_take_calls = BooleanField(label='Can take calls', render_kw={'class': 'form-check-input'})
    coffee_price = FloatField(label='Coffee price', validators=[DataRequired(), NumberRange(min=1, max=100)], render_kw={'class': 'form-control'})
    submit = SubmitField(label='Add new', render_kw={'class': 'btn btn-success'})


# ------------------ Routes
# Index page
@app.route('/')
def home():
    all_cafes = db.session.query(Cafe).all()
    return render_template('index.html', cafes=all_cafes)


# Add new cafe
@app.route('/add', methods=['GET', 'POST'])
def add():
    form = AddCafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            seats=form.seats.data,
            has_toilet=form.has_toilet.data,
            has_wifi=form.has_wifi.data,
            has_sockets=form.has_sockets.data,
            can_take_calls=form.can_take_calls.data,
            coffee_price="£" + str(form.coffee_price.data)
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html', form=form)


# Delete cafe
@app.route("/delete/<int:cafe_id>")
def delete(cafe_id):
    cafe = Cafe.query.get(cafe_id)
    if cafe:
        db.session.delete(cafe)
        db.session.commit()
    return redirect(url_for('home'))


# Flask run
if __name__ == '__main__':
    app.run(debug=True)
