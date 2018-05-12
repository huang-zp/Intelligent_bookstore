from flask import Blueprint, render_template

from datetime import datetime, timedelta
from app.models import BxBook, BxBookRating, User
from app.engines import db
from flask_login import current_user

now_time = datetime.now()
begin_time = now_time + timedelta(days=-7)

front_index = Blueprint('front_index', __name__, url_prefix='')
param_location = ('json', )


@front_index.route('/')
def index():

    books = db.session.query(BxBook).limit(15).all()

    return render_template('front_index.html', books1=[books[12], books[7], books[13]], books2=books[3:6])


@front_index.route('/recomm')
def recomm():
    books = db.session.query(BxBook).limit(15).all()
    if current_user.is_authenticated:
        isbn_ids = db.session.query(BxBookRating.book_isbn).order_by(BxBookRating.book_rating.desc()).limit(15).all()
        book_tops = db.session.query(BxBook).filter(BxBook.book_isbn.in_(isbn_ids)).all()
    else:
        isbn_ids = db.session.query(BxBookRating.book_isbn).order_by(BxBookRating.book_rating.desc()).limit(15).all()
        book_tops = db.session.query(BxBook).filter(BxBook.book_isbn.in_(isbn_ids)).all()

    return render_template('front_recomm.html', books1=[books[12], books[7], books[13]], books2=books[3:6],
                           book_tops=[book_tops[2], book_tops[4], book_tops[5], book_tops[6], book_tops[9]])


@front_index.route('/top')
def top():
    _books = db.session.query(BxBook).limit(15).all()
    isbn_ids = db.session.query(BxBookRating.book_isbn).order_by(BxBookRating.book_rating.desc()).limit(30).all()
    books = db.session.query(BxBook).filter(BxBook.book_isbn.in_(isbn_ids)).all()

    return render_template('front_top.html', books1=[_books[12], _books[7], _books[13]], books2=_books[3:6],
                           books=[books[2], books[4], books[5], books[6], books[9], books[10], books[11], books[13], books[14]] )


@front_index.route('/myrating')
def myrating():
    books = db.session.query(BxBook).limit(15).all()


    ratings = db.session.query(BxBookRating).filter(BxBookRating.user_id==6543).limit(10).all()

    print(ratings)
    return render_template('front_myrating.html', books1=[books[12], books[7], books[13]], books2=books[3:6], ratings=ratings)


@front_index.route('/login')
def login():
    books1 = db.session.query(BxBook).order_by(BxBook.id.desc()).limit(3).all()
    books2 = db.session.query(BxBook).order_by(BxBook.id).limit(3).all()

    return render_template('front_login.html', books1=books1, books2=books2)


@front_index.route('/register')
def register():
    books1 = db.session.query(BxBook).order_by(BxBook.id.desc()).limit(3).all()
    books2 = db.session.query(BxBook).order_by(BxBook.id).limit(3).all()

    return render_template('front_register.html', books1=books1, books2=books2)


@front_index.route('/info')
def info():
    books1 = db.session.query(BxBook).order_by(BxBook.id.desc()).limit(3).all()
    books2 = db.session.query(BxBook).order_by(BxBook.id).limit(3).all()

    user = db.session.query(User).filter(User.id == current_user.id).first()
    return render_template('front_info.html', books1=books1, books2=books2, user=user)