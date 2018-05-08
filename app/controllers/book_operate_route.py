import paramiko
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models import BxBook
from app.engines import db

book_operate = Blueprint('book_operate', __name__, url_prefix='')
param_location = ('json', )


@book_operate.route('/book/list')
@login_required
def book_list():

    books = db.session.query(BxBook).all()
    return render_template('book_list.html', books=books)


@book_operate.route('/book/delete/<int:book_id>')
def book_delete(book_id):
    book = db.session.query(BxBook).filter(BxBook.id == book_id).first()
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('book_operate.book_list'))


@book_operate.route('/book/add', methods=['POST', 'GET'])
def book_add():
    if request.method == 'POST':

        book_isbn = request.form['book_isbn']

        book_title = request.form['book_title']
        book_author = request.form['book_author']
        book_year_of_publication = request.form['book_year_of_publication']
        book_publisher = request.form['book_publisher']

        book_image_url_l = request.form['book_image_url_l']

        if book_isbn == '' or book_title == '' or book_image_url_l == '':
            flash(" 检查某些字段是否为空")
            return redirect(url_for('book_operate.book_add'))

        book = BxBook()
        book.book_isbn = book_isbn
        book.book_title = book_title
        book.book_author = book_author
        book.book_year_of_publication = book_year_of_publication
        book.book_publisher = book_publisher

        book.book_image_url_l = book_image_url_l
        db.session.add(book)
        db.session.commit()

        return redirect(url_for('book_operate.book_list'))

    return render_template('book_add.html')


@book_operate.route('/book/change/<int:book_id>', methods=['POST', 'GET'])
def book_change(book_id):
    book = db.session.query(BxBook).filter(BxBook.id == book_id).first()
    if request.method == 'POST':

        book_isbn = request.form['book_isbn']

        book_title = request.form['book_title']
        book_author = request.form['book_author']
        book_year_of_publication = request.form['book_year_of_publication']
        book_publisher = request.form['book_publisher']

        book_image_url_l = request.form['book_image_url_l']

        if book_isbn == '' or book_title == '' or book_image_url_l == '':
            flash(" 检查某些字段是否为空")
            return redirect(url_for('book_operate.book_change', book_id=book.id))

        book.book_isbn = book_isbn
        book.book_title = book_title
        book.book_author = book_author
        book.book_year_of_publication = book_year_of_publication
        book.book_publisher = book_publisher

        book.book_image_url_l = book_image_url_l
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('book_operate.book_list'))
    return render_template('book_change.html', book=book)



